#!/usr/bin/env python3
"""Project registry hooks. Registry: ~/.claude/projects.json (the single home for aliases and agents).

  projects.py session              SessionStart: inject the alias list + the current project's advisor/test rules
  projects.py gate                 PreToolUse(Bash): deny `git commit` without a complete test checklist
  projects.py checklist [dir]      write (or find) the checklist skeleton for the current staged diff, print its path

Resolve order: the main repo's folder name (worktrees resolve through `git-common-dir`), then any ancestor
folder name (for projects that are not git repos). `tester: null` means no commit gate for that project.
Fails open: any crash exits 1 with a traceback, which Claude Code treats as a non-blocking hook error.
Set PROJECTS_REGISTRY to point at another registry file (used by the tests).
"""
import hashlib, json, os, re, subprocess, sys

REG = os.path.expanduser(os.environ.get("PROJECTS_REGISTRY", "~/.claude/projects.json"))
SELF = "~/.claude/hooks/projects.py"
CODE = re.compile(r"\.(tsx?|jsx?|mjs|cjs|css|scss|html|py|kt|kts|java|gradle|json|ya?ml|sh|sql|vue)$")
NOT_CODE = re.compile(r"(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|\.snap)$")


def git(d, *a):
    r = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def registry():
    return json.load(open(REG))


def projects():
    return registry()["projects"]


def resolve(d):
    """Registry entry for dir d. Worktrees resolve to their main repo via git-common-dir."""
    reg = projects()
    common = git(d, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if common:
        name = os.path.basename(os.path.dirname(common.strip().rstrip("/")))
        if name in reg:
            return name, reg[name]
    p = os.path.abspath(d)  # non-git projects: match any ancestor folder
    while p != "/":
        if os.path.basename(p) in reg:
            return os.path.basename(p), reg[os.path.basename(p)]
        p = os.path.dirname(p)
    return None, None


def staged_code(d):
    names = (git(d, "diff", "--cached", "--name-only") or "").split()
    return [n for n in names if CODE.search(n) and not NOT_CODE.search(n)]


def hunks(d, f):
    out = git(d, "diff", "--cached", "-U0", "--", f) or ""
    rs = []
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, n = int(m.group(1)), int(m.group(2) or 1)
        rs.append(f"L{start}-{start + n - 1}" if n else f"L{start} (deletion)")
    return rs


def checklist_path(d):
    """One checklist per exact staged diff: re-staging changes the hash and needs a new checklist."""
    diff = subprocess.run(["git", "-C", d, "diff", "--cached", "--binary"], capture_output=True).stdout
    gd = git(d, "rev-parse", "--path-format=absolute", "--git-dir").strip()
    return os.path.join(gd, "test-checklists", hashlib.sha256(diff).hexdigest()[:12] + ".md")


def session():
    inp = json.load(sys.stdin)
    full = registry()
    reg = full["projects"]
    aliases = ", ".join(f"{v['alias']} = {k}" for k, v in reg.items())
    line = f"Project aliases (the user refers to projects by alias): {aliases}."
    if full.get("root"):
        line += f" Folders live in {full['root']}."
    ctx = [line]
    name, p = resolve(inp.get("cwd", os.getcwd()))
    if p:
        ctx.append(f"This session is in **{p['alias']}** ({name}, {p['kind']}).")
        if p.get("advisor"):
            ui = p.get("uiAdvisor", full.get("uiAdvisor"))
            extra = f" UI questions additionally go to `{ui}`." if ui else ""
            ctx.append(f"Before starting the user's first task, invoke the `{p['advisor']}` subagent with that task "
                       f"and the current branch, and act on its answer.{extra}")
        if p.get("tester"):
            ctx.append(f"Every code change is verified by `{p['tester']}` before commit: stage the change (separate "
                       f"command), invoke `{p['tester']}` on the staged diff (it picks the test layer, runs the tests and "
                       f"fills the checklist with `python3 {SELF} checklist`), then commit. A hook blocks "
                       f"commits whose staged diff has no complete checklist.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(ctx)}}))


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def gate():
    inp = json.load(sys.stdin)
    cmd = inp.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\b[^;&|\n]*\bcommit\b", cmd) or "CLAUDE_SKIP_TEST_GATE=1" in cmd:
        return
    cwd = inp.get("cwd", os.getcwd())
    m = re.search(r"\bgit\s+-C\s+(\S+)", cmd) or re.match(r"\s*cd\s+(\S+)\s*&&", cmd)
    d = os.path.join(cwd, os.path.expanduser(m.group(1).strip("'\""))) if m else cwd
    name, p = resolve(d)
    if not p or not p.get("tester"):
        return
    if re.search(r"\bgit\s+(-C\s+\S+\s+)?add\b", cmd) or re.search(r"\bcommit\b[^;&|\n]*(\s-[a-zA-Z]*a[a-zA-Z]*\b|--all\b)", cmd):
        deny("Commit gate: stage changes in a separate command first (no `git add`/`-a` in the commit command), "
             f"then run `{p['tester']}` on the staged diff, then commit.")
    files = staged_code(d)
    if not files:
        return
    path = checklist_path(d)
    if not os.path.exists(path):
        deny(f"Commit gate ({p['alias']}): no test checklist for this staged diff. Invoke `{p['tester']}` to test "
             f"the staged changes and fill {path} (create it with `python3 {SELF} checklist {d}`). "
             "If the user explicitly waived testing, prefix the commit with CLAUDE_SKIP_TEST_GATE=1.")
    text = open(path).read()
    problems = []
    if re.search(r"^\s*- \[ \]", text, re.M):
        problems.append("unchecked `- [ ]` items remain")
    for f in files:
        sec = re.search(rf"^## {re.escape(f)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
        need = len(hunks(d, f))
        got = len(re.findall(r"^\s*- \[x\]", sec.group(1), re.M)) if sec else 0
        if got < need:
            problems.append(f"{f}: {got}/{need} hunks checked")
    if problems:
        deny(f"Commit gate ({p['alias']}): checklist {path} incomplete: " + "; ".join(problems))


def checklist(d):
    path = checklist_path(d)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        branch = (git(d, "branch", "--show-current") or "").strip() or "detached"
        out = [f"# Test checklist: {branch}", "",
               "Tick each hunk `- [x]` only after it is verified; say how (unit / component / Playwright / typecheck / "
               "manual) and cite the test file + result. Re-staging changes the diff and needs a new checklist.", ""]
        for f in staged_code(d):
            out += [f"## {f}"] + [f"- [ ] {h}: " for h in hunks(d, f)] + [""]
        out += ["## Commands run", "- [ ] ", ""]
        open(path, "w").write("\n".join(out))
    print(path)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "session":
        session()
    elif mode == "gate":
        gate()
    elif mode == "checklist":
        checklist(sys.argv[2] if len(sys.argv) > 2 else os.getcwd())
