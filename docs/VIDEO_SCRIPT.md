# 5-Minute Hackathon Video Script

## 0:00–0:35 — Problem
“Inventory officers regularly review stock, demand, lead times and safety stock to decide which items need attention. The bottleneck is that this review can be repetitive and can miss changing demand patterns. My project is an AI Inventory Control Agent for stockout-risk and reorder decision support.”

Show the input inventory file.

## 0:35–1:00 — Baseline
“The baseline uses a simple rule: flag an item when current stock is below safety stock. It does not reason about recent demand, lead time or verification.”

Show the baseline result.

## 1:00–3:15 — Final agent workflow
Show:
Data Agent → Inventory Risk Agent → Verification Agent → Report Agent.

Explain one realistic case from input to final report.

Show:
- recent demand;
- days of cover;
- lead-time demand;
- reorder point;
- risk;
- verification;
- recommendation.

State clearly:
“The recommendation is decision support. A human must approve any consequential procurement action.”

## 3:15–4:10 — Evaluation
Show the same evaluation cases run through baseline and final workflow.

Show the actual table:
- primary metric;
- time per case;
- false positives/negatives;
- verification issues.

Only use measured results.

## 4:10–4:45 — Changelog
“First I established the baseline. Then I added recent-demand context, lead-time reasoning, reorder calculation and verification. I retained the changes that improved the measured outcome and removed/revised experiments that did not.”

Show the changelog.

## 4:45–5:00 — Hot take
“My main lesson from the experiments was [actual observed lesson]. The most valuable part was not simply adding more agents; it was [actual evidence-backed finding].”
