---
name: test-driven-development
description: 'TDD: enforce RED-GREEN-REFACTOR, tests before code.'
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - testing
    - tdd
    - development
    - quality
    - red-green-refactor
    related_skills:
    - systematic-debugging
    - subagent-driven-development
x-local-maintainer: TyphooN (TyphooN-)
---


# Test-Driven Development (TDD)

## Portable scope

This copy preserves a locally developed workflow, not transferable approval. Resolve the current task, repository, active Hermes profile, tools and ownership on this machine first. Historical project choices and TyphooN-specific executor/build policies are context, not permission to start services, run targets, modify security settings or publish. Project-root variables are documented in the collection's `PORTABILITY.md`; unset variables are not usable paths. Installing a skill installs no external tools or plugins.

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** Observe a regression fail for the intended new behavior before changing production code. Characterize inherited behavior separately; passing retrospective tests do not establish a prior RED→GREEN sequence.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the user first):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO NEW PRODUCTION BEHAVIOR WITHOUT A FAILING REGRESSION FIRST
```

For new behavior written before its failing test, stop implementation and return to RED for the affected owned change. Preserve its checkpoint and do not design assertions merely to bless the new code. TDD is not authority to delete user work, inherited implementations, frozen evidence or another executor's partial results.

## Existing and recovered code

1. Preserve the inherited baseline and establish ownership before edits; recovery must not erase the evidence it is meant to validate. On reboot-prone hosts, fsync each owned source before its tests, then fsync the source-bound result/log and containing directory: a durable receipt can outlive a zero-length source file. Restore missing owned code only from an exact retained preimage matching its recorded hash, and label that restoration as recovery rather than a new test execution.
2. Reconcile retained test receipts before choosing new work. Verify the source, selected tests, shared guard/fixtures, relevant environment and log bindings, then identify the actual assertion failures and any newer passing executions; a stale draft is not the test frontier. When restored fixtures disagree with a compatibility contract, establish that contract independently before deciding which side is stale. Pin immutable identifiers or wire encodings with literal expected vectors rather than deriving the oracle from the implementation under test; changing production identities to satisfy an obsolete fixture can invalidate retained state. Preserve the original failure and correct only the proven stale expectation, retaining all semantic assertions and negative controls. Label this fixture alignment, not a new product defect or a retrospective product RED→GREEN pair.
3. Resume the missing phase, not the executor's whole assignment. When a saved intended RED matches the unchanged pre-change source/test state, give the successor its exact failed identities and preserved snapshots and proceed directly to GREEN. When implementation has already advanced, retain the earlier causal pair and continue from the latest valid GREEN; do not restore old production bytes or rerun a known failure merely to recreate test-first history after an ownership change.
4. Run focused characterization only where inherited behavior lacks reusable current proof, using the real saved inputs and explicitly synthetic failure cases as appropriate. Report a first-run pass honestly as characterization; do not change a correct assertion to manufacture RED.
5. For any new behavior or bug fix without an applicable saved RED, add and observe the intended failing regression before the production change. For a behavior-preserving refactor, establish the existing contract first and keep it green.
6. Keep original execution, recovered execution, synthetic fixtures and independent acceptance separate in the handoff. Leave an interrupted worker's terminal outcome unknown when no final result survived, even when its durable test exits are known; the two records establish different things.

## Source-only native checkpoints

When native compilation/execution is held, pair any narrow token-presence contract with an explicit completeness regression for the known required helper definitions. A saved `main()` and forward declarations can satisfy superficial entry-point checks while leaving the candidate unfinished. Preserve the implemented prefix and test the actual missing-definition frontier before adding the remaining bodies.

Label such checks lexical/source-only: they do not establish C syntax, types, linking, runtime ownership safety or native behavior. Keep required compilation, dynamic proof and independent acceptance open; never turn a token-only GREEN into native readiness or replace missing helper bodies with stubs to satisfy the guard.

## Red-Green-Refactor Cycle

### RED — Write Failing Test

Write one minimal test showing what should happen.

**Good test:**
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'

    result = retry_operation(operation)

    assert result == 'success'
    assert attempts == 3
```
Clear name, tests real behavior, one thing.

