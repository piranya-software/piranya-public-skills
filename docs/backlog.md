# Release requirements

- Review public suitability of each candidate and obtain explicit authorization for publication, commits/pushes and listing submission; the source repository is already public.
- Authenticated OpenAI and Claude host installation, OAuth, discovery and consent-boundary acceptance; Claude strict host validation. Offline schema checks do not satisfy these gates.
- Pin reviewed source and builder commits for release; local content locks support uncommitted initial snapshots only as non-release artifacts.
- Extend explicit per-skill file lists when supporting references are authored; no recursive directory inclusion.
- Internal package host acceptance and source-transition verification belong to the internal repository; public output must never consume internal inputs.

## Acceptance evidence still required

- Run bundled synthetic scenarios in actual hosts. Record package content identity, surface, activation, tool discovery, consent controls and omissions; static schema checks are not behavioral results.
- Verify inline editor markup and native interactions against an approved compatible target; source-document comparison does not establish installed or rendered behavior.
- Review the available bounded listing metadata against current provider requirements; it is not submission completion. Confirm publisher/domain ownership, current provider acceptance of the approved service terms and privacy URLs.
- Define a synthetic reviewer dataset and least-privilege account procedure; provisioning and credential delivery need separate authority. Never put reviewer credentials in source or ZIPs.
- Confirm connector registration/submission requirements separately from plugin packaging before authorized submission.

## Foundation extensions

- Maintain successful clean-commit release-gate regression coverage in the suite; correction review exercised this separately in disposable Git fixtures.
- Exercise native symlink/reparse rejection on a privileged test host. Mocked checks do not certify every filesystem mechanism.
- Additional binary formats and scripts require a separately reviewed inventory, executable-content, size and portability contract. Only explicitly selected bounded PNG artwork is supported alongside text resources.
