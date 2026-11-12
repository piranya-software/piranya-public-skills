# Guarded changes and uncertain outcomes

## Read, patch, preserve

Resolve aliases to canonical paths when supported. Read the relevant current lines plus enough context to understand template boundaries. A truncated read is not the whole resource. `expected_revision` is opaque: preserve it exactly and bind it to the resource read.

`patch_file` operations use 1-indexed inclusive `start_line`/`end_line`, exact `expected_text`, and `replacement_text`. Join the expected lines with newlines, without a trailing newline. Any mismatch rejects the whole patch. Insert with `end_line = start_line - 1` and empty expected text; delete with empty replacement text. A block move can combine deletion and insertion in one patch; follow the discovered operation-order contract, not guessed shifted line numbers.

`write_file` replaces the complete resource. Use it for an intentional full rewrite, never for a diff, truncated excerpt or placeholder-filled draft. Inspect the complete replacement for missing bindings, editor IDs and unrelated content before sending.

Master-page content and head can share revision metadata. Read head again after changing content before editing head. Sequence related mutations rather than parallelizing operations that may invalidate one another's guards. Keep enough original content within the user's approved private working context to propose recovery; do not put customer source into shared examples.

## Relations and deletion

Inspect master-page usages and current attached script/stylesheet order. Attach only absent resources; reorder an existing relation instead of detaching and recreating it. Omitted attach ordinal appends; later stylesheet ordinals merge later and win at equal specificity, not against every stronger CSS rule. Read back order and unaffected siblings.

Before deleting, confirm the exact destructive scope, fresh revision and dependency consequences. A workspace delete does not promise relation cleanup or safe cascades. Detaching a relation is different from deleting its resource. Do not remove shared resources to make a page-local task easier.

## Recovery decision table

| Observation | Action | Do not claim |
|---|---|---|
| Revision or expected-text mismatch | Re-read, reconcile intended edit, retry only the still-authorized change | That the old payload is safe with a new token |
| Timeout/disconnect during write or create | Read the exact target; check existing resources before retrying creation | Failure means nothing changed |
| Save succeeds, readback fails | Report saved acknowledgment and unknown persisted state; reconcile before another mutation | Verified completion |
| Source is correct but appearance is wrong | Check attachment, active scope, route/master selection and computed styles; investigate cache only with evidence | Another overwrite will fix it |
| Access denied in one family | Inspect the returned authorization diagnostic and available session scope | Other working tools prove this family is authorized |
| Generic API error | Preserve sanitized error context and stop unsupported mutation attempts | A reconnect or installation update is necessarily required |

Rendered validation should be proportional. A local text change needs a targeted check, not a full redesign audit. A structural change needs viewport, navigation and relevant native-component checks. If no rendering/editor tool is available, return the exact limitation and do not relabel source verification as visual acceptance.
