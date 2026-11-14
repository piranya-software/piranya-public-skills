# Same-repository distribution

Canonical skill authoring lives in `skills/` and product documentation in `products/`; edit explicit `packages/*.json` inventories when membership changes. Never edit `plugins/` copies. `tools/distribute.py` uses the `pack.py` API and preserves its explicit input selection. Licensed inventories select root `LICENSE`; generation carries it into both provider ZIPs and each Claude tree. Each offering explicitly selects `readme_file: "products/<offering>.md"`, emitted as root `README.md` in both ZIPs and the Claude tree. Edit only the canonical product document, never generated READMEs.

```sh
python -m pip install -r tools/requirements.txt
python -m unittest discover -s tests -v
python tools/distribute.py
python tools/distribute.py --check
```

Generation captures each explicit inventory and selected inputs, creates an in-memory content lock, and builds both providers from that same capture. It writes versioned Claude manifests, MCP configuration, skills and `package-inputs.json` under `plugins/site-management/` and `plugins/reporting/`, plus four ignored `dist/{site-management,reporting}-{claude,openai}.zip` files. No local build locks are packaged or required. `package-inputs.json` includes the existing builder/schema and selected-source hashes, not a self-referential source commit. Source and generated trees belong in the same reviewed commit.

`--check` never writes: it rebuilds in temporary storage and compares exact generated-tree bytes and membership. Unexpected files and empty directories fail; linked/reparse output paths fail. Ignored ZIPs are verified when present but need not exist in a fresh checkout. Generation refuses unexpected plugin members rather than deleting them. Only the two plugin trees and four named ZIP targets are managed; other dist files are untouched. Remove obsolete generated members explicitly after reviewing inventory changes, then regenerate. Selected PNG assets retain exact binary bytes; only selected text is normalized to LF for Git checkout EOL independence; `.gitattributes` keeps builder/schema hashes stable. ZIP entries retain the existing deterministic ordering, timestamps and modes.

## Approval gates

The owner selected public distribution from this repository, not a dedicated distribution repository. The source repository is public. Visibility does not clear future candidate content or authorize publication; review current public suitability and Git author metadata before any approved commit/push. Local tests, scans and CI cannot provide semantic privacy clearance. MIT is selected for the public skills, documentation and tooling; see root `LICENSE`. It does not license the remote MCP service, grant service access, or waive authentication, authorization or service terms. Licensing is not account/target authority, privacy clearance or publication approval.

Commit reviewed source and generated artifacts together within the owner's repository publication authorization. Marketplace release tagging and submission separately require approved licensing/distribution terms, actual-host acceptance and explicit release authority. No tool or CI job here creates tags, releases, uploads or changes visibility. Verify the release checkout and independently pin the builder/dependencies; rebuild ZIPs at that approved tag and retain their SHA-256 values. Existing `pack.py --release-commit` can separately verify a clean source-commit-pinned candidate; distribution does not put that commit into its own generated output.

## Listing readiness

Bounded OpenAI listing metadata is available in the inventories and generated OpenAI manifests; it is not a submitted or complete listing. Product descriptions describe supported jobs, not verified host availability. Website links select the canonical product guides in this public GitHub repository; support uses the established public URL, and service terms and privacy link to the approved repository legal documents, distinct from the MIT license. Both inventories explicitly select the owner-approved [Piranya icon](artwork.md). OpenAI logo and composerIcon refer to `./assets/piranya-icon.png`; both provider ZIPs and Claude trees include its exact hash-bound bytes. Claude manifests declare `icon: "./assets/piranya-icon.png"` through the explicit `claude_icon` inventory field; no generated alias or second artwork source is needed. Publisher/domain ownership, privacy-policy applicability, authenticated host behavior, reviewer access and submission authority remain independent gates tracked in [release requirements](backlog.md). No credentials, portals, target probes or release tags are needed for offline metadata validation.

Review scenarios and public synthetic fixture prerequisites are maintained in [review case authoring](review-cases.md). Both 0.2.1 inventories contain five positive and three negative cases; reporting positive feature behavior and negative 1 refusal are owner-reported, not independently certified (negative 1 has no tool trace). Reporting negative 2 unsupported 10-minute refusal is also owner-reported with no verified tool trace. Reporting negative 3 CLV/XLSX refusal is owner-reported with no verified tool trace; all site-management cases remain NOT RUN. A real recording, stable fixture certification and reviewer host acceptance remain required before submission.

## Consumer updates

Claude consumers must select the reviewed release tag and the specific `plugins/site-management` or `plugins/reporting` path using their host's supported plugin installation workflow. Validate each unpacked plugin with `claude plugin validate <directory> --strict` and exercise authentication, discovery and consent boundaries in the actual host. OpenAI consumers use the corresponding OpenAI ZIP built from that same tag and must verify actual host acceptance. Offline validation is not host certification. Do not treat `main` as an automatic deployment channel; updates require an explicit reviewed tag/ZIP refresh.

Inventories without license fields remain supported by the updated builder. Older strict builders reject unsupported `license`, `license_file` or `readme_file` fields; consumers must explicitly upgrade their reviewed public builder/source pin and regenerate reviewed locks before consuming these inventories. Existing internal pins and site imports are not changed by distribution. Builder hashes invalidate earlier locks even for unchanged inventories.

An arbitrary MCP backend can change independently of these pinned skill/plugin files. Pinning distribution content does not pin backend implementation or authorize new tools. Automatic backend or repository scans are independent checks, not deployment approval or a substitute for human privacy/history review.
