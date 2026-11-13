# Piranya site management

For website editors and catalog managers maintaining a Piranya site through an AI assistant. Includes site editing and catalog management skills: inspect content and dependencies, make bounded changes and verify the saved result.

## Access and target selection

The canonical connection address below is deployed. Authenticated acceptance depends on the host, account and selected installation.

Use a compatible AI host with remote HTTP MCP support and the Piranya site-management connection (`https://mcp.piranya.io/mcp/site-management`). Install the reviewed provider package through the host's supported workflow, then follow the host's sign-in flow with your authorized Piranya account. These files contain no credentials and grant no access. No local checkout, shell or employee privileges are required to use the skills.

Before work, the assistant checks session information and fresh deployment results and matches the intended site by identity and address. Resolve ambiguous targets before proceeding. The selected connection and target stay fixed; a development label does not prove a sandbox. Authentication expiry, missing permissions, denied target access and installation incompatibility are different blockers. Do not switch identity or bypass a denial.

## OAuth sign-in

Each user signs in with their own authorized Piranya account and consents through the host. The package supplies no shared account, fixed OAuth client ID, client secret or access token.

OpenAI packages explicitly declare OAuth on the MCP server in `mcp.json` with `extensions["com.openai"].auth.type: "oauth"` and `client.mode: "cimd"`. This prefers Client ID Metadata Documents, with host-policy DCR fallback; endpoints and scopes remain discoverable. It is a registration preference, not proof that this endpoint or host has completed OAuth.

Claude plugins retain the supported remote HTTP `.mcp.json` entry. Claude Code discovers OAuth from the server; after installing the plugin, open `/mcp`, select this connection and follow Authenticate in the browser. Claude's optional `oauth` configuration is for specific settings such as a pre-registered client or callback port, not an `auth.type` switch. No invented auth field or empty OAuth object is bundled to imply enforcement. For Claude hosts other than Code, use that host's supported connector sign-in workflow; Code validation does not establish Desktop acceptance.

Package validation does not certify every host or account. If tools are missing or the host labels the plugin desktop-only, verify that host's connection and authentication settings separately.

## Permissions and confirmation

Your account needs access to the selected site and permission for each requested operation. Reading site resources or catalog records does not authorize writes; write permission does not authorize deletion. The package supports both inspection and mutation, not a read-only connection or a grant of broader access.

An inspection request remains read-only. For changes, identify the exact resource and affected pages or records first. Confirm consequences outside the original request, including shared layouts, defaults, overwrites, removal and destructive media detachment. Separate read, write and delete consent. An unlinked preview is not private. Do not place orders or modify baskets to test styling without consent.

## What you can ask

- “Inspect the home page and tell me which shared layout controls its header. Do not change anything.”
- “Change the heading on the selected page, preserve its editor bindings and verify the saved text.”
- “Find this product, show its current localized description and propose a focused update.”
- “Update the approved category assignment and verify that unrelated assignments remain unchanged.”

Supported work includes page content and routing, shared layout, styles, assets, fonts and design settings, plus Products, Categories, localized content, prices, assignments and media through supported tools. The assistant reads current revisions, preserves unrelated content and reads back exact changes. Saved, attached/activated and rendered/editor-verified results are reported separately.

## Boundaries

This is not authority to publish unrelated content, update installations, delete resources or execute arbitrary APIs. Native editor and commerce behavior must be preserved. Catalog configuration is not a customer-specific quote, stock promise, shipping decision or proof of checkout availability. Unsupported fields, missing tools, stale revisions or uncertain lifecycle safety stop the change rather than triggering a raw endpoint workaround.

## Compatibility, support and license

Tool availability and installed-producer capabilities must be checked on the selected connection; installation does not promise compatibility with every site or host. OpenAI/portable packages use streamable HTTP; Claude plugins use HTTP. Offline package validation is not certification of host installation, authentication or live behavior.

[Source and build documentation](https://github.com/piranya-software/piranya-public-skills/blob/main/docs/maintenance.md) describes packaging and release gates. [Support](https://support.piranya.dk/) · [Service terms](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/terms-of-service.md) · [Privacy](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/privacy.md).

The skills, documentation and tooling are covered by the bundled [MIT license](https://github.com/piranya-software/piranya-public-skills/blob/main/LICENSE). The remote MCP service and service access are not licensed by this package; authentication, authorization and applicable service terms still apply.
