# Piranya reporting

For business users analyzing Piranya sales, period comparisons, fees and rebates through an AI assistant. Includes the sales reporting skill for bounded, read-only analysis with explicit scope and interpretation limits.

## Access and target selection

The canonical connection address below is deployed. Authenticated acceptance depends on the host, account and selected installation.

Use a compatible AI host with remote HTTP MCP support and the Piranya reporting connection (`https://mcp.piranya.io/mcp/reporting`). Install the reviewed provider package through the host's supported workflow, then follow the host's sign-in flow with your authorized Piranya account. These files contain no credentials and grant no access. No local checkout, shell or employee privileges are required to use the skills.

Before work, the assistant checks session information and fresh deployment results and matches the intended site by identity and address. Resolve ambiguous targets before proceeding. The selected connection and target stay fixed; a development label does not prove a sandbox. Authentication expiry, missing permissions, denied target access and installation incompatibility are different blockers. Do not switch identity or bypass a denial.

## OAuth sign-in

Each user signs in with their own authorized Piranya account and consents through the host. The package supplies no shared account, fixed OAuth client ID, client secret or access token.

OpenAI packages explicitly declare OAuth on the MCP server in `mcp.json` with `extensions["com.openai"].auth.type: "oauth"` and `client.mode: "cimd"`. This prefers Client ID Metadata Documents, with host-policy DCR fallback; endpoints and scopes remain discoverable. It is a registration preference, not proof that this endpoint or host has completed OAuth.

Claude plugins retain the supported remote HTTP `.mcp.json` entry. Claude Code discovers OAuth from the server; after installing the plugin, open `/mcp`, select this connection and follow Authenticate in the browser. Claude's optional `oauth` configuration is for specific settings such as a pre-registered client or callback port, not an `auth.type` switch. No invented auth field or empty OAuth object is bundled to imply enforcement. For Claude hosts other than Code, use that host's supported connector sign-in workflow; Code validation does not establish Desktop acceptance.

Package validation does not certify every host or account. If tools are missing or the host labels the plugin desktop-only, verify that host's connection and authentication settings separately.

## Permissions and read-only scope

Your account needs reporting access to the selected site and the departments included in the question. Available tools and authorized departments are checked through current capabilities. Filters narrow a request; they never grant access. A selected-department request requires an actual selected department. A truncated department list does not prove that an omitted department is absent or denied.

This workflow reads business reports. It does not modify orders or other business data, change identity, certify accounts or authorize arbitrary report execution. No write or delete consent is implied by a reporting request.

## What you can ask

- “Show sales for last month in the site's business time zone, grouped by product and separated by currency.”
- “Compare this period with the previous period, if the installed reporting capabilities support it.”
- “Analyze lost-sales statuses for the selected department, explaining the effective status scope.”
- “Summarize supported fees and rebates, keeping incompatible reporting grains separate.”
- “Show expected delivery/pickup demand by weekday and hour, if supported; distinguish it from placed sales.”
- “Show a chronological 15-minute, 30-minute or hourly demand series in the business zone, if supported.”

The reviewed report is `sales-breakdown`. Establish the exact period, time zone, currencies, department scope, measures and status scope before running it. The assistant reports returned window boundaries, filters, units, totals and paging limitations. Live pages are not a snapshot; repeated page totals must not be added, and currencies must not be silently combined.

## Compatibility and limits

Comparison requires advertised support and cannot combine with time grouping. Language selection requires report revision 5 or later. Fee and rebate analysis requires revision 6 or later plus the advertised measures and compatible grain; revision alone is insufficient. Explicit timestamp selection requires report revision 7 or later and matching source metadata. Expected fulfillment uses the current expected delivery/pickup time, excludes missing expectations and is not actual fulfillment. Recurring ISO weekday/hour grouping and chronological subday intervals require revision 8 or later plus their exact advertised metadata/options; supported minute sizes are 15 and 30, hourly size is 1. Recurring groups aggregate occurrences, not a chronological series or per-occurrence average. The production connector runs MCP 0.20.0; target installation capabilities still determine which reporting selections are available. Unsupported criteria must not be silently dropped. Periods are bounded to 366 days and rows are paged; incomplete traversal is disclosed.

Arbitrary exports, download tickets, CSV URLs, filesystem paths and invented attachments have no approved delivery contract in this workflow. Do not promise them. Newly advertised reports, routes or schemas do not authorize execution. A failed or denied report is not evidence of zero sales.

## Compatibility, support and license

Tool availability and installed-producer capabilities must be checked on the selected connection; installation does not promise compatibility with every site or host. OpenAI/portable packages use streamable HTTP; Claude plugins use HTTP. Offline package validation is not certification of host installation, authentication or live behavior.

[Source and build documentation](https://github.com/piranya-software/piranya-public-skills/blob/main/docs/maintenance.md) describes packaging and release gates. [Support](https://support.piranya.dk/) · [Service terms](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/terms-of-service.md) · [Privacy](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/privacy.md).

The skills, documentation and tooling are covered by the bundled [MIT license](https://github.com/piranya-software/piranya-public-skills/blob/main/LICENSE). The remote MCP service and service access are not licensed by this package; authentication, authorization and applicable service terms still apply.
