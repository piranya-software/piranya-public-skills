# Piranya Site Operations

Use this read-only connector to investigate issues, recorded job executions, logs and entity-change history on a Piranya installation you administer.

## Connect in Claude

1. In Claude’s connector settings, add a custom connector with `https://mcp.piranya.io/mcp/site-operations` as the remote MCP URL, or select Piranya Site Operations from the directory if listed.
2. Sign in through Piranya and authorize access. Operational reads require installation-wide administrator access; a department- or account-only context is not sufficient.
3. Ask Claude to list your authorized Piranya installations. Select the intended installation before requesting operational evidence. If it is missing or access is denied, check your account and permissions with your Piranya administrator.

## Try a read

- “Summarize the issues reported for my selected installation. Distinguish reported findings from checks that could not establish a result.”
- “For the job I name, show recent recorded executions and identify the most recent failure in the results. Include its status and timestamps.”
- “Summarize the recorded change metadata for this record. Separate what the history shows from what it cannot explain.”

Results can be limited by the selected filters, paging and retained history. A missing result does not prove nothing happened. This connector cannot run or retry jobs, resolve issues, or change installation settings. Request only the evidence you need: logs and diagnostics can contain personal or confidential information. Never paste credentials into a conversation.

[Support](https://support.piranya.dk/) · [Privacy](../legal/privacy.md) · [Terms](../legal/terms-of-service.md)