**Bad test:**
```python
def test_retry_works():
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), 'success']
    result = retry_operation(mock)
    assert result == 'success'  # What about retry count? Timing?
```
Vague name, tests mock not real code.

**Requirements:**
- One behavior per test
- Clear descriptive name ("and" in name? Split it)
- Real code, not mocks (unless truly unavoidable)
- Name describes behavior, not implementation

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
# Use terminal tool to run the specific test
pytest tests/test_feature.py::test_specific_behavior -v
```

Confirm:
- Test fails (not errors from typos)
- Failure message is expected
- Fails because the feature is missing

Record the expected outcome separately from the literal child exit and actual failed testcase identities. Judge a reproduction or diagnosis milestone against that failure contract: an intended exit-1 RED can complete the diagnostic step while the buggy candidate remains unready. If a tracker treats that exit alone as failed diagnosis, append a contract-aware result linked to the original receipt; never rewrite the exit, erase the failures or waive an unrelated setup error to make the panel green.

When a RED invocation also selects passing guards or positive controls, derive the causal RED set from actual failure/error records, including parameterized subtest identities, not the complete selected-node set. Reconcile collection, executed nodes, outcomes and exit separately; a passing default-effect guard can validly precede a failing producer tracer in the same exit-1 run. Count RED/GREEN cycles separately from the union of unique failed identities, because one parameterized cycle can fail multiple cases. Bind each claimed pair to saved source/test snapshots and report whole-test-file equality separately from causal-test equality. When unrelated tests were appended, compare the exact causal functions, decorators, parameter data and relevant fixture/helper closure; do not invalidate an intact pair merely because the file grew, or bless it from matching function bodies when a causal helper changed. Record justified behavior-neutral fixture formatting deltas separately. Before crediting a pair, require every failed identity to appear and pass in the matching source-bound GREEN and applicable final full-suite proof, rather than disappear, skip or error during setup.

**New-behavior test passes immediately?** Check whether the requested behavior already exists or the assertion misses the intended change. An inherited-code characterization test may legitimately pass immediately; label it honestly rather than manufacturing failure.

**Test errors?** Fix the error, re-run until it fails correctly.

### GREEN — Minimal Code

Write the simplest code to pass the test. Nothing more.

**Good:**
```python
def add(a, b):
    return a + b  # Nothing extra
```

**Bad:**
```python
def add(a, b):
    result = a + b
    logging.info(f"Adding {a} + {b} = {result}")  # Extra!
    return result
```

Don't add features, refactor other code, or "improve" beyond the test.

**Keep GREEN minimal, not weaker.** A straightforward implementation may use literals or temporary duplication when they satisfy the real contract. Never weaken assertions, preservation guards, budgets or required negative paths to obtain GREEN. Refactor duplication after the focused regression passes, then verify the complete required behavior and failure scope before closing; refactoring is not a promise to repair knowingly skipped correctness later.

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
# Run the specific test
pytest tests/test_feature.py::test_specific_behavior -v

# Then run ALL tests to check for regressions
pytest tests/ -q
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)
- The expected nonempty testcase identities actually executed. Running an empty/truncated Python test file can exit 0 without testing anything; require the observed collection/execution count, and after an interrupted or rebooted session bind proof to nonempty test/source files before crediting success. Fsync task-owned source and proof when host reboot instability is observed.

**Test fails?** Fix the code when the test expresses the established contract. For a restored fixture that may express an obsolete contract, follow **Existing and recovered code** first; never weaken a valid assertion merely to obtain GREEN.

**Other tests fail?** Fix regressions now.

### REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers
- Simplify expressions

Keep tests green throughout. Don't add behavior.

**If tests fail during refactor:** Reverse only the owned refactoring delta from its recorded preimage, preserve unrelated work, and take smaller steps; never reset a dirty checkout to recover green.

### Repeat

Next failing test for next behavior. One cycle at a time.

## Avoid Horizontal Slices

Do **not** write all tests first and then all implementation. That is horizontal slicing: RED becomes "write a pile of imagined tests" and GREEN becomes "make the pile pass." It produces brittle tests because the tests are designed before the implementation has taught you what behavior and interface actually matter.

Use vertical tracer bullets instead:

```text
WRONG:
  RED:   test1, test2, test3, test4
  GREEN: impl1, impl2, impl3, impl4

