# Providers & Model Aliases

Set via `hermes model` (picker) or `hermes setup`. 35+ provider profiles ship as
plugins under `plugins/model-providers/`; user plugins of the same name override.
Full docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Providers

| Provider | Auth | Key env var(s) |
|----------|------|----------------|
| openrouter | API key | `OPENROUTER_API_KEY` |
| anthropic | API key or OAuth | `ANTHROPIC_API_KEY`; OAuth via `hermes model` / `hermes auth add anthropic --type oauth` |

**Anthropic billing caveat:** The official providers documentation states that direct Hermes Anthropic OAuth requires Claude Max plus purchased extra usage credits, consumes those extra/overage credits rather than the included Max allowance, and does not support Claude Pro on that path. API-key access is separately billed pay-per-token. OAuth support does not imply included-subscription usage. Recheck https://hermes-agent.nousresearch.com/docs/integrations/providers before billing-sensitive routing changes; do not run a paid probe without authorization.

| Provider (continued) | Auth | Key env var(s) |
|----------|------|----------------|
| nous | OAuth device code | `hermes auth add nous` (or `NOUS_API_KEY`) |
| openai-codex | OAuth | `hermes auth add openai-codex` |
| qwen-oauth | OAuth | `hermes auth add qwen-oauth` |
| minimax-oauth | OAuth | `hermes auth add minimax-oauth` |
| copilot | Token | `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` (Copilot device flow — `gh auth login` tokens do NOT work) |
| copilot-acp | External CLI | Copilot CLI on PATH or `COPILOT_CLI_PATH` |
| gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| xai | API key | `XAI_API_KEY` (SuperGrok OAuth also supported) |
| deepseek | API key | `DEEPSEEK_API_KEY` |
| zai (GLM) | API key | `GLM_API_KEY` / `ZAI_API_KEY` |
| minimax / minimax-cn | API key | `MINIMAX_API_KEY` / `MINIMAX_CN_API_KEY` |
| kimi-coding / -cn | API key | `KIMI_API_KEY` / `KIMI_CN_API_KEY` |
| alibaba (+coding-plan) | API key | `DASHSCOPE_API_KEY` / `ALIBABA_CODING_PLAN_API_KEY` |
| xiaomi | API key | `XIAOMI_API_KEY` |
| huggingface | Token | `HF_TOKEN` |
| fireworks / novita / nvidia / deepinfra / gmi / arcee / stepfun / upstage / kilocode / ai-gateway / opencode-zen / opencode-go / ollama-cloud | API key | `<NAME>_API_KEY` |
| bedrock / vertex / azure-foundry | Cloud SDK / key | AWS SDK creds / Vertex ADC / `AZURE_FOUNDRY_API_KEY` |
| custom | Config | `model.base_url` + `model.api_key` in config.yaml |

Multiple credentials per provider pool and rotate automatically (`hermes auth`).
Fallback chain when the primary fails: `hermes fallback add|remove|list`.

### Diagnose credential-pool rotation failures

