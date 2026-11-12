# Maintaining and consuming skills

## One authoring home

Edit reusable skill source here, never a generated package or an installed consumer copy. Public-safe site editing, Catalog and Reporting guidance belongs in this repository. Employee-only import orchestration and source analysis belong in the internal skills repository. A new product/workflow can introduce a new skill when it has a useful user-job trigger; a tool or technical namespace alone is not a reason for a skill.

Keep producer schemas, implementation contracts and enforcement in their owning repositories. Skills explain how to use those contracts, not how to bypass missing capabilities. Keep private evidence and customer examples out of public source even while this repository is privately hosted.

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
