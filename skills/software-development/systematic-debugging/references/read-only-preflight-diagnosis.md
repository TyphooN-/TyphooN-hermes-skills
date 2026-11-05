# Read-only preflight diagnosis

Use when a stateful producer or data qualifier returns a generic refusal and live database/content access or recovery is outside the current scope. This procedure identifies an observed guard failure; it does not qualify a proposed fix or authorize activation.

## 1. Pin the failure and permitted boundary

1. Retain the original command, exit and bounded error receipt. Bind the relevant implementation files by hash.
2. Find the error-emitting catch and trace its called guards in execution order. Identify whether the first relevant boundary uses only path/file metadata, sanitized publications, or actual private content.
3. Inspect the chosen function before invoking it. A function named `preflight` is not necessarily read-only: it may create locks, temporary files or other state. Prefer the smallest existing predicate that can establish the suspected refusal without those effects.
4. Read only admitted metadata and sanitized artifacts. Record size, ownership, permissions, link count and the configured threshold when relevant; do not open a private database to rediscover a failure already explained by its stat metadata.

Do not infer corruption from a recovery suggestion printed for every exception. A compound predicate can report one generic error for several independent causes; evaluate its individual conditions before selecting a remedy.

## 2. Qualify a disposable diagnostic harness

Run the probe with the resolved interpreter, for example:

```text
/absolute/python -I -B /private/evidence/diagnose.py
```

Keep code, logs and receipts in the task's private evidence directory. Disable bytecode writes so importing installed/read-only modules does not create cache files beside them.

Before using real inputs:

- Enforce the admitted boundary: deny private-content opens, database connections, network/process dispatch and writes outside the evidence directory as applicable.
- Record forbidden attempts in counters/events and assert those counters outside production exception catches; a swallowed denial must not become apparent success.
- Exercise a positive metadata-only control and a deliberately forbidden control. Describe the resulting enforcement accurately: Python audit instrumentation is not an operating-system sandbox.
- Preserve original time, memory, SQL, row, path and identity limits. Instrumentation should observe the failure, not change admission policy.
- Account for directory-relative file operations. Python's `open` audit event omits `dir_fd` and can add close-on-exec flags; authorize an intended relative operation only after validating its actual directory FD, not by guessing from cwd. Preserve invalid-harness receipts and repair the guard before drawing product conclusions.

Where concurrent publication is possible, collect before/after hashes of the exact retained outputs. Equal hashes establish byte preservation during the observation window; differing hashes need attribution and must not automatically be blamed on the probe.

## 3. Capture the smallest useful failure

Record module, function, line and exception class. Include an exception message only when it exactly equals a reviewed constant literal; otherwise emit a classification code. Never dump frame locals, arbitrary exception text, rows, endpoints or credentials.

For exception tracing, use a bounded ring or exclude ordinary handled missing-file events so setup noise cannot evict the terminal cause. Save the original refusal separately from instrumentation errors.

## 4. Test one predicate without changing live policy

Freeze the observed metadata projection and run the same production predicate against synthetic inputs. Change only the suspected field or explicit threshold in that synthetic control; retain all other predicate conditions and the original live default.

For a size guard, a stat-result fixture can test boundary values without writing a huge file. Use tiny private content fixtures only for separately admitted content behavior. Do not allocate gigabytes merely to test a metadata comparison.

Record each result at its actual boundary:

- Original preflight rejects at the identified predicate.
- A one-variable synthetic control passes or rejects that predicate.
- Other stages remain unexecuted unless their own commands and receipts exist.

A successful synthetic preflight does not imply the full producer would succeed. Conversely, do not require another exception or a conveniently named helper to exist: no further failure at the tested stage is a legitimate observation.

## 5. Produce a causal receipt, not a recovery claim

Save source hashes, exact command/exit, observed metadata, individual predicate outcomes, source-linked failure location, control results, forbidden-attempt counts, before/after output hashes and explicit unexecuted stages.

Parse sanitized records according to their actual producer schema before reporting counts. Missing fields are unknown/schema mismatch, not empty data. Keep full journals and inventories in evidence rather than printing them.

Report the confirmed refusal precisely, then separate the proposed correction, its required tests/review and any live-action approval. Preserve private history and existing defaults while evaluating consumer-policy changes; an offline candidate or passing metadata control is not permission to alter the running service, replay a journal or reset the source.
