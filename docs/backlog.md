# Release requirements

- Public suitability review, and explicit authorization for visibility, publication, commits/pushes and listing submission.
- Authenticated OpenAI and Claude host installation, OAuth, discovery and consent-boundary acceptance; Claude strict host validation. Offline schema checks do not satisfy these gates.
- Pin reviewed source and builder commits for release; local content locks support uncommitted initial snapshots only as non-release artifacts.
- Extend explicit per-skill file lists when supporting references are authored; no recursive directory inclusion.
- Internal package host acceptance and source-transition verification belong to the internal repository; public output must never consume internal inputs.

## Acceptance evidence still required

- Run bundled synthetic scenarios in actual hosts. Record package content identity, surface, activation, tool discovery, consent controls and omissions; static schema checks are not behavioral results.
- Verify inline editor markup and native interactions against an approved compatible target; source-document comparison does not establish installed or rendered behavior.
- Prepare approved listing copy, support/privacy links, domain ownership and publisher metadata against current provider requirements. Do not invent contact URLs, legal policy or publishing identity.
- Define a synthetic reviewer dataset and least-privilege account procedure; provisioning and credential delivery need separate authority. Never put reviewer credentials in source or ZIPs.
- Confirm connector registration/submission requirements separately from plugin packaging before authorized submission.

## Foundation extensions

- Maintain successful clean-commit release-gate regression coverage in the suite; correction review exercised this separately in disposable Git fixtures.
- Exercise native symlink/reparse rejection on a privileged test host. Mocked checks do not certify every filesystem mechanism.
- Add binary/script resources only with explicit inventory, executable-content, size and portability checks. Current packages deliberately support text resources only.
