# AI Inventory Control Agent

**AI Inventory Control Agent for Stockout Risk Detection and Reorder Decision Support**

## 1. Overview

The AI Inventory Control Agent is a multi-agent inventory decision-support system designed to help inventory, supply chain, and procurement teams identify stockout risks and prioritize replenishment decisions.

The system analyzes historical inventory data, recent demand, stock levels, supplier lead times, and safety stock to determine the risk level of each inventory item.

It produces an evidence-based inventory risk report containing:

* Inventory risk classification
* Days of stock cover
* Recent average demand
* Projected lead-time demand
* Reorder point
* Recommended reorder quantity
* Reasons supporting each risk classification
* Verification results

The system is designed for **decision support**. It does not automatically create or place purchase orders. Final procurement decisions remain subject to human approval.

---

## 2. Problem Statement

Inventory teams regularly need to determine which materials require immediate attention.

Manual inventory reviews can become difficult when teams must simultaneously consider:

* Current stock levels
* Recent consumption patterns
* Supplier lead times
* Safety stock
* Demand variability
* Changing demand trends

A simple stock-level check may fail to identify items whose recent demand is increasing rapidly.

This project addresses the problem by combining recent demand analysis, stock coverage, lead-time requirements, and verification into a structured workflow.

---

## 3. Solution

The system uses four cooperating components:

```text
Data Agent
     ↓
Inventory Risk Agent
     ↓
Verification Agent
     ↓
Report Agent
```

### Data Agent

Loads and validates the inventory history dataset.

It checks that the required fields are available and converts the date field into a usable datetime format.

### Inventory Risk Agent

Analyzes each inventory item using:

* 30-day average demand
* 7-day average demand
* Demand variability
* Current stock
* Supplier lead time
* Safety stock
* Days of cover
* Reorder point

The agent assigns one of four risk levels:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

It also calculates a recommended replenishment quantity based on the recent-demand target.

### Verification Agent

Checks the generated findings for basic consistency issues, including:

* Negative recommended order quantities
* Negative days of cover
* High-risk findings without explanations

### Report Agent

Organizes the verified findings by priority and generates a structured JSON inventory risk report.

The report is saved to:

```text
outputs/inventory_report.json
```

---

## 4. Risk Logic

The system calculates days of cover as:

```text
Days of Cover = Current Stock / Average Daily Demand
```

Recent demand is calculated using the latest seven days of demand.

Projected lead-time demand is:

```text
Projected Lead-Time Demand =
Average Daily Demand × Supplier Lead Time
```

The reorder point is:

```text
Reorder Point =
Projected Lead-Time Demand + Safety Stock
```

The system also compares recent seven-day demand with the 30-day average to identify significant increases in demand.

Risk classification is based primarily on the relationship between days of cover and supplier lead time.

```text
CRITICAL → Days of cover ≤ 75% of lead time

HIGH     → Days of cover ≤ lead time

MEDIUM   → Days of cover ≤ 150% of lead time

LOW      → Days of cover > 150% of lead time
```

These rules provide a transparent and reproducible decision-support mechanism.

---

## 5. Dashboard

The project includes a Streamlit dashboard for interactive inventory analysis.

Run it with:

```bash
streamlit run src/app.py
```

The dashboard provides an operational view of:

* Total items reviewed
* Critical-risk items
* High-risk items
* Medium-risk items
* Low-risk items
* Inventory risk distribution
* Reorder recommendations
* Evidence supporting each recommendation

The dashboard also maintains the human-approval requirement for procurement decisions.

---

## 6. Evaluation

The project includes a separate evaluation workflow:

```bash
python src/evaluate.py
```

The current development evaluation contains 12 synthetic cases.

The development run produced:

```text
Evaluation cases:             12
Baseline accuracy:            0.583
Final workflow accuracy:      1.000
Baseline false negatives:     5
Final false negatives:        0
```

These figures are **development evaluation results**, not a claim of performance on real-world inventory data.

The project includes evaluation artifacts in:

```text
outputs/
├── case_level_results.csv
├── evaluation_results.csv
└── evaluation_results.json
```

A final submission evaluation should be performed on the approved evaluation set used for the hackathon.

