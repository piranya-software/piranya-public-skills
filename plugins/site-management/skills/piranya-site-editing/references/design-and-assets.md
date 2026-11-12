# Design, assets and fonts

## Assets: bytes, references and membership differ

List existing assets/folders before uploading. Confirm the actual image composition and resolution, not just a plausible filename. A valid URL can point to an icon or unsuitable crop. Keep ownership and rights decisions with the user; do not make a private source public merely to make uploading easier.

`piranya.assets.upload` accepts a file name and exactly one of public `source_url` or `content_base64`, plus supported folder options. Prefer a user-approved public source URL when one already exists. For small supplied bytes, use the host's supported byte transfer, not invented base64. For larger nonpublic files, use `create_upload_ticket` only if the host supports direct file transfer. Follow the returned upload contract and required content type; never expose the single-use ticket in a report or shared document. If the host cannot transfer the bytes, explain the limitation and ask for an approved upload route instead of assuming a shell.

Overwrite is explicit and can affect shared usages. Inspect impact and obtain missing overwrite consent. After upload, verify the returned file identity and usable reference. Uploading does not attach a script/stylesheet, create Product media membership or register a Font. Do not claim a complete asset inventory when listing bounds or folder scope exclude files.

## Fonts

Use an approved font file and the current `workspace.create_font` schema; do not infer accepted file-type enum values from the extension. Registration references the uploaded file and creates a Font identity. An external CSS font import is not a registered Design System font. Inspect existing fonts first, register only when needed, map the font through the supported theme fields, and verify the active rendered family/weight. Preserve icon-font declarations when changing text typography.

## Tokens and active scope

Read `design_system.get_designer_values` for the intended domain/master/page/route/department context before choosing catalog keys. Reuse semantic tokens and inspect effective values and their sources; do not assume a token's name implies the desired brand value. Respect locked tokens and server value validation.

Inspect themes and scope rules before adding overrides. `preview_resolution` is a read-only resolution aid, not evidence of visual rendering or persisted activation. Theme/token updates require the exact `if_match_version`; obtain it from a fresh `get_theme` before each guarded update and reconcile conflicts. Scope rules have no equivalent optimistic version: read immediately before changing and check the result.

A theme alone is inactive until a matching scope rule binds it. Page/route-scoped rules outrank broader scopes regardless of priority and require supported audit fields such as reason and acting user identity. Never invent an identity or broaden scope to avoid a denied narrow operation. Review all affected contexts before activating a shared theme.

Verify persisted assignments, matching rules, effective resolved values, font mappings and rendered computed styles separately. If Design System access is unavailable, do not imply workspace access grants it. Offer a clearly disclosed, narrowly scoped CSS-only alternative only if it fits the user's authorized outcome; do not silently call it a theme change or bypass access controls.
