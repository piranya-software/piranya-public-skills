# Native control contracts and conditional commerce states

## Keep the working native structure

Native controls own state, validation, availability, price calculation and submission. Style or reposition existing nodes; do not clone inputs, submit buttons, choice logic, pricing or business rules. Read the actual current markup and supported integration contract before structural edits. A silent click with no request is a possible ancestry failure, not proof that another endpoint is needed.

- Keep each real submit/add control inside its original form. Fixed positioning does not require moving it outside the form. Inspect form ancestry and handler lookup assumptions before moving any node.
- Preserve direct-child and sibling relationships used by native handlers. A decorative wrapper around an amount picker can break child-only lookups while looking correct. Use grid/flex placement of existing children first; test mouse, keyboard, focus and change behavior afterward.
- Preserve real native inputs, names, data attributes, validation and state events. Presentation shortcuts must drive the supported native control rather than an independent quantity/selection model. Do not assume every product detail mode or cart API is equivalent, and do not turn a source-specific implementation example into a public frozen API contract.
- Observe native state rather than forcing it: selected classes, checked/disabled inputs, open/closed drawer classes, loading and error state can be updated asynchronously. Derived presentation must be idempotent. A broad MutationObserver callback that writes identical content repeatedly can observe its own writes forever; guard one-time setup and compare derived output before writing.

## Inspect every rendering variant

A product card, popup and standalone detail page are separate styling contexts. Simple, grouped/configurable products and picker modes (including `toggle_box_button`) can use different structures and rules. Inventory the actual variants and test each affected context, not just the first product. Native button styles in list cards do not automatically cover detail-page buttons.

Checkboxes/radios may keep their real input offscreen while adjacent label `::before`/`::after` paints the visible indicator. Check input position, clipping, opacity and both pseudo-elements before styling accent-color or redrawing controls. Inspect all matching rules and their complete declarations, including checked-state transforms, offsets, opacity and clipping. Reused classes can name both a row and a nested label: target the intended direct-child level to avoid double padding/chrome. Existing icon fonts can have custom codepoint maps; verify actual rendered glyphs instead of assuming standard mappings. Keep decorative icons outside rich-text sanitization boundaries, and measure the native editor wrapper as well as its contents.

Drawer open/closed state, overlay and outer wrapper must agree at wide and narrow widths. Inspect supported native desktop/mobile behavior classes before recreating hide/show CSS. A reveal transform on an ancestor can change the containing block for fixed drawers. Preserve required native ancestry if a supported structural repair is necessary; avoid relocating the drawer merely as a visual workaround. Author display rules for elements toggled with `hidden` so they do not override hidden state (for example, scope flex/grid display to `:not([hidden])`).

## Empty picker: data, state or presentation?

First distinguish absent data, conditional rendering, hidden/clipped content, float collapse and an actual binding failure. If group options are present but no choices populate, inspect supported catalog profiles and relation consistency: each option's variant-group identity must agree with the relation's group identity. A populated response alone does not prove consistent membership. Use the catalog companion/current schemas for supported corrections with fresh guards and readback. If the required edit is unavailable, report the exact bounded mismatch and supported administration path; never fake options in workspace HTML, probe endpoints, or resend an entire nested product graph to repair one relation.

Use real authorized representative states: plain/variant rows, empty/populated baskets, conditional discounts, stock/availability, shipping/payment choices, selected/unselected and loading/error states where relevant. A conditional element missing from one sample is not proof it never renders. Populate only within separately authorized test-data/basket scope; do not invent catalog facts or change live prices/availability to manufacture coverage. Separate read/inspection, catalog write, basket mutation and order/payment consent. Report unreachable states as unverified rather than passed.

## Native financial display guard

Keep totals, rebates, tax, currency, rounding, quantity steps and eligibility under native business logic. A cosmetic summary may reflect native-rendered values through a supported presentation contract; it must not recalculate payable amounts, copy prototype pricing rules or submit its own financial state. Currency/number parts may be separate spans with CSS-only spacing: parent textContent can concatenate them. Preserve meaningful parts and accessible spacing without parsing formatted strings into a replacement pricing engine. Verify conditional rebate rows and generic global classes such as price, not just the normal total.

A first wizard step with a valid default is not necessarily seen or confirmed. Preserve the intended initial reveal/confirmation interaction rather than automatically skipping it. During brief submit/loading transitions, observe the whole interaction in an active context; a library may restore inline styles between checkpoints. Do not add proxy submit controls to race the library. Stop before checkout/order/payment unless that operation has its own explicit authorization.
