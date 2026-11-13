# Maintaining and consuming skills

[Product overview](../README.md) · [Build and contributor commands](#contributor-setup-and-builds)

## One authoring home

Edit reusable skill source here, never a generated package or an installed consumer copy. Public-safe site editing, Catalog and Reporting guidance belongs in this repository. Employee-only import orchestration and source analysis belong in the internal skills repository. A new product/workflow can introduce a new skill when it has a useful user-job trigger; a tool or technical namespace alone is not a reason for a skill.

Keep producer schemas, implementation contracts and enforcement in their owning repositories. Skills explain how to use those contracts, not how to bypass missing capabilities. Keep private evidence and customer examples out of this public repository.

## Freshness before authoring

1. Resolve the selected checkout and instructions. Check branch, status and configured upstream; fetch metadata before deciding whether it is current.
2. Never pull over dirty files, silently stash, reset or switch an active writer. Coordinate overlap. If clean and behind the intended upstream, an explicitly requested fast-forward can update it; divergence needs reconciliation.
3. Read the current canonical rule and relevant producer contract before changing it. Update contradictory guidance in place, qualify compatibility and preserve unique safety constraints.
4. Recheck upstream before publication. A current checkout at session start is not proof that nobody published meanwhile.

## Verification and publication

Run the repository tests, validate skill identity and references, inspect public suitability, and explicitly add new supporting files to every affected package inventory. Re-lock only as a deliberate acceptance of selected source/tooling changes; never use automatic re-locking to hide stale-lock failures. Build and inspect both selected provider outputs; syntax validation and synthetic tests do not prove live-host behavior.

Use the owning repository's authorized publication process. Capture the exact published commit, then update the internal consumer's public source pin/lock and rebuild that composition. Publish the internal consumer before advancing site-imports' dependency record. Verify remote heads rather than treating push exit alone as publication evidence.

## Consumption is deliberate

Consumers pin immutable source revisions and verify package/file hashes. At session start, check upstream metadata and selected pins; report available changes. Select upgrades explicitly at a safe task boundary. Do not silently change a running import's instructions when main advances.

Generated copies must remain distinguishable from authoring source. Refuse to overwrite locally changed or unmanaged files. An upstream improvement is not consumed until the relevant consumer pin is advanced, its package regenerated and its installed content verified. Report source publication separately from consumer adoption and host acceptance.

## Learning cadence

During work, capture reusable discoveries at coherent checkpoints and before ending the session. Choose public skill, internal workflow, producer design pattern, pack, recipe or backlog by purpose. Require evidence and applicability limits; do not invent a lesson for every session or preserve incident narratives as general rules. Publish independently useful approved corrections without waiting for unrelated product work, then close the consumer update loop.

## Contributor setup and builds

### Layout

- `skills/`: canonical skill content and portable supporting references.
- `packages/`: explicit package inventories, independent of provider.
- `tools/pack.py`: offline Python CLI; selects only declared files, never archives a checkout.
- `schemas/`: byte-pinned official Agent Plugins 1.0.0 schemas and source/hash provenance.
- `tests/`: synthetic safety and reproducibility tests.
- `dist/`: ignored local locks and generated ZIPs.

The initial site-management inventory selects `piranya-site-editing` and `piranya-catalog-management`; reporting selects `piranya-sales-reporting`. Every supporting file must be explicitly listed in its inventory before locking. Missing or undeclared dependencies fail rather than being copied implicitly. Other product areas, skills-only packages (`"connectors": {}`), several connectors, and either provider use the same builder.

### Local commands

Follow [skill maintenance](maintenance.md) before authoring improvements or refreshing consumer copies. Canonical source and pinned consumption have separate update steps; generated copies are never authoring targets. See [same-repository distribution and release gates](releasing.md) for generated Claude plugin paths, both provider ZIPs and release-tag consumption.

Python 3.11+ and the dependencies declared in `tools/requirements.txt` are required. Inventories and locks use JSON; the builder does not claim YAML/frontmatter validation. Installation is an explicit operator action, not a builder side effect:

```sh
python -m pip install -r tools/requirements.txt
python -m unittest discover -s tests -v
python tools/pack.py lock --source . --inventory packages/site-management.json --lock dist/site-management.lock.json
python tools/pack.py build --source . --inventory packages/site-management.json --lock dist/site-management.lock.json --provider openai --output dist/site-management-openai.zip
python tools/pack.py build --source . --inventory packages/site-management.json --lock dist/site-management.lock.json --provider claude --output dist/site-management-claude.zip
python tools/pack.py lock --source . --inventory packages/reporting.json --lock dist/reporting.lock.json
python tools/pack.py build --source . --inventory packages/reporting.json --lock dist/reporting.lock.json --provider openai --output dist/reporting-openai.zip
```

Run locking only after reviewing the exact inventory and selected content. Re-locking accepts changed content; it is not a security approval. The initial uncommitted snapshot is supported deliberately. `build` refuses stale content or builder/schema hashes. Repeating a build with unchanged locked inputs produces identical ZIP bytes (stored compression, sorted entries, fixed timestamps and modes). Generated `package-inputs.json` records selected source, builder/schema hashes, provider and output-file hashes; the CLI prints the ZIP SHA-256.

For a source-commit-gated candidate, add `--release-commit FULL_40_CHARACTER_GIT_COMMIT` to `build`. This is not a literal usable value: supply the actual commit. The check requires a clean source checkout at that commit and verifies every selected byte against Git. It does not grant release approval. Initial uncommitted content cannot pass this gate.

### Consume from another repository

Use an explicitly supplied, reviewed checkout/tool path, never a runtime sibling-path assumption:

```sh
python "$PUBLIC_BUILDER_PATH/tools/pack.py" lock --source "$PUBLIC_SOURCE_PATH" --inventory "$PUBLIC_INVENTORY_PATH" --lock "$PUBLIC_LOCK_PATH"
python "$PUBLIC_BUILDER_PATH/tools/pack.py" build --source "$PUBLIC_SOURCE_PATH" --inventory "$PUBLIC_INVENTORY_PATH" --lock "$PUBLIC_LOCK_PATH" --provider openai --output "$PUBLIC_OUTPUT_PATH"
```

The caller must provide these actual paths. Pin the reviewed public builder checkout by commit before release; independently verify its checkout and dependencies. The lock includes builder and schema content hashes and the complete selected source-input hashes, so an initial local snapshot can be consumed without a fictitious commit. Preserve/review that lock as an input to an internal build; do not regenerate it automatically in a consumer build. Private composition belongs to a separate internal builder, not to this CLI: `--source` accepts only explicit public skill files, optional root LICENSE, optional `products/*.md` README selection and explicitly selected bounded `assets/*.png` artwork. No internal checkout, network fetch, or private evidence is consulted at runtime. See [packaging contract](packaging.md).

### Provider formats and release gates

OpenAI output uses root `plugin.json`, optional `mcp.json` and `streamable-http`. Portable metadata and transport envelopes use official Agent Plugins 1.0.0 schemas; the bounded OpenAI server-auth overlay is validated separately. Root `mcp.json` retains the required Agent Plugins `$schema` format marker even with OAuth; this is not full extended-document conformance to the pinned portable schema. Claude output uses `.claude-plugin/plugin.json`, optional root `.mcp.json`, and `http`. Skills remain at root `skills/` for both. Explicit `openai_auth` selects only OAuth with optional CIMD preference; no fixed client IDs, secrets, arbitrary extension pass-through or tool-filter fields are accepted. Claude OAuth remains server-discovered; do not add an invented auth switch or treat an empty `oauth` object as requiring OAuth. See [schema provenance](schemas.md) and [endpoint evidence](endpoints.md).

Local validation is not host certification or semantic privacy clearance. Repository publication and visibility require owner authority and complete content/history disclosure clearance, including Git author metadata. Marketplace release separately requires approved licensing/distribution terms, source/tooling pins, submission authority and authenticated host installation/OAuth/discovery plus read/write/delete-consent testing. Claude strict plugin validation and actual OpenAI host acceptance remain separate checks. No host acceptance, reviewer access or listing approval is claimed by the offline builder.
