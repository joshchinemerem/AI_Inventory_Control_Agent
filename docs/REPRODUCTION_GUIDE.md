# Reproduction Guide

## Environment
- Python: 3.10+
- pandas
- numpy

## Setup

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

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run baseline/evaluation

```bash
python src/evaluate.py
```

Expected output:
a JSON file at `outputs/evaluation_results.json`.

## Run final workflow

```bash
python src/inventory_agent.py
```

Expected output:
`outputs/inventory_report.json`

The report contains:
- items reviewed;
- risk counts;
- findings;
- evidence;
- verification notes;
- human-approval requirement.

## Data

The included dataset is synthetic and contains 30 days of inventory history for 10 items.

Required columns:
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

## Reproducing the hackathon evaluation

1. Put the same approved evaluation cases into the evaluation dataset.
2. Run the baseline.
3. Run the final workflow.
4. Record the primary metric for every case.
5. Record runtime for both approaches.
6. Preserve all failures rather than deleting them.
7. Generate a final comparison table.
8. Attach the evidence to the README/changelog.

Do not modify evaluation cases after seeing results.

## Approximate runtime/cost

For the included deterministic demonstration, runtime and cost depend on the local machine and are effectively local-compute only. If an external LLM is added later, record the actual model, API cost and runtime from the final run.
