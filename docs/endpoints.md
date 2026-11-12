# Public connector endpoints

Initial package inventories use these concrete production addresses:

- Site management: `https://mcpserver.prod.core.piranya.io/mcp/site-management`
- Reporting: `https://mcpserver.prod.core.piranya.io/mcp/reporting`

Sanitized source trace: the MCP GitOps ApplicationSet `clusters/core/shared/appsets/model-context-protocol-server.yaml` selects the production environment and production release file; its ingress host is `mcpserver.{{.metadata.labels.env}}.core.piranya.io` and its public HTTPS base URL uses that same host. The MCP server's maintained README surface table defines `/mcp/site-management` and `/mcp/reporting`. These addresses are configuration-derived, not a live reachability, availability or OAuth certification. No private values, release payloads or credentials are copied here.

Site management is a curated fixed toolset; reporting is excluded from it. A connector path is discovery selection, not an authorization boundary. The server independently enforces authorization and target delegation. Do not substitute `/mcp/all` silently.

For another public deployment or future product, supply a reviewed inventory with explicit concrete HTTPS URLs and fixed MCP paths. The builder does not guess a hostname, fetch discovery metadata, substitute environment placeholders or accept localhost/private literals. DNS ownership, public resolution and semantic appropriateness still require owner review; syntactic checking is not network verification. Non-MCP skills need no connector at all.
