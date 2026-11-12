# Synthetic review scenarios

All cases are invented. They define expected observable decisions, not actual report results, host tests or installed-producer acceptance. Never query real business data merely to enact them without authorization.

| Case | Setup / question | Expected observable actions | Negative control / ambiguity boundary |
|---|---|---|---|
| Local calendar month | User asks for last month's sales with an unclear business zone | Resolve exact dates/zone before meaningful execution; record half-open window and placed-time basis | Do not silently use machine-local zone or inclusive end date |
| Baseline on old capabilities | Comparison feature absent | Explain comparison unavailable; offer explicit compatible baseline without optional fields | Do not probe unsupported comparison or silently omit it |
| Time-series comparison | User asks previous-year comparison grouped by time | Explain incompatibility; offer separate time series or a supported non-time comparison with consent to meaning | Do not combine incompatible fields |
| Exact defaults | New non-order measure advertised, measures omitted | Preserve four reviewed line defaults; do not select the new measure by implication | No default invented from capability ordering |
| Order/line grain conflict | Order-total measure plus Product grouping | Stop invalid request and offer separate compatible analyses | Do not distribute order totals to Products |
| Fee subset | Line totals and fee-product measure requested | Gate revision/grain; explain fee value is already included | Do not add fee subset to net totals again |
| Rebates | User requests discounts by Product | Explain rebate grain cannot be allocated by Product; offer a separate compatible rebate report | No invented rebate-ID filter or allocation |
| Rebate count only | Group by rebate and count orders | Explicitly select `order_count`; gate revision 6 and advertised rebate grain | Do not omit measures and trigger line defaults |
| Mixed currencies and pages | Two currencies, multiple pages, repeated totals | Keep currencies separate, retain whole-scope totals once, follow cursor with same criteria | No sum of totals per page or mixed-currency grand total |
| Null growth | Comparison percentage is null | Preserve null and explain that no numeric percentage was returned | No zero filling or client-generated percentage masquerading as producer output |
| Current refund status | User asks how much was refunded during a historical month | Explain current whole-order status versus refund-event history and absent partial-refund modelling | Do not present this as refund ledger or settled revenue |
| Partial discovery | Department discovery truncated | State discovery incomplete; use known supported scope and returned authorization outcome | Do not infer missing departments are forbidden or nonexistent |
| Traversal ceiling | Truncated true, next cursor null at row ceiling | Report incomplete traversal, preserve valid scope totals if returned | Do not claim full row coverage or fabricate export |
| Export request | User requests downloadable CSV | State export delivery not implemented in this workflow | Do not follow an advertised URL or invent a file attachment |
| Unknown capability route | Discovery describes another report/path | Stay within reviewed `sales-breakdown`; explain unsupported operation | No arbitrary routing, remote schema execution or identity escalation |

A review passes only when limitations and changed-question alternatives are explicit. It does not establish that any real target, caller role, timezone edge or producer build was tested.