RIGHT:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

A tracer bullet is one end-to-end behavior slice. It proves the path works, teaches you about the interface, and keeps each next test grounded in what you just learned.

## Why Order Matters

**"I'll write tests after to verify it works"**

A test written after a new implementation does not show that it would have caught the missing behavior:
- It may test the wrong contract or mirror implementation details.
- It may miss the original defect or an important failure path.
- No observed pre-change failure supports a RED→GREEN claim.

For new changes, test-first demonstrates the intended missing behavior. For inherited code, characterization establishes a reproducible current contract and guards later changes; it is useful proof, but not evidence of test-first history.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Do not let sunk cost justify skipping a failing regression for new behavior. Equally, do not destroy inherited or frozen work to simulate test-first development. Preserve the baseline, characterize existing behavior, and apply RED→GREEN to the next owned behavior change.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals — it's spirit not ritual"**

For new behavior, retrospective tests can mirror the implementation instead of demonstrating the intended missing contract. Write the failure first. For inherited behavior, characterize what exists without pretending that this reproduces its development order; use a failing regression for subsequent fixes or additions.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | For a new change, passing later does not show the test catches the missing behavior. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Preserve inherited work; sunk cost still does not excuse skipping RED for a new owned change. |
| "Keep as reference, write tests first" | Do not backdate new implementation history; distinguish inherited characterization from the next RED→GREEN change. |
| "Need to explore first" | Keep exploration separate from production changes and preserve required evidence; start each new behavior from a failing test. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for the code you touch. |

## Red Flags — Return the owned change to RED

Stop a new behavior change when:

- Production behavior was added before observing its intended failing regression.
- Assertions were weakened or tailored solely to match the new implementation.
- The failure cannot be explained or is an unrelated setup error.
- Manual checks, elapsed effort or later passing tests are presented as proof of test-first development.
- A characterization test is relabelled as a historical RED phase.

Return to the intended failing contract before further implementation. Preserve inherited/user-owned code, frozen proof and unrelated work; destructive cleanup does not establish TDD.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Observed each new-behavior/fix regression fail before its production change
- [ ] Identified inherited-code characterization separately, without a retrospective RED claim
- [ ] Each required RED failed for the intended missing behavior, not a typo or setup error
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Do not claim TDD for an unobserved development sequence. Return an incomplete new change to RED; retain and accurately label inherited characterization rather than deleting the baseline.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. Ask the user. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify the design. |

## Hermes Agent Integration

### Running Tests

Use the `terminal` tool to run tests at each step:

```python
# RED — verify failure
terminal("pytest tests/test_feature.py::test_name -v")

# GREEN — verify pass
terminal("pytest tests/test_feature.py::test_name -v")

# Full suite — verify no regressions
terminal("pytest tests/ -q")
```

### With delegate_task

Give the implementation worker a self-contained task packet with the baseline, owned paths, intended behavior and project's canonical focused/broader checks. Require the observed failing regression, minimal change, passing proof and exact commands/exits in its handoff. For recovered existing code, require preserved inputs and characterization before any new change. Use the current `delegate_task` schema rather than copying stale invocation parameters. TDD grants no commit, push or publication authority.

### With systematic-debugging

Bug found? Write failing test reproducing it. Follow TDD cycle. The test proves the fix and prevents regression.

Never fix bugs without a test.

## Descriptor-backed I/O tests