1. **Bind the executing runtime before changing accounts.** Resolve the active profile, PATH-selected launcher, selected source revision and running gateway revision. A reopened TUI can reconnect to the same loaded backend, so a repaired checkout alone does not establish repaired execution. For multiple affected chats, retain an allowlisted metadata projection per session: identity/cwd, provider/model, endpoint classification, explicit-key or credential-reference presence and runtime generation. Extract it through the selected revision's saved-runtime schema, including nested envelopes such as `gateway_runtime`; a missing top-level endpoint is not proof that the resumed route is unset or noncanonical. Do not include token values, account labels, prompts or chat history.
2. **Classify the actual rejection.** Distinguish transient throttling, hard quota, model entitlement and recorded cooldown using the provider's error markers and the selected source's classifier; HTTP 429 alone is insufficient. Treat a quota widget or persisted `ok` status as an observation, not proof that an API request is available. Do not clear legitimate exhaustion, switch accounts or enable paid fallback merely to make a diagnostic pass.
3. **Trace the resumed route through agent construction.** Compare fresh resolution with restored launch parameters, session-policy binding and the kwargs actually handed to the agent. In particular, test whether an explicit *canonical provider endpoint* without an explicit account credential accidentally selects a singleton before the pool rung. A unit test of pool selection cannot detect a pool lost by an earlier resolver or omitted by a later constructor. Follow the selected revision's existing migration/policy helpers instead of recreating their mapping in the test.
4. **Observe a public-path behavioral RED with synthetic credentials.** With round-robin configured, repeated canonical resolutions must exercise both eligible fixture accounts; cover trailing-slash equivalence, cooldown exclusion, hard-cap recovery and gateway forwarding. Keep transient retry and finite all-exhausted termination as separate controls. A missing helper/import or private-home guard failure is test setup failure, not the product reproduction. Preserve intentional baseline fallback behavior rather than silently redefining it as part of this repair.
5. **Prove credential boundaries before effectful selection.** Exercise explicit key/account pins, foreign/proxy endpoints and environment/config overrides. Check both persisted row metadata and the effective loaded row generation: an environment override can mask a stored foreign URL, and rows can change between the metadata check and pool loading. Trace rejected-pool and explicit-endpoint branches through the real downstream credential resolver, raw pool fallback and quota-probe/refresh paths; a returned `credential_pool=None` does not prove that the returned token came from a singleton. In an isolated fixture with no singleton, test canonical-pool-to-foreign-endpoint and foreign/proxy-pool-to-canonical-endpoint rejection using the real resolver rather than a stub that always returns a singleton. Keep genuine permitted-singleton fallback as a separate positive control. Count forbidden selection/refresh attempts outside production catches, because a throwing sentinel alone can be swallowed and leave a broken guard green.
6. **Carry availability rules through raw fallback.** With the singleton absent, exercise recently exhausted rows without an explicit reset, elapsed and future resets, sole-credential cooldowns, DEAD rows and active model-scoped cooldowns through the real resolver. Compare the primary pool decision with the returned fallback credential: returning a token with `credential_pool=None` must not bypass a bench the pool still enforces. Reuse the maintained availability/TTL helpers rather than duplicating a raw timestamp comparison, because a missing reset timestamp does not mean availability. Keep elapsed-cooldown and genuine-singleton positive controls; an unknown quota-probe result must not clear a legitimate bench.
7. **Verify refresh custody at the authoritative store.** Build a private named-profile fixture with no local rows or singleton that borrows an expired, quota-exhausted root row. Trace owner resolution, store-specific locking, current row identity/generation and stored/effective route validation before refresh. Require the replacement single-use token pair to be durably committed to that owner before probing or exposing recovery; the active profile must not gain a shadow grant. Test both restored and still-exhausted quota responses, preserve unrelated rows, and inject a persistence failure that must stop before probe or credential return. Simulate a peer commit immediately before lock acquisition to verify newer-generation adoption and changed-route refusal without refreshing the stale pair. Assert effect counters outside catches. These are synthetic custody checks, not authorization to refresh or repair live credentials, nor independent acceptance of an implementation.
8. **Verify failed client replacement as a state transaction.** Trace the real rebuild helper's return contract and keep test stubs faithful. Inject explicit failure and exceptions; verify client, key, pool-entry identity, account headers, API mode, client kwargs and transport cache remain coherent. Do not report rotation success or clear the old transport cache merely because credential fields were assigned before a failed SDK rebuild.
9. **Isolate the proof and run the maintained checks.** Use the repository's guarded runner and private test home. In a deliberately credential-less fixture, isolate `Path.home()` and disable external CLI-login adoption in that fixture's config, not in production policy; otherwise the operator's existing login can invalidate the negative control. Preserve assertions and run the focused causal cases, related policy/client suites and applicable static checks against the final source generation. Follow `test-driven-development` for retained RED/GREEN identity reconciliation.
10. **Separate candidate proof from recovery.** Reconcile source integration, fresh imports, supported gateway activation and each session's observed route independently. Check saved route metadata against the pre-operation projection without rewriting frozen model context or replaying project work. Synthetic passes establish the routing contract, not real quota or provider availability; claim an actual successful request only when separately authorized and observed. For a recurring repair, follow the local-repair retention procedure in `references/cli-reference.md` before promising it will survive updates.

### User-defined model aliases

Work with `/model <name>` in CLI and every gateway platform. Resolved by
`hermes_cli/model_switch.py::resolve_alias()`; user aliases are checked BEFORE
the built-in table, so a user `sonnet`/`grok` shadows the built-in.

```yaml
# Full form
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  local-qwen:
    model: qwen3.5:397b
    provider: custom
    base_url: "https://ollama.com/v1"
  theta:
    model: theta-1
    provider: custom
    base_url: "https://theta.example.com/v1"
    key_env: THETA_API_KEY        # or: api_key: "${THETA_API_KEY}"

# Short form ("provider/model"), also via CLI:
#   hermes config set model.aliases.fav openrouter/anthropic/claude-sonnet-4.6
model:
  aliases:
    fav: openrouter/anthropic/claude-sonnet-4.6
```

`/model fav` — session-scoped; add `--global` to persist as default.

An alias with its own `base_url` authenticates with its own credential
(`api_key`, which also accepts a `"${VAR}"` reference, or `key_env`). With
neither set the key is resolved from the alias HOST, never carried over from
the provider that was active before the switch.

Built-in aliases (catalog-resolved against the active provider): `sonnet`,
`opus`, `haiku`, `claude`, `gpt5`, `gpt`, `codex`, `o3`, `o4`, `gemini`,
`deepseek`, `grok`, `llama`, `qwen`, `minimax`, `nemotron`, `kimi`, `glm`,
`step`, `mimo`, `trinity`.
