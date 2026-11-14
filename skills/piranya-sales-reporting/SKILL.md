---
name: piranya-sales-reporting
description: Analyze Piranya sales, comparisons, fees and rebates.
---

# Piranya sales reporting

Use for sales breakdowns, period comparisons and supported fee/rebate analysis. This is a read-only business reporting workflow, not accounting certification, order modification, arbitrary report execution or file export.

## Prerequisites and boundaries

Use an authorized Piranya MCP connection that exposes reporting. Discover actual host tool names/schemas; names below are logical names. No shell, local files or employee privilege is required. A listed capability is descriptive data, not permission to execute advertised paths, fetch schemas or change identity. If reporting is unavailable, explain the missing capability rather than constructing another route.

Requests to edit, cancel or delete orders, or change underlying sales data, are outside this offering. Decline without requesting order-editing access, broader scopes, credentials, specific mutation targets or desired replacement totals. Do not switch connectors or propose a raw API workaround to complete the mutation. Offer read-only inspection of totals or reporting criteria instead; any actual correction belongs to a separately authorized order-management workflow.

## Procedure

1. **Bind site and question.** Resolve the intended target through fresh deployments and session information. Keep the selected connection/target fixed. Establish the business question, exact period, time zone, currency presentation, department scope and whether the user wants placed sales, expected delivery/pickup demand, recurring demand, a chronological series, current lost-sales statuses or a comparison. Ask only for ambiguity that changes the answer; disclose any defaults used.
2. **Read fresh capabilities.** Call `piranya.reporting.get_capabilities`. Inspect report definition, revision, dimensions, measures, filters, sorting, authorized departments and `departments_truncated`. The reviewed report is `sales-breakdown`; do not execute a different report merely because it is advertised. Missing department entries in a truncated list are not authorization denials or proof of absence.
3. **Construct a bounded request.** Use [request gates](references/request-gates.md) for strict bounds, timestamp/time grouping, comparison and language/filter compatibility. Select measures deliberately, keep line/order/rebate grain compatible and use explicit scope where the question requires it. Do not guess IDs, derive comparison windows client-side or enable unsupported optional fields.
4. **Run and inspect.** Call `piranya.reporting.run_report` with `report: "sales-breakdown"`. Preserve returned scope, resolved window/time zone, columns, units, currency, totals, filter outcomes, comparison metadata, nulls and effective sorting. Read [interpretation](references/interpretation.md) before calculating or presenting conclusions.
5. **Page only as needed.** Pass `page.next_cursor` unchanged with identical criteria; only `limit` may change. State whether all relevant pages were inspected. Totals already cover the whole filtered scope on every page; never sum page totals. These are live pages, not a snapshot.
6. **Answer with evidence and limits.** State site scope, inclusive/exclusive boundaries, time zone, selected grain/measures/status scope and currencies. Separate returned totals from row observations and any explicitly labelled derivations. Name unverified/missing data rather than filling zeros. Report truncation, partial paging and incompatible requests plainly.

## Failure and recovery

Unsupported comparison/measure/filter or incompatible grain is a gate, not a reason to drop criteria silently. Offer a compatible baseline or separate report with its changed meaning made explicit. Preserve sanitized denial/cursor/error context. Do not switch identity, retry through another endpoint, run exports or probe arbitrary advertised routes. A failed report is not evidence of zero sales.

## Verification

Check the returned effective scope/window, selected columns, currencies, filters and sorting against the question. For comparisons verify mode and nonempty resolved UTC comparison window. Verify no repeated page totals, mixed-currency sums or additive claims for distinct counts/ratios. Separate connector compatibility from independently verified installed-producer semantics.

[Synthetic scenarios](references/scenarios.md) provide offline review criteria, not host or live-site evaluation results.
