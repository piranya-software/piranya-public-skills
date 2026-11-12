# Piranya skills

Provider-neutral skills for meaningful user jobs. The repository is **private initially**; its selected inputs must still be suitable for eventual public distribution. No license has been selected. Nothing here authorizes publication, visibility changes, commits, pushes, listing submission, deployment, reviewer provisioning, or credential handling.

## Layout

- `skills/`: canonical skill content and portable supporting references.
- `packages/`: explicit package inventories, independent of provider.
- `tools/pack.py`: offline Python CLI; selects only declared files, never archives a checkout.
- `schemas/`: byte-pinned official Agent Plugins 1.0.0 schemas and source/hash provenance.
- `tests/`: synthetic safety and reproducibility tests.
- `dist/`: ignored local locks and generated ZIPs.

The initial site-management inventory selects `piranya-site-editing` and `piranya-catalog-management`; reporting selects `piranya-sales-reporting`. Every supporting file must be explicitly listed in its inventory before locking. Missing or undeclared dependencies fail rather than being copied implicitly. Other product areas, skills-only packages (`"connectors": {}`), several connectors, and either provider use the same builder.

## Local commands

Follow [skill maintenance](docs/maintenance.md) before authoring improvements or refreshing consumer copies. Canonical source and pinned consumption have separate update steps; generated copies are never authoring targets. See [same-repository distribution and release gates](docs/releasing.md) for generated Claude plugin paths, both provider ZIPs and release-tag consumption.

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

## Consume from another repository

Use an explicitly supplied, reviewed checkout/tool path, never a runtime sibling-path assumption:

```sh
python "$PUBLIC_BUILDER_PATH/tools/pack.py" lock --source "$PUBLIC_SOURCE_PATH" --inventory "$PUBLIC_INVENTORY_PATH" --lock "$PUBLIC_LOCK_PATH"
python "$PUBLIC_BUILDER_PATH/tools/pack.py" build --source "$PUBLIC_SOURCE_PATH" --inventory "$PUBLIC_INVENTORY_PATH" --lock "$PUBLIC_LOCK_PATH" --provider openai --output "$PUBLIC_OUTPUT_PATH"
```

The caller must provide these actual paths. Pin the reviewed public builder checkout by commit before release; independently verify its checkout and dependencies. The lock includes builder and schema content hashes and the complete selected source-input hashes, so an initial local snapshot can be consumed without a fictitious commit. Preserve/review that lock as an input to an internal build; do not regenerate it automatically in a consumer build. Private composition belongs to a separate internal builder, not to this CLI: `--source` accepts only the public `skills/<name>/...` inventory shape. No internal checkout, network fetch, or private evidence is consulted at runtime. See [packaging contract](docs/packaging.md).

## Provider formats and release gates

OpenAI/portable output uses root `plugin.json` and optional `mcp.json`, official Agent Plugins 1.0.0 schemas, and `streamable-http`. Claude output uses `.claude-plugin/plugin.json`, optional root `.mcp.json`, and `http`. Skills remain at root `skills/` for both. No invented provider authorization or tool-filter fields are emitted. See [schema provenance](docs/schemas.md) and [endpoint evidence](docs/endpoints.md).

Local validation is not host certification or semantic privacy clearance. Repository publication and visibility require owner authority and complete content/history disclosure clearance, including Git author metadata. Marketplace release separately requires approved licensing/distribution terms, source/tooling pins, submission authority and authenticated host installation/OAuth/discovery plus read/write/delete-consent testing. Claude strict plugin validation and actual OpenAI host acceptance remain separate checks. No host acceptance, reviewer access or listing approval is claimed by the offline builder.
