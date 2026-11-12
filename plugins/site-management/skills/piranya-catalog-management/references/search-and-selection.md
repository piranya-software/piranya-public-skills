# Search and target selection

Search performs one bounded native read, not arbitrary schema-driven querying. Use the tool's static typed selectors; do not add dotted relation paths, raw REST controls, operators or guessed filters.

## Category selection for Products

`category_ids` accepts 1–100 distinct positive signed 32-bit integers. Multiple Categories match **OR**, not AND. Descendants are included by default; retain that user-friendly department/category interpretation unless the user requests direct membership. Set `include_sub_categories: false` for direct-only membership. Either boolean requires a category selector. Do not combine `category_ids` with the scalar `category_id` equality selector.

Native category selection retains campaign applicability. There is no supported campaign-bypass or campaign-only search control. Category membership search is not a customer pricing/orderability calculation.

## Equality filters

Use at most 20 unique `{field, value}` filters. Values retain their actual types; strings are not coerced to booleans or IDs.

| Entity | Positive integer fields | Boolean fields |
|---|---|---|
| Product | `id`, `department_id`, `owner_department_id`, `category_id` | `is_active`, `is_deleted`, `is_hidden` |
| Category | `id`, `department_id`, `parent_id` | `is_deleted`, `is_hidden` |

Product `owner_department_id` and `department_id` are aliases; combining them conflicts. Category has no `is_active` filter. Unknown/duplicate/conflicting fields and arbitrary nested keys reject. Native ID selectors can suppress normal active/nonhidden defaults; set explicit status filters when state matters.

Ordinary Product search selects active, nonhidden Products. To investigate hidden/inactive records, choose the required `is_hidden` and `is_active` filters deliberately rather than declaring missing records from ordinary search. An exact profile read can succeed even when a generic list excludes the record.

## Pagination and completeness

Product pages default to 20, cap 50; Category pages default to 50, cap 100. Text queries are trimmed and bounded to 1–500 characters. Pass returned cursors unchanged with the same target, entity, query and selectors. Do not decode or repurpose them: they do not promise signed query binding or snapshot consistency.

Follow every relevant page before claiming a complete inventory or preparing a bulk edit. If access, a cap or host limitations prevent completion, name the boundary. Do not post-filter one page and present it as a complete native filtered result. On older installations, establish that selectors are honored before relying on them for mutation selection; use authorized read controls with known inclusions/exclusions, not customer write experiments. Stop if observed results contradict the filter contract.
