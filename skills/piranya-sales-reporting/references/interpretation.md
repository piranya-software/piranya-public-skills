# Interpret sales without changing their meaning

## Time and status

Reports use `orders.placed_time`, not payment settlement or delivery time. Preserve `source_timestamp_field`, `reporting_time_zone`, resolved half-open windows and bucket definitions. Date-only requests resolve in the producer's zone; do not rebucket client-side. Stored local timestamps can have repeated-hour ambiguity at autumn DST; state this when material.

Counted orders exclude deleted, test and synthetic payment orders. Default `sales` excludes currently declined/refunded/cancelled orders. Lost-sales status scopes select **current whole-order status**, not a historical ledger of refund events. Partial refunds are not modelled. Payment state is not filtered. Never label these results settled cash, recognized revenue or a refund audit without another supported source.

Order-grain measures exclude suborders invoiced with their parent to avoid duplicate parent totals. Line-grain measures count each order's own lines once. These grains answer different questions; do not merge them into an invented reconciliation.

## Amounts, fees and rebates

- Line net/gross amounts precede order-level rebates and shipping. Order totals are after rebates and include shipping.
- `fee_product_net_amount` is the subset of fee-product line value **already included** in line totals. Do not add it again. Fees billed outside orders are excluded.
- `rebate_net_amount` is positive order rebate value. `rebate_fee_net_amount` is the absolute value of negative rebates (price-raising fees). Do not net these against each other or subtract both as discounts.
- Rebate reports read order-rebate records. They do not allocate discounts to Products, Categories or VAT rates. Do not invent an allocation to force totals to reconcile.
- The producer rounds aggregates once per currency using currency decimal places (fallback two), away from zero. Preserve serialized amounts; do not reround to manufacture agreement.

Report currency columns and units alongside values. Keep currencies separate; unknown/null currency is not a default currency and must remain explicit. A currency conversion requires a separately authorized source and methodology, not an implicit sum.

## Totals and nonadditivity

Returned totals cover the entire filtered scope on **every page**, not that page's rows. Retain totals once. A page of leading Products is not the full catalog; distinguish whole-scope totals from the displayed subset.

`order_count` is distinct and nonadditive across Product/Category and rebate groups. An order appearing in two groups is not two distinct orders overall. Average order value and other ratios cannot be summed or averaged across rows. Do not reconstruct totals from grouped rows, fill absent groups with zero or combine currencies to create a grand total.

Preserve comparison metadata, `derived_from`, `derivation`, units and currency-column relationships. Keep null percentages null; they are not zero growth. The connector does not compute comparison percentages, merge groups or reconstruct totals. If an additional calculation is explicitly requested, label it as a derivation, use a calculation tool when available and state its inputs; do not present it as producer-returned data.

## A useful final answer

Lead with the business result, then enough context to make it reproducible:

1. Selected site and effective department scope, including unknown/truncated discovery.
2. Resolved date boundaries/time zone and the placed-time basis.
3. Measures, grain, currency separation and current status scope.
4. Producer totals versus selected row observations; comparison mode/window if used.
5. Pagination/truncation, live-data movement, missing measures and unverified interpretations.

No matching rows, a denied report and a truncated response are different outcomes. No rows do not prove a complete historical absence outside the requested scope. A valid envelope or revision is compatibility evidence, not proof all installed producer semantics were independently tested.
