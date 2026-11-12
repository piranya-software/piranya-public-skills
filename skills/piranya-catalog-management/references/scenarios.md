# Synthetic review scenarios

These are invented reasoning cases, not live acceptance or host evaluation. IDs must be freshly discovered from the authorized target when actually operating; no fixture identity authorizes a mutation.

| Case | Setup / request | Expected observable actions | Negative control / boundary |
|---|---|---|---|
| First price | Existing Product has no price; user requests a base price | Fresh capabilities/profile; explicit `action: "add"`; resolve currency/VAT/quantity intent; explicit null base applicability; readback new and retained rows | No duplicate Product, guessed currency or availability claim |
| Existing localized title | One language title needs correction | Read profile; retain returned localization ID; partial field update with both revisions; readback unrelated localizations | No localization collection replacement |
| Category with descendants | Find Products in a selected Category | Resolve Category; category selector with default descendants; explain OR for multiple selections; page if completeness required | Do not use dotted paths or claim AND semantics |
| Direct-only request | User explicitly excludes child Categories | Send `include_sub_categories: false` with category selection | Do not silently restore default true |
| Hidden inactive record | Generic search returns no match | Deliberate status selectors and exact identity/profile confirmation | No declaration of absence from an ordinary active/nonhidden listing |
| Stale profile | Another editor changes Product before save | Re-read/reconcile fields and keys before new guarded update | No claim that preflight prevents every concurrent race |
| Truncated media | Profile flags relevant media as truncated | Obtain sufficient supported reads or stop membership-wide operation with limitation | Do not treat absent rows as deleted or empty |
| Unsafe detach | Shared attachment flag is null or target lifecycle safety unknown | Stop detach, explain delete-scope/flag/lifecycle gates | Do not flip flag, raw-delete File or experiment on customer content |
| Reorder drift | Attach returns a different ordinal and reindexed siblings | Inspect refreshed order; use owned relation reorder if supported and needed; readback siblings | Do not report exact requested ordinal from success alone |
| Acknowledged update, refresh failed | `updated: true` and `profile_refresh_error` | Read exact Product before any replay; distinguish acknowledgment from verification | No automatic duplicate addition |
| Unsupported membership | User asks to add a localization through update | Explain unsupported membership operation and offer supported administration path if available | Do not infer write permission from dynamic schema |
| Campaign mismatch | Category search omits campaign-only membership | Explain native campaign applicability and search boundary | Do not claim membership equals customer purchase eligibility |

Where installed keyed merge or deletion lifecycle compatibility is unestablished, a static schema or synthetic fixture does not close that gate. Review cases require explicit compatibility limits, not live mutation experiments.
