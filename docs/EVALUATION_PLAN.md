# Evaluation Plan

## Primary metric
**Inventory attention classification accuracy** against a predefined operational reference.

For each item/case:
- 1 = correctly identified as requiring attention or not requiring attention.
- 0 = incorrect classification.

## Secondary metrics
1. Average time per case.
2. False positives.
3. False negatives.
4. Explanation completeness.
5. Verification issues detected.

## Required evaluation set
Target: **10+ cases** where practical.

Include:
- normal case;
- low-stock case;
- high recent-demand case;
- long lead-time case;
- high variability case;
- misleading/simple case;
- at least one difficult case.

## Fairness
Use the same cases and same underlying information for the baseline and final workflow.

## Example comparison

| Metric | Baseline | Final Agent | Change |
|---|---:|---:|---:|
| Primary accuracy | [run] | [run] | [calculate] |
| Avg time/case | [run] | [run] | [calculate] |
| False negatives | [run] | [run] | [calculate] |
| Explanation completeness | [run] | [run] | [calculate] |

## Rule
Never manufacture results. If an experiment performs worse, record it in the changelog and explain what was learned.
