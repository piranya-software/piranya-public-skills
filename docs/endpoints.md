# Public connector endpoints

Package inventories select these owner-requested canonical connection targets:

- Site management: `https://mcp.piranya.io/mcp/site-management`
- Reporting: `https://mcp.piranya.io/mcp/reporting`

These canonical endpoints are deployed. Authenticated host acceptance remains separate from deployment and depends on the host, account and installation. The canonical authorization-server issuer is `https://identity.piranya.io`; it is not the MCP endpoint or a substitute for host discovery. Package generation does not certify live reachability, availability, OAuth discovery or sign-in. No private values, release payloads or credentials are copied here.

Site management is a curated fixed toolset; reporting is excluded from it. A connector path is discovery selection, not an authorization boundary. The server independently enforces authorization and target delegation. Do not substitute `/mcp/all` silently.

For another public deployment or future product, supply a reviewed inventory with explicit concrete HTTPS URLs and fixed MCP paths. The builder does not guess a hostname, fetch discovery metadata, substitute environment placeholders or accept localhost/private literals. DNS ownership, public resolution and semantic appropriateness still require owner review; syntactic checking is not network verification. Non-MCP skills need no connector at all.
