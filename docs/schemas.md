# Schema provenance and provider scope

`schemas/provenance.json` records exact downloaded bytes, source URLs and SHA-256 hashes. The official pinned files are:

| File | Official source | SHA-256 |
| --- | --- | --- |
| plugin.schema.json | https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883` |
| mcp.schema.json | https://agent-plugins.org/schemas/1.0.0/mcp.schema.json | `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb` |

Updates are deliberate maintenance: fetch from the official URL, inspect schema changes and references, update the byte hash, and rerun tests/host validation. Neither building nor testing downloads schemas. Source URLs are provenance, not permission for remote schema resolution.

Portable Agent Plugins 1.0.0 metadata uses `$schema`, `name`, `version`, `description` and optional `author.name` and `license: MIT`. Optional MCP configuration uses `mcpServers` with `type: streamable-http` and `url`. It always includes the required Agent Plugins `$schema` format marker, including with selected provider auth. OpenAI OAuth output follows the separately documented provider extension below; it does not claim conformance to the portable MCP schema. No credentials, headers or invented provider fields are generated. The optional strict inventory object `openai_interface` is emitted only as `extensions["com.openai"]["interface"]` in OpenAI output, never Claude metadata. Arbitrary extension namespaces are not accepted. The official portable schema validates the envelope offline but assigns no semantics to extension contents; the builder separately validates the bounded interface contract below.

## Bounded OpenAI OAuth

[OpenAI's package authentication reference](https://developers.openai.com/plugins/build/plugins#oauth-configuration-reference) places authentication at each `mcpServers.<name>.extensions["com.openai"].auth` in `mcp.json`, not in the plugin manifest's interface. Optional inventory `openai_auth` maps only declared connector names to `{ "type": "oauth" }`, optionally with `"client": { "mode": "cimd" }`. Omission of `client` leaves registration to host discovery; `auto` is not a documented manifest mode. Both offering inventories explicitly prefer CIMD. OpenAI documents DCR fallback for CIMD preference; this does not prove live server support or user sign-in.

This builder rejects all other auth types, fields and client modes, fixed client IDs, secrets, endpoint/scope overrides, unknown connector names and arbitrary extensions. The inventory is captured and hash-bound through the existing builder path, including for Claude; only OpenAI emits this auth extension. Existing listing interface and Claude icon remain separate.

The current official Agent Plugins 1.0.0 MCP schema still rejects server `extensions` (`additionalProperties: false`); its downloaded bytes match the pinned hash above. It is not edited or represented as supporting OpenAI's extension. The builder retains root `$schema: "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"` as the required format marker documented by OpenAI, including with OAuth. It validates a copy with server extensions removed against the unchanged pinned portable schema and validates each extension separately against a strict bounded OpenAI overlay. Unknown namespaces, wrapper fields and auth fields fail. This layered check is not full portable-schema validation of the extended document. Full extended-document OpenAI host acceptance remains a separate gate.

## Claude OAuth discovery

[Claude's remote authentication documentation](https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers) describes server challenges and `/mcp` browser sign-in. Its [pre-configured credentials reference](https://code.claude.com/docs/en/mcp#use-pre-configured-oauth-credentials) documents automatic DCR and CIMD discovery plus optional `oauth` settings, not an `auth.type: oauth` declaration. The installed Claude Code 2.1.293 HTTP configuration schema also has optional `oauth` settings (`clientId`, `callbackPort`, `authServerMetadataUrl`, `scopes`, `xaa`), with no auth-type/enable switch. An empty `oauth` object supplies no meaningful setting and is not used as a false OAuth-required declaration.

Claude packages therefore retain only `type: http` and `url` for remote MCP connections. Supported OAuth setup is documented in each bundled product guide, without fixed client identity or secrets. No explicit OAuth-required switch for this remote plugin format is established by these contracts; OAuth discovery is the supported convention. Strict CLI validation is not authenticated acceptance, Desktop certification or proof that host tool visibility/classification changes.

## Bounded OpenAI interface

[OpenAI listing rules](https://developers.openai.com/plugins/deploy/submission-errors) define the final-directory bounds used here, rather than the looser package limits. `openai_interface` is optional; its known fields are optional so partial metadata does not imply submission readiness. Missing metadata remains absent. Unknown fields fail for either provider.

| Field | Builder rule |
| --- | --- |
| displayName, shortDescription | Nonblank single line, at most 30 characters each |
| longDescription | Nonblank, at most 4,000 characters; LF line breaks allowed |
| developerName | Nonblank single line, at most 80 characters |
| category | Productivity, Creativity, Developer Tools, Business & Operations, Data & Analytics, Communication, Education & Research, Security, Finance, Healthcare, Travel, Entertainment, Other |
| websiteURL, supportURL, privacyPolicyURL, termsOfServiceURL | At most 1,024 characters; concrete public-DNS HTTPS URL; no credentials, query, fragment, private/placeholder hostname, nonstandard port or unsafe path |
| defaultPrompt | String or array of at most three strings, each nonblank, single line and at most 128 characters; unique after NFKC/whitespace normalization; no @mentions |

Control/format characters are rejected. Inventory metadata is hash-bound, including for Claude builds even though Claude manifests omit it; metadata changes require explicit lock review. `logo` and `composerIcon` accept only package-relative `./assets/<selected-name>.png` references to explicitly selected, validated PNG artwork; see the [binary packaging contract](packaging.md). Both providers carry the selected exact bytes, but only OpenAI emits these interface fields. Terms must remain absent unless an approved service terms URL is selected. See [listing readiness](releasing.md#listing-readiness) for independent release gates.

Claude's official documentation at https://code.claude.com/docs/en/plugins-reference documents `.claude-plugin/plugin.json`, standard root `skills/`, optional root `.mcp.json`, and host validation. Remote HTTP MCP transport is documented at https://code.claude.com/docs/en/mcp . Claude metadata here includes `name`, `version`, `description` and optional `author.name` and `license: MIT`; remote entries include `type: http` and `url`. Current package inventories identify the author as `Piranya`. The documented Claude `license` field accepts SPDX identifiers; this builder restricts it to MIT. Root LICENSE covers the public skills, documentation and tooling, not the remote MCP service or access rights. The official [directory listing fields](https://code.claude.com/docs/en/plugins-reference#directory-listing-fields) document `icon` as a plugin-relative image path read by Anthropic’s directory, not by Claude Code at load time. The builder accepts only optional `claude_icon: "./assets/<selected-name>.png"`, emits it as manifest `icon` only for Claude, and requires an explicitly selected validated PNG. Unknown provider fields and arbitrary image paths remain rejected. The local restricted metadata validation is not an official Claude JSON Schema. Authoritative host validation and authenticated runtime tests remain distinct release gates; manifest acceptance does not prove runtime behavior.
