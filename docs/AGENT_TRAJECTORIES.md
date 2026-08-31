# Representative Agent Trajectories

## Purpose

This document describes representative executions of each component in the AI Inventory Control Agent workflow.

The workflow consists of:

Data Agent → Inventory Risk Agent → Verification Agent → Report Agent

The trajectories are based on the actual workflow implemented in the repository.

---

## Trajectory 1 — Data Agent

### Input

data/inventory_history.csv

### Actions

1. Load the inventory history CSV file.
2. Validate the required columns.
3. Convert the date column to datetime format.
4. Sort the data by item code and date.
5. Return the validated dataset to the Inventory Risk Agent.

### Required fields validated

- date
- item_code
- item_name
- category
- unit
- stock_on_hand
- daily_demand
- receipts
- lead_time_days
- safety_stock

### Output

Validated and chronologically sorted inventory data.

### Evidence

The workflow successfully processed the inventory dataset and reviewed 12 inventory items during the development run.

---

## Trajectory 2 — Inventory Risk Agent

### Input

Validated inventory history from the Data Agent.

### Actions

1. Group records by item code.
2. Identify the latest inventory record.
3. Calculate recent 7-day average demand.
4. Calculate 30-day average demand.
5. Calculate demand variability.
6. Calculate days of cover.
7. Calculate projected lead-time demand.
8. Calculate reorder point.
9. Compare stock coverage with supplier lead time.
10. Assign an inventory risk level.
11. Generate reasons supporting the classification.
12. Calculate a recommended replenishment quantity for human review.

### Risk levels

- CRITICAL
- HIGH
- MEDIUM
- LOW

### Example actual finding

Item:

RM-003 — Sugar

Observed evidence:

- Latest stock: 0.00
- 7-day average demand: 96.43
- Lead time: 8 days
- Days of cover: 0.00
- Reorder point: 779.41
- Risk level: CRITICAL
- Recommended order quantity: 2900.77

The finding is supported by the stock position being at or below the reorder point and the days of cover being no greater than supplier lead time.

### Output

A structured inventory finding containing:

- risk level;
- days of cover;
- average demand;
- projected lead-time demand;
- recommended order quantity;
- reasons;
- supporting evidence.

---

## Trajectory 3 — Verification Agent

### Input

Inventory findings produced by the Inventory Risk Agent.

### Actions

1. Check whether recommended order quantities are negative.
2. Check whether days of cover are negative.
3. Check whether high-risk findings contain explanations.
4. Record any detected issues or corrections.
5. Pass the verified findings to the Report Agent.

### Actual development-run result

Verification issues detected:

0

No corrections were required during the successful development run.

### Output

Verified inventory findings with verification notes.

---

## Trajectory 4 — Report Agent

### Input

Verified inventory findings.

### Actions

1. Sort findings according to risk priority.
2. Place critical findings before lower-risk findings.
3. Include supporting evidence.
4. Include explanations for the risk classification.
5. Include recommended replenishment quantities.
6. Include verification notes.
7. Mark the report as requiring human approval.

### Actual development-run result

The workflow reviewed:

12 items

Risk distribution:

- Critical: 7
- High: 0
- Medium: 1
- Low: 4
- Verification issues: 0

### Output

The final report is generated at:

outputs/inventory_report.json

The report contains:

- project title;
- workflow method;
- inventory summary;
- item-level findings;
- evidence;
- verification notes;
- human approval requirement.

---

## End-to-End Workflow

The complete execution is:

```text
inventory_history.csv
        ↓
   Data Agent
        ↓
Validated inventory data
        ↓
Inventory Risk Agent
        ↓
Risk findings and recommendations
        ↓
Verification Agent
        ↓
Verified findings
        ↓
Report Agent
        ↓
inventory_report.json