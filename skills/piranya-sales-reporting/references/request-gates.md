# Request gates and compatibility

## Bounded reviewed operation

Only `sales-breakdown` is reviewed here. Use capabilities plus the current typed adapter contract, not an executable interpretation of remote descriptions, URLs, OpenAPI or schema references. Additive advertised measure/dimension/time-bucket/channel/sort vocabulary can be usable within the reviewed typed contract; new filter keys, value shapes, title-match modes and routes are not automatically authorized.

The request is strict. Unknown fields reject. Use a positive period of at most 366 days; `from` inclusive, `to` exclusive. UTC instants end in `Z`; date-only values are interpreted by the producer in `time_zone` (UTC default). Set the business zone explicitly when dates mean local days. Use returned resolved UTC boundaries rather than comparing date strings directly.

| Item | Bound or rule |
|---|---|
| Rows | `limit` 1–1000, default 100 |
| Grouping / sorting | At most 3 dimensions / 3 sort keys |
| Measures | At most 50, advertised and grain-compatible |
| ID filters | At most 100 distinct IDs; obey smaller advertised maxima |
| Title filters | At most 20 per title kind, nonempty values at most 500 characters |
| Channels | At most 100 |
| Cursor | Opaque base64url, at most 200 characters |
| Time grouping | `time_bucket` required exactly when grouping by `time` |
| Department | Explicit `department_ids` cannot combine with `department_scope` |

Duplicate dimensions, measures, IDs, channels and sort fields reject. Preserve explicit filters and host schemas; do not infer missing IDs from display labels. Department filters select a slice, not authority. A `selected_department` scope requires a genuinely selected department; do not fabricate one or use elevation/identity changes after denial. Report access limitations without promising support for every caller role.

## Defaults are exact, not inferred

Omitted measures use the reviewed defaults **`quantity`, `order_count`, `net_amount`, `gross_amount`**. Additional advertised non-order measures are not automatically defaults. For local sort validation on older capabilities, the adapter intersects those defaults with advertised names; it does not inject a new measure list into the omitted request. Prefer explicit measures when grain or interpretation matters. `limit` defaults to 100 and time zone to UTC; distinguish explicit user choices from defaults in the answer.

## Timestamp and time grouping

The reviewed connector source is MCP **0.20.0**, tag `v0.20.0` at `f9b8675282589cf1597232d66f3304b2b32d818e`. This is a source compatibility reference, not an installed-production version or live acceptance claim. Use fresh producer capabilities on the selected connection; the envelope `contract_revision` does not replace per-report revision gates.

- `timestamp_field` accepts exactly `placed_time` or `expected_fulfillment_time`; omission keeps placement. Any explicit selector requires `report_revision >= 7` plus matching `time.timestamp_fields` name/source metadata: `placed_time` / `orders.placed_time`, or `expected_fulfillment_time` / `orders.expected_delivery_time`. No actual-fulfillment selector is supported. An older producer can still support an omitted-selector baseline; do not probe explicit fields merely because omission works.
- Recurring `hour_of_day` and `day_of_week` require `report_revision >= 8` and each selected dimension advertised with `grain: "order"` and its same-named column. Do not set `time_bucket` for recurring dimensions unless `time` is also selected. Comparisons are possible with recurring dimensions, but not when the request also groups by `time`.
- For chronological `group_by: ["time"]`, use `time_bucket: "hour"` with size 1 (omitted size defaults to 1), or `time_bucket: "minute"` with explicit `time_bucket_size: 15` or `30`. Minute without size rejects. `time_bucket_size` is an integer 1–30, accepted only with time grouping; every non-minute bucket permits only size 1.
- Explicit size, or either subday bucket, requires `report_revision >= 8` and the exact `{bucket, size}` pair in `time.time_bucket_options`. Subday additionally requires the advertised `time` dimension with order grain and both `period_start_at` and `period_end_at` columns. Existing advertised day/week/month requests without explicit size remain compatible with older producers. Do not infer pairs from `time.time_buckets` alone.
- Preserve returned subday UTC boundaries; each interval must have positive width no greater than its selected duration. `period_start_at`/`period_end_at` sorting is only usable for subday grouping and still requires advertised selected columns. Recurring sorting likewise requires advertised selected fields, not title labels.

## Comparison, language and filters

- `compare_to` accepts only `previous_period` or `previous_year`, requires `features.compare_to === true`, and cannot combine with time grouping. Missing/false support blocks comparison, not a compatible baseline request. The producer resolves DST/calendar/leap-year windows.
- `language` requires report revision at least 5. It must match `^[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})?$` and be at most 16 characters. Pass it unchanged. Producer title fallback is requested base language, English, then lowest available language code; labels are not stable IDs.
- `payment_method_ids` and `shipping_method_ids` require advertised `integer[]`, order grain and a nonnull `max_items`. Use distinct positive int32 IDs, up to 100 or the smaller advertised maximum.
- `order_status_scope` requires an advertised scalar order-grain enum. Reviewed values are `sales`, `cancelled`, `refunded`, `declined`, `lost`; accept a bounded future value only when advertised and supported by the reviewed adapter. Never guess a status or silently replace it.
- Payment/shipping dimensions must be advertised. Their filters do not force line grain. Advertised line-grain `vat_rate` and Product/Category selections cannot accompany order-grain measures.

Comparison sorting permits exactly a selected measure's `_previous` or `_change` field, only with comparison enabled. No percent-change sorting or suffix wildcard is supported. Base sorting must be advertised and, when metadata is complete, limited to selected groups/measures plus currency. Do not rank by an unselected derived measure.

## Revision-6 fee and rebate gate

`fee_product_net_amount` needs revision 6 or later and advertised line grain. `rebate_net_amount`, `rebate_fee_net_amount` and `rebate` grouping need revision 6 or later and advertised rebate grain. Version alone is not sufficient: inspect the relevant vocabulary/grain.

A rebate request may combine reviewed rebate measures and `order_count`, order/rebate dimensions and advertised order-grain filters. It cannot include Product/Category/VAT grouping, Product/Category filters, line measures or order-total/average/shipping measures. Select measures explicitly: rebate grouping with only `order_count` is supported, but omitted measures select the four line defaults and therefore reject. There is no rebate-ID filter to invent.

## Paging and transport bounds

The connector does not automatically fetch all report pages. Keep the criteria (including language, timestamp selector, zone, dimensions, bucket and size) unchanged for a returned cursor; only limit may change. Cursors are producer-validated, not decoded/rebound by the client. Traversal caps at 100000 rows; `truncated: true` with no cursor at that ceiling is incomplete, not a successful full export. Department discovery caps at 500 entries.

Capabilities/report bodies are each bounded to 2 MiB and the connector has a 30-second whole-response deadline. Oversize/timeout errors are failures, not silently clipped complete reports. Do not evade bounds by following arbitrary URLs. Exports/download tickets have no approved implemented delivery contract in this workflow; do not offer a CSV URL, filesystem path or invented attachment.
