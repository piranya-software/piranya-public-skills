# Rendering diagnostics and native layout

## Follow source to paint

1. Identify the requested route's actual master page, attachments and stylesheet order. Read current source and revisions before diagnosing; saved source, generated CSS, loaded CSS and final paint are four separate checks.
2. Inspect the generated stylesheet URL actually linked by the page through an available authorized browser/read surface. Check compiler error comments and expected selectors from every changed resource. Mixed-unit SASS evaluation of native CSS functions and colon-bearing utility selectors can invalidate or omit rules. Use supported syntax with the same intended semantics; never treat a successful save as compilation success.
3. Inspect the loaded CSSOM, matching selectors and computed properties on the real element. Include global/native rules, media/supports/layer blocks, imports when accessible, and nested style rules. Check a rule's own selector AND its nested rules; these are not mutually exclusive. Report inaccessible sheets, not an exhaustive negative result. Source absence in a local resource alone does not prove global origin.
4. Resolve the cascade per property: origin/importance, specificity (including type selectors), and source order. Find all competitors, not just the first. Audit the full native declaration set, including position/insets, float/clear, flex, min/max sizes, overflow and opacity. An undeclared property remains uncontested; a later ordinary rule cannot cancel an earlier important declaration. Prefer scoped sufficient selectors; use important overrides only for a demonstrated requirement, not a blanket reset.
5. Verify paint in an active, visible browser context. Hover, transitions and screenshots can be stale or suspended in hidden/background contexts. If paint and computed styles disagree, inspect both pseudo-elements, selector matches, loaded rules and hit-tested layers before blaming the browser. Reproduce in a fresh active context; do not preserve hostname-specific or historical tool observations as universal defects. Retained console messages alone do not establish a current error.

If source is correct but generated output remains stale, report the observed boundary and use a documented supported refresh/recompile operation if available. Do not add dummy newlines, placeholder changes, cache-busting live edits or unrelated saves to trigger invalidation. No arbitrary endpoint probing is authorized by diagnosis.

## Measure the actual component

- Capture bounding rectangles, computed layout and scrollWidth/clientWidth on the affected element and ancestors at relevant desktop/mobile widths. Use hit testing at the bad pixel for overlapping ancestor chrome; walk overflow ancestors for clipped content. Preserve load-bearing dialog scrolling rather than disabling overflow to achieve decorative bleed.
- Inspect the width available to each component instance, not only the viewport. A sidebar and main grid can render the same card at different widths simultaneously; container-based adaptation may be more appropriate than a viewport breakpoint.
- Check real longest labels, multi-line text, icons and largest expected numeric values. A number that fits at a small value can clip at a larger value. Font metrics and actual clamped-row heights must be measured, not inferred from line-height alone.
- Reset competing float/clear, width, flex-shrink and minimum sizes deliberately when adopting flex/grid. Changing display alone does not remove float shrink-to-fit. A winning width does not cancel a separate min-width constraint. A fixed image height can cap responsive card growth.
- Align rows by understanding every variable track: a flexible spacer before trailing variable content transmits that variability upward. Every auto-sized title/description row above an alignment spacer can independently break alignment. Use explicit tracks/placement only after verifying the real child set across variants. Optional direct children need conditional templates rather than empty implicit rows; reset desktop grid placement at narrow breakpoints so implicit columns cannot survive.
- After float-to-grid or order changes, compare rendered order with DOM order; do not diagnose an unexplained observation as a general browser reordering rule. Avoid applying a second column grid around a native widget already managing its own columns.
- Measure the complete current sticky header at scroll time, including secondary rows. Hit-test scrolled controls for occlusion. Sticky content needs enough containing-block height to travel; fixed descendants are constrained by transformed ancestors. Avoid moving native controls to escape that constraint without inspecting their ancestry contracts.

## Legacy page positioning and floats

For authored CSS-layout sections, set `piranya:allowchildreposition="false"` on the section itself. Legacy positioning can otherwise turn explicitly sized direct children into floats with computed margins, collapsing block parents and overlapping following content. Flex/grid may mask the injected float without removing the underlying mechanism.

The Platform-owned page-root wrapper is different: it is not an authored section where that attribute can be added. Avoid explicit inline width/height on the page's own top-level elements; these can trigger repositioning of all root children. Put necessary sizing on nested authored wrappers only after checking their actual flex/grid parent. Verify computed float on root children, root height and the next master-page element's boundary (usually the footer).

For other native float containers, compare parent height with descendant/scroll height. Use a suitable float-containing layout or clearfix where compatible; do not hide overflow merely to mask collapse, since popovers and badges may need to escape.

## Author for the next editor

Keep HTML one element per line with nested indentation, text on its element's line, CSS one declaration per line and scripts one statement per line. Comments default to none and, when needed, explain one non-obvious constraint briefly; no source-prototype references, debug narratives or customer feedback in live resources.

Organize recurring CSS by concern (base, navigation, footer, forms, native commerce components) rather than one growing resource. When a touched resource becomes difficult to navigate, propose a bounded authorized split. Extract complete rules, preserve attachment/cascade order, remove the original duplicate only after the new attachment is verified, and compare rendering before functional edits. Sequence these dependent operations; never parallelize removal and addition or broaden a local edit into an unapproved refactor. Re-read patch insertions with both neighboring rules: finding a selector alone does not prove surrounding braces or compilation remain valid.
