# ROA programme engineering method profile

This document describes a recurring engineering pattern visible across ROA-associated repositories. It is a programme-level map, not a universal conformance contract: repository-local contracts, oracles and evidence remain authoritative.

## Compact loop

```text
human intent / target
        -> exact repository AS-IS
        -> gap + debt + authority/evidence boundary
        -> minimum coherent semantic slice
        -> revision/source/blob-bound candidate where required
        -> implementation
        -> executable repository-local oracles
        -> semantic/state/authority mutation campaign
        -> independent no-novelty tail
        -> bounded modeled saturation OR repair/escalation/remodel
        -> PR/merge
        -> reload exact AS-IS and re-derive
```

## 1. Exact AS-IS before intent expansion

Work begins from the current canonical repository state, not from an old roadmap or previous assistant recommendation. The relevant local neighborhood, target gap, blockers, evidence obligations and authority boundaries are re-derived.

A roadmap is therefore a falsifiable hypothesis about what should happen next. It does not become a second source of runtime truth.

## 2. Minimum coherent semantic slice

A slice is not merely a feature-sized diff. It is the smallest coherent transformation that closes or contains a demonstrated semantic, authority, evidence, runtime or governance gap while minimizing unrelated surface expansion.

The unit is semantic because its boundary is defined by what must remain true: ownership, evidence, transitions, failure behavior, authority or reconstruction properties.

## 3. Candidate identity and blob binding

Where required by a repository's evidence model, the candidate is bound to an exact revision and exact Git blob/content digests for the relevant runtime surfaces.

Blob binding answers: **which exact bytes does this receipt or falsification evidence concern?**

It does not answer: **are those bytes correct, secure, complete or true in the world?** Those claims require their own oracle.

## 4. Executable oracles before promotion

Static documents, dashboards, file existence and topology are not silently promoted into runtime evidence. The slice must satisfy whatever executable tests, readbacks, receipts, CI gates, replay checks, source-binding checks or external observations its local claim requires.

## 5. Adversarial semantic mutation

Mutation campaigns attack the declared boundary rather than merely maximizing a number. Depending on the repository and slice, mutation families can target:

- semantic distinctions and forbidden equivalences;
- state-machine transitions and continuity;
- authorization or authority relaxation;
- provenance, evidence and receipt binding;
- error/failure handling;
- transport and materialization;
- cross-layer combinations;
- transformation losslessness and compression.

Campaign scale is repository-local and risk-adjusted. Some governed components use escalation ladders such as `1k -> 100k -> 1M -> 10M`. An unsafe survivor, a new root class/signature or a non-converged tail can require the next tier.

Counts are meaningful only inside the declared model. Ten million semantic/state mutations are not automatically ten million compiled AST mutants and do not constitute production or scientific proof.

## 6. Saturation by no-novelty

Primary mutation volume is not the convergence criterion.

After known modeled classes have been exercised, an additional independent tail must fail to discover a new **material** failure class or signature before a bounded modeled saturation claim is admitted.

Material novelty is structural. Examples include a new:

- canonical owner;
- denominator or dependency;
- supported boundary;
- root failure path/class/signature;
- evidence obligation;
- rollback or retirement domain;
- human gate;
- authority transition.

Another instance of an existing equivalence class does not necessarily reset saturation.

Late novelty invalidates saturation. Persistent novelty at the maximum governed tier is a reason to remodel the taxonomy or design, not permission to declare success.

Where compression/refactoring is itself optimized, a second independent tail may test whether a materially better valid compression remains (`no-better-compression`).

## 7. Bounded claim

The result of the loop is deliberately local:

```text
modelled saturation != executable proof
modelled saturation != runtime proof
modelled saturation != physical/world observation
modelled saturation != external validation
modelled saturation != scientific truth
```

The next stronger claim requires the next stronger oracle.

## Representative repository evidence

The programme-level pattern is descriptive and is grounded in repository-local mechanisms, including:

- **ROA** - hosted semantic-chat governance includes deterministic multi-million semantic/governance mutation campaigns and explicit no-novelty tails.
- **iKant** - engineering governance derives a minimum semantic slice from exact AS-IS/gap/debt state, supports risk-adjusted mutation ladders and treats persistent novelty as a fail-closed remodelling signal; source-bound receipts bind relevant runtime Git blobs.
- **A-OSP** - roadmap/governance artifacts distinguish material novelty from new examples of an existing class and require repeated zero-novelty windows for saturation claims in relevant engineering analysis.
- **Juriscribe** - mutation/stress evidence, no-novelty and no-better-compression tails are explicit parts of convergence and compression/consolidation modes, with source transport bound to pinned revisions and Git blob identity where attested execution is claimed.

These examples do not imply identical implementation across every programme repository.