For input-byte budgets, observe the underlying descriptor offset at the reservation boundary, not only `handle.tell()`, parser counters or intercepted logical reads: a buffered reader can already have fetched trailing data. Use admitted synthetic regular files and an intact positive control; keep application-read bounds distinct from kernel readahead, heap limits and preemptive deadlines. The linked recipe includes the discriminating read-ahead controls.

Model pathname bindings and open-handle identities independently. A rename or replacement changes which inode a name resolves to, not the inode already held by an open FD; keep mutable metadata on the inode rather than freezing all `fstat` fields at open. Otherwise a fake can reject through an earlier FD-identity check while leaving the intended path-relationship branch untested.

Vary one refusal condition at a time with every preceding check valid, and distinguish acknowledged close plus FD-number reuse from close uncertainty. For file-size budgets, vary held-descriptor `st_size` independently from pathname metadata before and after the real private-fixture reader; pathname-only growth can leave missing descriptor checks green. Assert read-entry counters and checked closure outside production catches, and keep size budgets separate from persistent association identity. Test interrupted current handoff and rejection after a completed earlier transfer separately; exception bookkeeping for one invocation must not retroactively relabel or revoke resources already returned by another. Install default-backend refusal in the shared guard used by every admitted suite, not only in the new feature's fixture. Keep mock-only tests synthetic; neither a correct fake nor green tests establish actual filesystem or runtime behavior. Use [Descriptor-backed I/O test design](references/descriptor-backed-io.md) for the fixture model and discriminating case matrix.

For bounded snapshot readers, inject identity, pathname or timestamp changes during the final zero-byte EOF probe as well as earlier data reads. An earlier mutation can be rejected by the next pre-read pin and conceal a missing post-read check. Verify the final-boundary cases against a disposable mutant removing only that post-read check, and retain its exact failed identities.

## Process death tests

- Test process creation before handle registration, not only at the first receipt write: inject failure at the first post-return statement and post-effect creation with no returned handle. Distinguish definitely-not-started, known-child and unresolved-creation custody; require no unknown-identity signals, domain removal or completion for the unresolved case. A nonzero exit alone does not prove child cleanup.
- Model uncertain post-effect wait delivery separately from ECHILD: inject a consumed child status followed by a delivery/decode failure, then assert outside production catches that no potentially reused numeric PID is signalled and custody is not falsely released. This is synthetic failure-path proof, not native process-mechanics evidence.
- Keep wait fixtures faithful to their API: model a live `waitpid(WNOHANG)` as `(0, 0)` and advance a synthetic clock until the production polling deadline expires. Do not throw `TimeoutExpired` from the waitpid fake, because that bypasses the real timeout path and can hide exception-custody defects.
- Audit initialization before a fork-based death test: logging, backend discovery, or runtimes can already have started threads. Do not run allocation, logging, environment mutation, or backend work in a child inheriting those locks. Prefer a fresh executable child with an internal worker mode dispatched before threaded initialization.
- Distinguish the intended assertion signal from setup failure and successful acceptance of invalid input. Check the exact assertion text in focused proof so an unrelated abort cannot masquerade as the regression result.
- Disable core dumps in the disposable worker, bound the parent's wait, and terminate/reap only that worker on timeout. Exercise launch failure and timeout cleanup as well as the expected assertion.
- Inject catchable cancellation at final persistence and both sides of signal-handler restoration, not only during child wait. A deferred callback can change live cancellation state after a report snapshot or an already-evaluated return value. Require nonzero outcomes for accepted late cancellation and truthful terminal status; keep pending-owner reports distinguishable from a post-handoff terminal report. Label synthetic signal callbacks separately from real POSIX signal proof.
- When scanning processes for an existing worker, compare complete argv tokens and exclude the inspection process. Searching command-line substrings can match the inspector's own inline script and falsely suggest an active lane.
- Scope cleanup fault injection to the intended operation and phase, not just the filename. A synthetic control file may be initialized with an empty value before a later kill/control write; rejecting both can produce a false RED before any child exists. Choose the intended exception class and errno deliberately, and assert the constructed type and reached boundary: Python can specialize `OSError(errno.EACCES, ...)` into `PermissionError`, selecting a different production catch than the fixture intends. Assert that acquisition/dispatch occurred before the injected terminal failure, preserve invalid proof receipts, and rerun a corrected fixture against both the frozen original and candidate. Label a corrected post-implementation comparison retrospective rather than inventing test-first history.

