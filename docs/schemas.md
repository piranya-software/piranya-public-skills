# Schema provenance and provider scope

`schemas/provenance.json` records exact downloaded bytes, source URLs and SHA-256 hashes. The official pinned files are:

| File | Official source | SHA-256 |
| --- | --- | --- |
| plugin.schema.json | https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883` |
| mcp.schema.json | https://agent-plugins.org/schemas/1.0.0/mcp.schema.json | `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb` |

Updates are deliberate maintenance: fetch from the official URL, inspect schema changes and references, update the byte hash, and rerun tests/host validation. Neither building nor testing downloads schemas. Source URLs are provenance, not permission for remote schema resolution.

Portable Agent Plugins 1.0.0 metadata uses `$schema`, `name`, `version`, `description` and optional `author.name` and `license: MIT`. Optional MCP configuration uses `$schema` and `mcpServers`, with entries containing only `type: streamable-http` and `url`. No credentials, headers, custom auth fields or invented provider fields are generated.

Claude's official documentation at https://code.claude.com/docs/en/plugins-reference documents `.claude-plugin/plugin.json`, standard root `skills/`, optional root `.mcp.json`, and host validation. Remote HTTP MCP transport is documented at https://code.claude.com/docs/en/mcp . Claude metadata here includes `name`, `version`, `description` and optional `author.name` and `license: MIT`; remote entries include `type: http` and `url`. Current package inventories identify the author as `Piranya`. The documented Claude `license` field accepts SPDX identifiers; this builder restricts it to MIT. Root LICENSE covers the public skills, documentation and tooling, not the remote MCP service or access rights. The local restricted metadata validation is not an official Claude JSON Schema. Authoritative host validation and authenticated runtime tests remain distinct release gates; manifest acceptance does not prove runtime behavior.
