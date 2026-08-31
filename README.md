# AI Inventory Control Agent — micro1 Agentic Workflows Hackathon

## 1. Project idea

**AI Inventory Control Agent for Stockout Risk and Reorder Decision Support**

### Intended user
Inventory Control Officers / Supply Chain Officers / Procurement Officers.

### Problem
Inventory teams must repeatedly review stock levels, recent consumption, lead times and safety stock to identify items that need attention. A manual review can be slow and can miss changing demand patterns.

### Proposed solution
A multi-agent workflow:
**Data Agent → Inventory Risk Agent → Verification Agent → Report Agent**

The workflow analyzes inventory history, identifies risk, calculates a decision-support reorder quantity, verifies the result, and produces an evidence-based report.

**Important:** the system does not place purchase orders. Recommendations require human approval.

---

## 2. Why this matches the hackathon brief

The hackathon asks for:
- a specific meaningful problem and user;
- purposeful agent design;
- a fair baseline comparison;
- an improvement changelog;
- a primary evaluation metric;
- reproducibility;
- complete code, reproduction guide, a short video, and representative agent trajectories.

This project is structured around those requirements.

---

## 3. Repository structure

```
AI_Inventory_Control_Agent/
├── data/
│   └── inventory_history.csv
├── src/
│   ├── inventory_agent.py
│   └── evaluate.py
├── prompts/
│   ├── data_agent.txt
│   ├── inventory_risk_agent.txt
│   ├── verification_agent.txt
│   └── report_agent.txt
├── docs/
│   ├── REPRODUCTION_GUIDE.md
│   ├── IMPROVEMENT_CHANGELOG.md
│   ├── VIDEO_SCRIPT.md
│   ├── AGENT_TRAJECTORIES.md
│   ├── EVALUATION_PLAN.md
│   └── SUBMISSION_CHECKLIST.md
├── outputs/
└── README.md
```

---

## 4. Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run the workflow:
```bash
python src/inventory_agent.py
```

Run evaluation:
```bash
python src/evaluate.py
```

The generated report is saved to:
`outputs/inventory_report.json`

---

## 5. Primary metric

Primary outcome:
**correct identification of inventory cases requiring attention against a predefined evaluation reference.**

Supporting metrics:
- analysis time per case;
- false positives/false negatives;
- number of verification issues;
- recommendation explanation completeness.

Before the final hackathon submission, run the baseline and final workflow over at least 10 approved evaluation cases where practical, including a difficult case. The included synthetic demonstration is only a development artifact; its numbers must not be presented as final hackathon performance unless they are reproduced and accepted as the evaluation set.

---

## 6. Baseline

The baseline is deliberately simple:
- inspect only the latest stock;
- flag an item when stock is below safety stock;
- no recent-demand analysis;
- no lead-time reasoning;
- no verification agent;
- no structured evidence report.

The final workflow receives the same input cases and uses additional tools/agents.

---

## 7. Safety and governance

This is decision support, not autonomous purchasing.

Human approval is required before consequential procurement actions.

Do not place credentials, private customer information, confidential company records, or unauthorized data in the submission.

The included dataset is synthetic.

---

## 8. What must still be customized before submission

1. Replace the placeholder/team information with your real details.
2. Run the workflow and evaluation yourself.
3. Add at least 10 final evaluation cases where practical.
4. Record actual runtime and cost.
5. Capture actual agent trajectories from your runs.
6. Record the final 5-minute demo.
7. Update the changelog with your actual experiments and measured results.
8. Only claim performance numbers supported by your run evidence.
