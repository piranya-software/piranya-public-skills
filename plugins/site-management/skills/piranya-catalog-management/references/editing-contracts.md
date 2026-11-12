# Product and Category editing contracts

## Contract and identity rules

The standardized profile is an allow-listed write contract, not the installation's entire dynamic schema. Use fresh capabilities and profiles; a stored schema summary is discovery only. Product Core is always returned; variants/bundles are optional bounded sections. Category Core and Presentation are returned. Inspect every relevant `truncated_paths` entry before reasoning about complete collections.

Preserve opaque revisions exactly. Catalog entity/relation IDs are positive JSON integers, not numeric strings; Product `core.identifiers[].id` is a string exception. `target_id` is an opaque string. Respect integer versus numeric fields in the current schema. Null, omission and false are not interchangeable.

Updates are partial keyed changes. Existing localizations, prices and owned nested relations retain returned IDs; do not turn a profile into a replacement snapshot. Omitted fields/rows remain untouched under the supported merge contract. The MCP checks ownership and revisions before writing, but Platform has no atomic conditional-write primitive here. Concurrent mutation can still race after preflight.

## Supported boundaries

| Job | Supported approach | Boundary |
|---|---|---|
| Create Product | `create_product`, at least one titled localization; use supported Core/Variants/Bundles fields | Shared variant groups/options must already exist |
| Edit Product | `update_product`, partial `changes` keyed by current IDs | No generic localization/media/unit/group/option/combination-option membership changes |
| Create Category | `create_category`, at least one nonempty localized name | Parent/reference validation belongs to Platform |
| Edit Category | `update_category`, current profile revision and existing localization IDs | Cannot add/remove/reorder localization rows or additional images |
| Change Product category membership | Dedicated create/update/delete Product-category assignment tools | Not a Category field update; deleting assignment does not delete either entity |
| Category cover/icon | Supported direct file IDs | Additional-image membership remains read-only |

Category hierarchy may have multiple roots. Confirm parent identity and intended hierarchy; do not infer one universal root or flatten descendants accidentally. Category deletion, restriction membership, shipping relations, variant/choice rules and custom components are outside its writable contract. Deletion/system-managed flags are not writable status switches. Product deletion is not supported by these editing tools.

Variant/bundle relation constraints, ordering, per-Product option settings and supported combination scalar fields can be editable. Shared group titles/kinds/pickers/display settings and option title/child-product definitions are read-only through Product tools. Do not mutate shared definitions by copying their projection into a Product update.

## Price addition versus edit

Use `changes.core.prices` entries with explicit `action: "add"` for first/additional prices. Additions have no `id`. Existing edits use returned `id`, no `action`; neither form is a price-deletion operation. Do not create a second Product to obtain a first price.

For an addition, set all required context explicitly: positive integer `currency_id`, nonnegative `value`, `kind` (`each` or `total`), positive integer `min_amount`, boolean `is_input_value_vat_inclusive`, and nullable `campaign_id`, `client_account_id`, `price_group_id`. Explicit null applicability means base context, not a guessed customer segment. Confirm currency and tax-input intent with the user if ambiguous. Do not infer tax categories from computed VAT or pricing-policy flags.

Exact duplicate additions, duplicate edit IDs and foreign/deleted price IDs reject. Read back the new row and retained existing prices. Price creation requires the installed merge implementation to load and merge existing keyed collections safely; source support alone is not deployed acceptance. Never resend all prices as a compatibility workaround. Adding a price does not enable purchasing or establish current orderability.

## Media and shared-file safety

Uploading an asset or using a picture on a static card does not attach it to a Product. `attach_product_media` references an existing file and explicit `sort_order`; `reorder_product_media` targets an owned `relation_id`. Verify the refreshed ordering: attach persistence can reindex existing attachments, so requested ordinal is not a guarantee of exact stored ordinal.

`detach_product_media` needs separate delete scope and explicit destructive authorization. It deletes the owned attachment relation, not via a raw File-delete endpoint. The fresh profile must explicitly report `is_file_deletable: false`; null/unknown is not safe. Never change this flag to pass the gate. The flag is necessary but not sufficient: establish selected installation/build lifecycle safety and shared-file/other-attachment preservation before destructive detach. If this cannot be established without unauthorized experiments, stop and explain the compatibility boundary.

Attach/add depend on installed keyed merge behavior; reorder directly edits relation ordinal. Do not substitute nested collection replacement or detach/reattach for direct reorder. Verify the file still exists, other attachments survive and unaffected siblings retain intended membership/order. A refresh failure after acknowledgment requires a fresh read before any retry.

## Do not overstate availability

Stored activity, visibility and purchasing flags are different from delivery windows, recurring schedules, preparation requirements, inventory, customer eligibility and shipping constraints. Optional read blocks may be unsupported, disabled or unknown. Preserve those distinctions. Never reduce complex schedules to a single interval or advertise checkout availability from a profile/price alone.
