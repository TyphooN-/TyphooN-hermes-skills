# Multimodal qualification

Use when a candidate is intended for images, screenshots, OCR, diagrams, documents, or video. These are acceptance criteria, not claims that any particular model has passed them.

## Verify the complete image path first

1. Trace the intended image consumer before proposing downloads or provider changes. Resolve the main chat preset, auxiliary vision route and any provider-native image path separately, then inventory already configured local vision weights/projectors with stat-only checks before acquiring anything. Inspect the exact derivative's architecture and packaged files: check whether vision weights are retained, whether the runtime needs a separate projector, and whether that projector is compatible with the language-model revision. A text-only selected preset is not proof that every installed model is text-only, that the provider-native image path failed or that another download is required. File presence and compatible configuration identify candidates, not working vision.
2. Trace the served request contract through the processor, chat template, image markers, and encoder/projector. Check that image content is actually consumed rather than silently reduced to a text-only prompt.
3. Record image resolution, resizing/tiling, image-token budget, and multi-image limits. Keep them comparable in an A/B test; different preprocessing can dominate the apparent model-quality difference.
4. Confirm that the candidate's supported image path reaches the intended hardware backend and fits its per-device budget. A language GGUF plus an unrelated projector is not a qualified pair.

## Acceptance matrix

| Surface | Evidence to capture | Regression it detects |
|---|---|---|
| Basic perception | Ground-truth objects, positions, and counts in an image | Model ignores or misreads image content |
| Small-text OCR | Exact strings from known screenshots/documents at declared resolution | Quantization, preprocessing, or encoder changes lose text detail |
| Tables and charts | Known cell values, labels, units, and relationships | Plausible prose substitutes for extraction or spatial reasoning |
| Desktop screenshots | Requested element and its observed location | Captioning is mistaken for UI grounding |
| Multiple images | Correct cross-image comparison and attribution | Images are dropped, confused, or reordered |
| Unanswerable visual question | Explicit uncertainty when evidence is absent | Confident visual hallucination |
| Structured output | Valid requested schema plus correct image-derived values | JSON syntax passes while extracted content is wrong |
| Resource lifecycle | Peak per-device memory, latency, unload/recovery, and child cleanup | Functional success masks operational failure |

Use public or synthetic fixtures with known answers unless private media is explicitly in scope. Keep the fixture set and expected results versioned. Evaluate a decensored derivative on visual quality as well as refusal behavior; refusal reduction alone does not prove retained image reasoning.

## Audit existing evidence before choosing a comparison

1. Read the benchmark's exact argv and omissions before reusing its numbers. A native text benchmark that never loaded the projector measures neither image latency nor vision quality; a vision-named alias does not change the measured workload.
2. Compare measured and served context, KV types, placement, flash attention and speculative decoding. A weight-file benchmark can bypass the serving preset, so report it as historical text throughput rather than present multimodal performance when those settings differ.
3. Identify what an image smoke test actually proves. One exact button-label response proves that a particular image path answered that fixture, not reliable OCR, coordinate grounding, multi-image reasoning or a model ranking.
4. Verify benchmark/report meaning in addition to process exit. A conditional-fallback gate can return success after recording missed targets; consume its hit counts, per-case verdicts and fallback decision rather than equating exit zero with task acceptance.
5. Treat a publisher's statement that vision or MTP was preserved as a retention claim. Pin and exercise the local quantization/projector pair; restored base components and text/refusal scores do not establish that derivative's visual accuracy.

## Report boundaries

- Mark publisher benchmark tables as publisher evidence, not local scores.
- Mark tests of the base model separately from tests of a derivative or quantization.
- Mark absent CUDA/HIP/MIG hardware as unassessed rather than interpreting parser fixtures as a hardware pass.
- Recommend separate fast and quality roles only when the task evidence and memory/latency budget justify them; do not multiply model residency merely to fill the catalog.
