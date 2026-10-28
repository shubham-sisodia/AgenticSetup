// eslint.config.js (flat config)
// Keep the element -> component mapping identical to designSystem.forbidElements in .claude/guardrails.json.
import react from "eslint-plugin-react";

const forbid = (element, component, pkg = "@acme/ui") => ({
  element,
  message: `use <${component}> from ${pkg}`,
});

export default [
  {
    files: ["src2/**/*.{tsx,jsx}"],
    ignores: ["**/*.test.*", "**/*.stories.*"],
    plugins: { react },
    rules: {
      "react/forbid-elements": ["error", {
        forbid: [
          forbid("button", "Button"),
          forbid("input", "Input"),
          forbid("select", "Select"),
          forbid("textarea", "Textarea"),
          forbid("table", "DataTable"),
          { element: "a", message: "use the router <Link> for in-app links" },
        ],
      }],
    },
  },
];
