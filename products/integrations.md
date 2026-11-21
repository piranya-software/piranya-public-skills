# Piranya Integrations

Use this read-only connector to discover what your configured Piranya integrations can read and retrieve specific source records. Available operations depend on the integration and installation.

## Connect in Claude

1. In Claude’s connector settings, add a custom connector with `https://mcp.piranya.io/mcp/integrations` as the remote MCP URL, or select Piranya Integrations from the directory if listed.
2. Sign in through Piranya and authorize access. You need installation-wide administrator access and an enabled, configured integration that supports reads. A department- or account-only context is not sufficient.
3. Obtain the deployment target ID for the intended installation. This connector does not list installations itself. Use an authorized Piranya Core connection at `https://mcp.piranya.io/mcp` and ask it to list your authorized installations using `piranya.deployments.list`. Select the matching installation and use its returned `target_id` with Integrations. If you cannot connect Core or the installation is not listed, ask your Piranya administrator for help. Do not substitute a site URL or an integration instance ID.

## Try a read

- “For the selected installation, list the configured integrations that support reading data and tell me what operations they offer.”
- “If the configured integration supports it, look up the product I specify and summarize what the source returns.”

Discover the reader and its available operations before requesting a record. Results reflect what the selected source returned for that request; they do not establish complete or historical coverage. If the source returns a continuation cursor, more results may be available. An unavailable or failed read is not an empty result.

This connector cannot configure integrations, synchronize systems, submit or change orders, or write back to connected services. Ask only for records you are authorized to share with your AI provider. Never paste credentials into a conversation.

[Support](https://support.piranya.dk/) · [Privacy](../legal/privacy.md) · [Terms](../legal/terms-of-service.md)
