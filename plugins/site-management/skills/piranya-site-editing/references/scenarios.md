# Synthetic review scenarios

These invented cases describe expected observable actions. They are not execution logs, supplied customer examples or proof of host evaluation. Use discovered schemas and authorized read surfaces; do not create test resources on a real site to enact them.

| Case | Setup / request | Expected observable actions | Must not do / compatibility boundary |
|---|---|---|---|
| Local text change | A page heading needs correction | Resolve site/page; read current lines/revision; exact guarded patch; readback and targeted rendered text check | Full rewrite from a truncated excerpt; claim editor verified without opening it |
| Concurrent edit | Revision changes after inspection | Re-read and compare both changes; preserve unrelated edit; apply reconciled payload with fresh guard | Blind retry with a new revision |
| Shared metadata | Master content saved before head change | Read current head revision after content save, then guarded head patch | Reuse pre-content head revision |
| Uncertain create | Connection drops after page create | Search/read exact intended resources and identity before deciding whether another create is needed | Assume failure and create a duplicate |
| Hidden preview ambiguity | User asks for a private redesign, only ordinary page creation is exposed | Explain missing access-control proof; establish guest/sitemap controls or seek acceptance of an explicitly public preview | Claim unlinked/noindex is private; publish first and ask later |
| Native commerce route | User wants checkout restyled | Inspect native Shop route vocabulary, active shell and narrow selectors; verify relevant native controls within consent | Create a checkout CustomPage or submit an order to prove CSS |
| Editor conversion | Raw rich text is being made editable | Use appropriate native wrappers, unique new UUIDs and preserved existing identities; inspect wrapper sizes and editor opening | Treat guest rendering as proof of editor validity |
| Theme not visible | Theme saved but no matching rule | Inspect rule scope and effective values; activate only approved context; verify readback then render | Broad wildcard activation to bypass an unavailable narrow scope |
| Upload unsupported by host | User supplies a large private font, host cannot transfer bytes | State transfer limitation and request an approved supported upload route | Publish source publicly or fabricate encoded bytes |
| Shared stylesheet | One page requested, stylesheet has many usages | Inspect usage; choose scoped change and verify affected contexts | Claim site-wide safety from one page screenshot |


## Rendering and control contract cases

| Case | Required observation / decision | Negative control |
|---|---|---|
| Saved CSS absent from pack | Compare saved source, actual generated link, compile comments, loaded rules and active paint | No dummy cache edits or arbitrary URL probes |
| Third cascade competitor | Inspect every matching rule including nested rules and both pseudo-elements, per property | No blanket important reset after finding only one competitor |
| Hidden paint / old console | Reproduce in fresh visible context and inspect present-tense behavior | No stale-error or browser-bug conclusion from retained logs alone |
| Root/footer overlap | Measure root height, direct-child float and footer boundary; inspect top-level inline dimensions | No min-height masking or invented root attribute |
| Narrow shared card | Measure component width, largest number, wrapping rows, min constraints and optional children | Viewport alone and one short value are insufficient |
| Sticky multi-row header | Measure current complete header and hit-test scrolled controls | No constant offset or duplicate native column grid |
| Silent amount/submit control | Compare direct-child relationships and original form ancestry; exercise keyboard and click | No cloned input, moved-out submit or proxy business logic |
| Conditional picker | Inspect real data membership, hidden/float state, picker mode and popup/detail contexts | No fake HTML options, full nested resends or unsupported endpoint repair |
| Conditional totals | Observe native financial display and authorized rebate/plain/variant states | No price engine clone, basket mutation without consent or checkout submission |
| CSS split / insertion | Verify cascade order, remove duplicates sequentially and read surrounding braces | No parallel remove/add, placeholder live resource or debug narrative |

Review completion requires a visible decision at each gate and explicit unperformed checks. Older installations may lack an operation or differ in rendering; stop at the missing contract instead of inventing fallback APIs.
