# Piranya reporting

For business users analyzing Piranya sales, period comparisons, fees and rebates through an AI assistant. Includes the sales reporting skill for bounded, read-only analysis with explicit scope and interpretation limits.

## Access and target selection

Use a compatible AI host with remote HTTP MCP support and the Piranya reporting connection (`https://mcpserver.prod.core.piranya.io/mcp/reporting`). Install the reviewed provider package through the host's supported workflow, then follow the host's sign-in flow with your authorized Piranya account. These files contain no credentials and grant no access. No local checkout, shell or employee privileges are required to use the skills.

Before work, the assistant checks session information and fresh deployment results and matches the intended site by identity and address. Resolve ambiguous targets before proceeding. The selected connection and target stay fixed; a development label does not prove a sandbox. Authentication expiry, missing permissions, denied target access and installation incompatibility are different blockers. Do not switch identity or bypass a denial.

## Permissions and read-only scope

Your account needs reporting access to the selected site and the departments included in the question. Available tools and authorized departments are checked through current capabilities. Filters narrow a request; they never grant access. A selected-department request requires an actual selected department. A truncated department list does not prove that an omitted department is absent or denied.

This workflow reads business reports. It does not modify orders or other business data, change identity, certify accounts or authorize arbitrary report execution. No write or delete consent is implied by a reporting request.

## What you can ask

- “Show sales for last month in the site's business time zone, grouped by product and separated by currency.”
- “Compare this period with the previous period, if the installed reporting capabilities support it.”
- “Analyze lost-sales statuses for the selected department, explaining the effective status scope.”
- “Summarize supported fees and rebates, keeping incompatible reporting grains separate.”

The reviewed report is `sales-breakdown`. Establish the exact period, time zone, currencies, department scope, measures and status scope before running it. The assistant reports returned window boundaries, filters, units, totals and paging limitations. Live pages are not a snapshot; repeated page totals must not be added, and currencies must not be silently combined.

## Compatibility and limits

Comparison requires advertised support and cannot combine with time grouping. Language selection requires report revision 5 or later. Fee and rebate analysis requires revision 6 or later plus the advertised measures and compatible grain; revision alone is insufficient. Unsupported criteria must not be silently dropped. Periods are bounded to 366 days and rows are paged; incomplete traversal is disclosed.

Arbitrary exports, download tickets, CSV URLs, filesystem paths and invented attachments have no approved delivery contract in this workflow. Do not promise them. Newly advertised reports, routes or schemas do not authorize execution. A failed or denied report is not evidence of zero sales.

## Compatibility, support and license

Tool availability and installed-producer capabilities must be checked on the selected connection; installation does not promise compatibility with every site or host. OpenAI/portable packages use streamable HTTP; Claude plugins use HTTP. Offline package validation is not certification of host installation, authentication or live behavior.

[Source and build documentation](https://github.com/piranya-software/piranya-public-skills/blob/main/docs/maintenance.md) describes packaging and release gates. [Support](https://support.piranya.dk/) · [Service terms](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/terms-of-service.md) · [Privacy](https://github.com/piranya-software/piranya-public-skills/blob/main/legal/privacy.md).

The skills, documentation and tooling are covered by the bundled [MIT license](https://github.com/piranya-software/piranya-public-skills/blob/main/LICENSE). The remote MCP service and service access are not licensed by this package; authentication, authorization and applicable service terms still apply.
