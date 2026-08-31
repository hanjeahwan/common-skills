# Output Execution Runs

This report records how output-eval variants were produced and whether timing or token evidence is observed or estimated.

- Cases: `3`
- Variant runs: `6`
- Command executed: `6`
- Model executed: `6`
- Recorded fixtures: `0`
- Timing observed: `6`
- Token observed: `6`
- Token estimated: `0`
- Delta: `11.11`
- Gate pass: `True`

Command runner evidence is present. This proves the eval harness executed an external command, but it is not provider-backed model evidence unless the runner reports model metadata.

## Runs

| Case | Variant | Mode | Model | Duration ms | Tokens | Score | Status |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| bootstrap-without-empty-domains | baseline | model | gpt-5.6-sol | 7450.16 | 585 | 0.0 | pass |
| bootstrap-without-empty-domains | with_skill | model | gpt-5.6-sol | 9249.07 | 2204 | 0.0 | pass |
| reject-parallel-domain-entry | baseline | model | gpt-5.6-sol | 5560.11 | 1025 | 0.0 | pass |
| reject-parallel-domain-entry | with_skill | model | gpt-5.6-sol | 6477.88 | 2084 | 33.33 | pass |
| migrate-implemented-proposal-truth | baseline | model | gpt-5.6-sol | 10164.76 | 1084 | 0.0 | pass |
| migrate-implemented-proposal-truth | with_skill | model | gpt-5.6-sol | 10636.41 | 2256 | 0.0 | pass |

## Next Fixes

- Keep recorded fixtures as reproducible baselines, but do not describe them as model-executed evidence.
- Use `scripts/provider_output_eval_runner.py` for provider-backed holdout cases when release confidence depends on real generation behavior.
- Compare timing, token cost, and assertion deltas before promoting a skill to governed reuse.