## Exact source/patch guards

- Test source verification in real disposable Git trees. `git status` can hide tracked edits under `assume-unchanged` or `skip-worktree`; reject visibility-suppressing flags before every manifest branch, or independently reconstruct all tracked working-tree content with a fresh index. Exercise both flags with and without declared patches and check real-index preservation.
- Preserve unified patch syntax: an empty context line contains one literal space. If packaged `.patch` files cause false-positive blank-at-EOL failures, use a narrowly scoped `.gitattributes` rule such as `upstream/patches/*.patch whitespace=-blank-at-eol`; keep other checks and independently run `git diff --check` on the actual source. Do not strip context prefixes or globally disable whitespace checking.
- Run a relative-path SHA256SUMS check from the manifest's own directory and require every declared file to be verified. Never use `--ignore-missing` to certify a complete snapshot: a wrong working directory must remain a failed invocation until corrected and rerun.
- To commit an owned hunk in a pre-existing dirty file, record its initial working content and generate the unified patch from that snapshot to the updated working content, not from HEAD. Verify the complete delta equals only the authorized change, run `git apply --cached --check`, apply that patch to the index, and review the staged diff. This preserves the user's prior edits as unstaged work; never select a hunk by resetting the shared index or staging the whole dirty file.

## Installed helper bundles

- Prove packaging through the real managed installer in a disposable HOME, then remove its disposable source checkout before invoking the installed CLI. For stronger no-repository-fallthrough evidence, run the unmodified installed `__main__` under a fresh isolated interpreter with an exercised audit hook denying original-checkout reads; identify that Python boundary honestly, not as an OS sandbox. Assert real output payloads and preserve child exits/readback hashes, rather than counting file presence or `--help` as end-to-end delivery.
- Exercise newly packaged sibling dependencies through the existing registry transaction: registered-version replacement, exact no-op repeat, differing unregistered/manual-edit refusal before writes, and an injected registration failure after both replacement and first-time installation. Preserve earlier fixture failures and repair bare sibling imports with explicit file loading when the required `-I` interpreter excludes the test directory; never weaken interpreter isolation to obtain green.

## Consumer-boundary controls

- Include deterministic publication temporaries and lock paths in the same canonical alias set as explicit input/state/export destinations, before any input read or cleanup. Exercise the real CLI with absolute, relative and hardlinked aliases; assert exact input identity/bytes and directory preimages, because individually private regular files can still be user-supplied input rather than owned stale output.

- Exercise syntactically valid wrong-shaped configuration through the actual loader and every guarded consumer, not only parser errors. Preserve the distinction between invalid present lists/scalars, missing/empty valid mappings, and supported blank/null defaults; assert refusal before provider, credential, or fallback dispatch rather than merely checking a returned error.
- Scope async lifetime assertions to the loop/semaphore references owned by the test after its tasks and sockets finish. Collect cyclic garbage before checking weak references; immediate emptiness of an entire process-global weak cache can fail because of earlier traceback cycles. Do not clear active cache entries to manufacture a pass.
- Bind qualification criteria to the exact bytes used to parse the case snapshot, not to later reads of the same path. Reproduce stale-initial/then-reviewed bytes and assert zero dispatch/no reusable false pass; also test late observation/publication changes and unchanged-case reuse.
- Test narrow workload exceptions at every admission layer, including quiet polls. A coarse cwd-derived conflict class is not compile proof: exercise every recognized transfer command, package manager and unknown driver under that cwd, preserve strict/legacy behavior, and require positive compiler controls with the same shared predicate.
- Test strict opt-in admission against inherited operator waivers before quiet/input preflights, dispatch, and cache reuse, plus late waiver changes. Preserve legacy gates' waiver behavior without mutating the global waiver set; putting a waiver in a receipt does not satisfy an unwaived admission invariant.