---

## 7. Baseline

The baseline represents a simpler inventory-review approach.

It primarily checks the latest stock level against safety stock and does not incorporate the complete workflow used by the final system.

The final workflow adds:

* Recent-demand analysis
* Lead-time reasoning
* Days-of-cover analysis
* Reorder-point calculation
* Demand variability
* Verification
* Structured evidence reporting

This provides a basis for comparing the improved workflow with a simpler approach.

---

## 8. Dataset

The included dataset is synthetic and is provided for demonstration and reproducibility.

Dataset:

```text
data/inventory_history.csv
```

The dataset contains inventory history including:

* Date
* Item code
* Item name
* Category
* Unit
* Stock on hand
* Daily demand
* Receipts
* Lead time
* Safety stock

No private customer information or confidential company records are included.

---

## 9. Repository Structure

```text
AI_Inventory_Control_Agent/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   └── inventory_history.csv
│
├── docs/
│   ├── AGENT_TRAJECTORIES.md
│   ├── EVALUATION_PLAN.md
│   ├── IMPROVEMENT_CHANGELOG.md
│   ├── REPRODUCTION_GUIDE.md
│   ├── SUBMISSION_CHECKLIST.md
│   └── VIDEO_SCRIPT.md
│
├── outputs/
│   ├── case_level_results.csv
│   ├── evaluation_results.csv
│   ├── evaluation_results.json
│   └── inventory_report.json
│
├── prompts/
│   ├── data_agent.txt
│   ├── inventory_risk_agent.txt
│   ├── report_agent.txt
│   └── verification_agent.txt
│
└── src/
    ├── app.py
    ├── evaluate.py
    └── inventory_agent.py
```

---

## 10. Installation

### Clone the repository

```bash
git clone https://github.com/joshchinemerem/AI_Inventory_Control_Agent.git
cd AI_Inventory_Control_Agent
```

### Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 11. Run the Inventory Workflow

Run:

```bash
python src/inventory_agent.py
```

The workflow generates:

```text
outputs/inventory_report.json
```

A successful run produces a summary similar to:

```text
items_reviewed: 12
critical: 7
high: 0
medium: 1
low: 4
verification_issues: 0
```

---

## 12. Run the Evaluation

Run:

```bash
python src/evaluate.py
```

The evaluation compares the baseline and final workflow against the development reference cases.

---

## 13. Run the Dashboard

Start Streamlit:

```bash
streamlit run src/app.py
```

Then open the local Streamlit address displayed in the terminal.

---

## 14. Human Approval and Governance

The system is designed as **inventory decision support rather than autonomous procurement**.

The agent can recommend that an item requires replenishment, but it does not:

* Create purchase orders
* Approve purchases
* Contact suppliers
* Transfer funds
* Execute procurement transactions

Human approval is required before consequential procurement actions.

---

## 15. Reproducibility

The repository contains the components required to reproduce the development workflow:

* Source code
* Synthetic dataset
* Agent prompts
* Evaluation scripts
* Evaluation outputs
* Inventory report
* Documentation
* Reproduction guide

For detailed reproduction instructions, see:

```text
docs/REPRODUCTION_GUIDE.md
```

---

## 16. Project Documentation

Additional project documentation is available in the `docs/` directory:

| Document                   | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| `REPRODUCTION_GUIDE.md`    | Instructions for reproducing the workflow |
| `EVALUATION_PLAN.md`       | Evaluation methodology                    |
| `IMPROVEMENT_CHANGELOG.md` | Record of workflow improvements           |
| `AGENT_TRAJECTORIES.md`    | Representative workflow trajectories      |
| `VIDEO_SCRIPT.md`          | Demonstration video structure             |
| `SUBMISSION_CHECKLIST.md`  | Final submission checklist                |

---

## 17. Project Status

The current implementation successfully runs the complete inventory workflow and Streamlit dashboard.

The development evaluation has also been executed successfully.

Before final submission, the approved hackathon evaluation set, final evidence, and demonstration materials should be reviewed and updated with the actual results from the final run.

---

## 18. License

This project is provided for demonstration and hackathon purposes.
