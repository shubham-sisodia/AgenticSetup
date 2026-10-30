# Test checklist: feature/invoice-filters

Tick each hunk `- [x]` only after it is verified; say how (unit / component / Playwright / typecheck / manual) and cite the test file + result. Re-staging changes the diff and needs a new checklist.

## src/lib/filters.ts
- [x] L12-40: unit: src/lib/filters.test.ts "empty query returns all rows", "status=paid keeps paid only" (pass)
- [x] L58 (deletion): unit: same file, removed helper had no other callers (rg shows 0) (pass)

## src/pages/invoices/InvoiceFilters.tsx
- [x] L1-64: component: src/pages/invoices/InvoiceFilters.test.tsx "typing updates ?q= in the URL" (pass)

## src/pages/invoices/columns.tsx
- [x] L20-22: typecheck only: renamed column key, `tsc -b` clean

## e2e/invoices.spec.ts
- [x] L1-30: Playwright: e2e/invoices.spec.ts "filter survives reload" chromium (pass)

## Commands run
- [x] npm run test -- src/lib src/pages/invoices: 14 passed
- [x] npx tsc -b: 0 errors
- [x] npx playwright test e2e/invoices.spec.ts: 1 passed