- Exercise callback-capable opaque-handle equality/hash/repr at validation and collection-membership boundaries, not only explicit backend hooks. Arm reentry after the preceding effect, then assert later effect attempts outside product catches; a retained failure discovered only after another consuming call is not a passing guard. Preserve legitimate stable-value opaque-handle controls.
- For backend-returned validated mappings, mutate the original during a later callback and assert the consuming operation receives the validated projection or refuses before dispatch. A type check at acquisition does not freeze a backend-owned alias; preserve unchanged/shared positive controls and avoid custom deepcopy hooks when exact primitive fields can be detached safely.
- Test root selection through the actual launcher/configuration/cache consumer with two distinct disposable checkouts. Mutate only the selected served artifact and assert receipt revocation. Monkeypatching a helper's ROOT can hide an integration bug where serving honors an override but identity construction fingerprints another checkout.
- Serialize malformed response candidates through the real bounded decoding path before classifying them as wire-visible defects. Python integer-key dictionaries become string-key JSON objects; preserve a serialization control and do not report an unreachable in-memory shape as an HTTP bug. Keep all synthetic lifecycle results explicitly offline and ineligible for model qualification.

## Closure-to-runtime identity tests

1. Capture the recorded identity through the actual producer within the admitted SOURCE/MOCK scope. Keep private filesystem copying and hashing real; mock only external ELF, loader, process and provider effects.
2. Mutate one extracted member after capture while preserving its admitted archive and admission record, then invoke the real assembly consumer. Cover each distinct member-class branch that claims the same invariant; one correct library path does not establish executable-tool handling.
3. Observe RED before the production edit. Require the specific identity refusal and absent effects outside product catches. Add an unchanged control that reaches a dedicated mocked external boundary and checks copied bytes and manifest digests against the original producer identity. Give that boundary a sentinel exception type distinct from the intended refusal, because an arbitrary caught exception can hide acceptance of the changed member.
4. Preserve the failing source/test preimages, make the minimal identity fix, and require every failed identity to pass in GREEN without weakened assertions. Record whether regression bytes stayed identical; if the causal assertion or fixture changes, establish the new pair rather than silently crediting the old RED. Label a control stopped at the first mocked boundary as proof only up to that cut point, not complete assembly, native loader behavior or concurrent-copy-race qualification.

## Physical GPU inventory contracts

- Keep management-tool indices distinct from runtime ordinals. Preserve raw PCI/UUID/index fields, validate join keys before normalization, and test duplicate identities across all rows before clearing contested keys; early clearing can hide transitive or three-way collisions.
- Exercise unavailable tools/drivers, nonzero exits with plausible stdout, timeouts with partial stdout, malformed CSV, unsupported memory/display metadata, visibility reordering and MIG parents with offline fixtures. Mark unresolved runtime mappings explicitly unusable for placement; fixtures never establish actual CUDA/HIP/MIG qualification.
- Add inventory modes without silently migrating runtime-index consumers. Prove legacy default CLI/API contracts separately from opt-in physical observations, and distinguish an expected unavailable-source inventory exit from an unrelated pre-existing placement-suite failure.

## Testing Anti-Patterns

- **Testing mock behavior instead of real behavior** — mocks should verify interactions, not replace the system under test
- **Testing implementation details** — test behavior/results, not internal method calls
- **Brittle tests** — test behavior, not structure; refactoring shouldn't break them. Inject I/O faults at named semantic boundaries, not guessed global call ordinals. Distinguish pre-effect failure, post-effect uncertainty and unreturned partial acquisition; never expect a close-uncertain resource to count as checked-closed.
- **Happy path only** — always test edge cases, errors, and boundaries

## Final Rule

```
New behavior or bug fix → observed failing regression → minimal change → passing proof
Inherited behavior → preserved baseline → characterization, then RED→GREEN for later changes
```

Keep those histories distinct. No exception to test-first new behavior is implied by recovering existing code.
