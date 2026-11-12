# Schema provenance and provider scope

`schemas/provenance.json` records exact downloaded bytes, source URLs and SHA-256 hashes. The official pinned files are:

| File | Official source | SHA-256 |
| --- | --- | --- |
| plugin.schema.json | https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883` |
| mcp.schema.json | https://agent-plugins.org/schemas/1.0.0/mcp.schema.json | `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb` |

Updates are deliberate maintenance: fetch from the official URL, inspect schema changes and references, update the byte hash, and rerun tests/host validation. Neither building nor testing downloads schemas. Source URLs are provenance, not permission for remote schema resolution.

Portable Agent Plugins 1.0.0 metadata uses `$schema`, `name`, `version`, `description` and optional `author.name` and `license: MIT`. Optional MCP configuration uses `$schema` and `mcpServers`, with entries containing only `type: streamable-http` and `url`. No credentials, headers, custom auth fields or invented provider fields are generated. The optional strict inventory object `openai_interface` is emitted only as `extensions["com.openai"]["interface"]` in OpenAI output, never Claude metadata. Arbitrary extension namespaces are not accepted. The official portable schema validates the envelope offline but assigns no semantics to extension contents; the builder separately validates the bounded interface contract below.

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

Claude's official documentation at https://code.claude.com/docs/en/plugins-reference documents `.claude-plugin/plugin.json`, standard root `skills/`, optional root `.mcp.json`, and host validation. Remote HTTP MCP transport is documented at https://code.claude.com/docs/en/mcp . Claude metadata here includes `name`, `version`, `description` and optional `author.name` and `license: MIT`; remote entries include `type: http` and `url`. Current package inventories identify the author as `Piranya`. The documented Claude `license` field accepts SPDX identifiers; this builder restricts it to MIT. Root LICENSE covers the public skills, documentation and tooling, not the remote MCP service or access rights. The local restricted metadata validation is not an official Claude JSON Schema. Authoritative host validation and authenticated runtime tests remain distinct release gates; manifest acceptance does not prove runtime behavior.
