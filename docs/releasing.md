# Same-repository distribution

Canonical authoring lives only in `skills/`; edit explicit `packages/*.json` inventories when membership changes. Never edit `plugins/` copies. `tools/distribute.py` uses the existing `pack.py` API without changing that builder or its internal consumers.

```sh
python -m pip install -r tools/requirements.txt
python -m unittest discover -s tests -v
python tools/distribute.py
python tools/distribute.py --check
```

Generation captures each explicit inventory and selected inputs, creates an in-memory content lock, and builds both providers from that same capture. It writes versioned Claude manifests, MCP configuration, skills and `package-inputs.json` under `plugins/site-management/` and `plugins/reporting/`, plus four ignored `dist/{site-management,reporting}-{claude,openai}.zip` files. No local build locks are packaged or required. `package-inputs.json` includes the existing builder/schema and selected-source hashes, not a self-referential source commit. Source and generated trees belong in the same reviewed commit.

`--check` never writes: it rebuilds in temporary storage and compares exact generated-tree bytes and membership. Unexpected files and empty directories fail; linked/reparse output paths fail. Ignored ZIPs are verified when present but need not exist in a fresh checkout. Generation refuses unexpected plugin members rather than deleting them. Only the two plugin trees and four named ZIP targets are managed; other dist files are untouched. Remove obsolete generated members explicitly after reviewing inventory changes, then regenerate. Selected text is normalized to LF for Git checkout EOL independence; `.gitattributes` keeps builder/schema hashes stable. ZIP entries retain the existing deterministic ordering, timestamps and modes.

## Approval gates

The owner selected public distribution from this repository, not a dedicated distribution repository. **Do not change visibility until the complete Git history and current candidate have been cleared for public use, including consent to Git author metadata exposure.** Local tests, scans and CI cannot provide semantic privacy clearance. No license is selected; that decision gates marketplace/directory distribution terms, not an otherwise authorized repository commit or visibility change. This tooling neither chooses a license nor grants publication approval.

Commit reviewed source and generated artifacts together within the owner's repository publication authorization. Marketplace release tagging and submission separately require approved licensing/distribution terms, actual-host acceptance and explicit release authority. No tool or CI job here creates tags, releases, uploads or changes visibility. Verify the release checkout and independently pin the builder/dependencies; rebuild ZIPs at that approved tag and retain their SHA-256 values. Existing `pack.py --release-commit` can separately verify a clean source-commit-pinned candidate; distribution does not put that commit into its own generated output.

## Consumer updates

Claude consumers must select the reviewed release tag and the specific `plugins/site-management` or `plugins/reporting` path using their host's supported plugin installation workflow. Validate each unpacked plugin with `claude plugin validate <directory> --strict` and exercise authentication, discovery and consent boundaries in the actual host. OpenAI consumers use the corresponding OpenAI ZIP built from that same tag and must verify actual host acceptance. Offline validation is not host certification. Do not treat `main` as an automatic deployment channel; updates require an explicit reviewed tag/ZIP refresh.

An arbitrary MCP backend can change independently of these pinned skill/plugin files. Pinning distribution content does not pin backend implementation or authorize new tools. Automatic backend or repository scans are independent checks, not deployment approval or a substitute for human privacy/history review.
