# Improvement Changelog

## Purpose

This document records the progression from the simple baseline inventory rule to the final multi-agent inventory decision-support workflow.

All reported evaluation results below come from the 12-case synthetic development evaluation included in this repository.

## Experimental Progression

| Stage | What was tried and why | Evidence | Decision / learning |
|---|---|---|---|
| Baseline | Compared latest stock against safety stock using a simple stock-level rule. | Baseline accuracy: 0.583; false negatives: 5/12. | The simple rule missed several inventory cases requiring attention. |
| Iteration 1 | Added recent 7-day demand analysis to capture changing consumption patterns. | Implemented in the Inventory Risk Agent. | Retained because recent demand provides additional information beyond latest stock. |
| Iteration 2 | Added supplier lead time and days-of-cover reasoning. | Implemented in the Inventory Risk Agent. | Retained because stock coverage relative to lead time is important for stockout-risk detection. |
| Iteration 3 | Added lead-time demand, reorder point, and recommended replenishment quantity. | Implemented in the final workflow and included in the generated inventory report. | Retained as decision-support information for human review. |
| Iteration 4 | Added the Verification Agent to check recommendations and explanations for basic consistency issues. | Final run reported 0 verification issues. | Retained as a safeguard before report generation. |
| Final | Combined data validation, inventory risk analysis, verification, and structured reporting. | Final accuracy: 1.000; false negatives: 0/12. | The combined workflow performed better than the simple baseline on the development evaluation. |

## Development Evaluation Result

The final development evaluation contained 12 synthetic cases.

| Metric | Baseline | Final Workflow |
|---|---:|---:|
| Evaluation cases | 12 | 12 |
| Attention classification accuracy | 0.583 | 1.000 |
| False negatives | 5 | 0 |

The final workflow therefore improved the measured development accuracy from 58.3% to 100.0% and reduced false negatives from 5 to 0.

These results apply only to the included synthetic development evaluation. They should not be interpreted as performance on real-world inventory data.

## Main Failure Mode

The baseline's main failure mode was relying primarily on the latest stock level compared with safety stock. This can miss situations where recent demand, supplier lead time, or stock coverage indicates a higher operational risk.

The final workflow addresses this limitation by considering recent demand, days of cover, lead-time demand, reorder point, and demand variability.

A remaining limitation is that the risk rules are deterministic and based on the available synthetic data. Real-world deployment would require validation against historical operational outcomes and organization-specific inventory policies.

## Key Design Lesson

The development evaluation suggests that the important improvement was not simply adding more components, but combining multiple relevant inventory signals into a transparent decision-support workflow.

Recent demand and lead-time-aware stock coverage provide information that a simple latest-stock-versus-safety-stock rule does not capture. The Verification Agent then provides an additional consistency check before the report is produced.

Future work should validate these rules against real historical stockout and replenishment outcomes and investigate whether organization-specific thresholds improve generalization.

## Limitations

- The current evaluation uses synthetic data.
- The evaluation set is limited to 12 development cases.
- Runtime and monetary execution cost were not separately measured.
- The workflow provides recommendations but does not execute procurement actions.
- Human approval remains required before consequential procurement decisions.