
# Evaluation Plan

## 1. Objective

The evaluation measures how accurately the inventory workflow identifies cases that require operational attention compared with a predefined reference classification.

The evaluation compares a simple baseline approach with the final inventory workflow using the same evaluation cases.

## 2. Primary Metric

Inventory attention classification accuracy

For each evaluation case:

- 1 = the system correctly identifies whether the inventory case requires attention.
- 0 = the system incorrectly classifies the case.

Accuracy is calculated as:

Accuracy = Correct Classifications / Total Evaluation Cases

## 3. Secondary Metrics

The evaluation also considers:

1. False positives.
2. False negatives.
3. Explanation completeness.
4. Verification issues detected.
5. Average analysis time per case, where measured.

## 4. Evaluation Set

The development evaluation contains:

12 synthetic inventory cases.

The cases represent different inventory conditions, including:

- low stock;
- changing recent demand;
- supplier lead time;
- stock coverage;
- demand variability;
- cases that may not be identified by a simple stock-level rule.

The synthetic dataset is included in:

data/inventory_history.csv

## 5. Fair Baseline Comparison

The baseline and final workflow are evaluated against the same underlying cases.

### Baseline

The baseline uses a simple inventory rule based primarily on the latest stock level compared with safety stock.

It does not use the complete lead-time, recent-demand, days-of-cover, verification, and structured reporting workflow.

### Final Workflow

The final workflow consists of:

Data Agent
     ↓
Inventory Risk Agent
     ↓
Verification Agent
     ↓
Report Agent

It incorporates:

- recent demand;
- 30-day demand average;
- 7-day demand average;
- demand variability;
- supplier lead time;
- days of cover;
- lead-time demand;
- reorder point;
- recommended replenishment quantity;
- verification;
- evidence-based reporting.

## 6. Development Evaluation Results

The evaluation was executed successfully using:

python .\src\evaluate.py

Observed result:

Evaluation cases:             12
Baseline accuracy:            0.583
Final workflow accuracy:      1.000
Baseline false negatives:     5
Final false negatives:        0

### Comparison

| Metric | Baseline | Final Workflow | Change |
|---|---:|---:|---:|
| Evaluation cases | 12 | 12 | Same cases |
| Attention classification accuracy | 58.3% | 100.0% | +41.7 percentage points |
| False negatives | 5 | 0 | -5 |
| Verification issues | Not applicable | 0 | — |

The final workflow achieved higher accuracy and fewer false negatives than the baseline on the included 12-case synthetic development evaluation.

## 7. Evaluation Artifacts

The repository contains the generated evaluation outputs:

outputs/case_level_results.csv
outputs/evaluation_results.csv
outputs/evaluation_results.json

These files provide supporting evidence for the development evaluation.

## 8. Reproducibility

The evaluation can be reproduced from the repository using:

python .\src\evaluate.py

The inventory workflow itself can be reproduced using:

python .\src\inventory_agent.py

The workflow generates:

outputs/inventory_report.json

## 9. Interpretation

The development results indicate that the final workflow performed better than the simple baseline on the included synthetic cases.

However, the result should be interpreted carefully.

The evaluation:

- uses synthetic data;
- contains 12 cases;
- does not establish performance on real-world inventory data;
- does not establish production readiness;
- does not measure long-term stockout prevention.

Therefore, the 100% result is reported only as the result of the included development evaluation.

## 10. Limitations and Future Evaluation

Before production use, the workflow should be evaluated using historical operational inventory data containing known stockout, replenishment, and demand outcomes.

Future evaluation should include:

- a larger evaluation set;
- real historical inventory cases where authorized;
- organization-specific safety-stock policies;
- different supplier lead times;
- seasonal demand patterns;
- unexpected demand spikes;
- missing or inconsistent data;
- measurement of runtime;
- measurement of operational impact.

## 11. Governance

The system is a decision-support tool.

It does not automatically:

- create purchase orders;
- approve purchases;
- contact suppliers;
- transfer funds;
- execute procurement transactions.

Human approval is required before consequential procurement decisions.