# Representative Agent Trajectories

The hackathon requires representative trajectories for every agent used. Capture these from actual runs for the final submission.

## Trajectory 1 — Data Agent
Input:
`inventory_history.csv`

Actions:
1. Load dataset.
2. Validate required columns.
3. Parse dates.
4. Sort by item/date.
5. Return validated data.

Evidence to capture:
- input;
- validation result;
- any data-quality warning;
- output passed to the next agent.

## Trajectory 2 — Inventory Risk Agent
Input:
validated inventory history.

Actions:
1. Group by item.
2. Calculate 7-day demand.
3. Calculate days of cover.
4. Calculate lead-time demand.
5. Calculate reorder point.
6. Assign risk level.
7. Generate evidence/reasons.
8. Recommend a quantity for human review.

Evidence to capture:
- calculation/tool output;
- selected evidence;
- final finding.

## Trajectory 3 — Verification Agent
Input:
risk findings.

Actions:
1. Check recommendation arithmetic.
2. Check risk/evidence consistency.
3. Check missing explanations.
4. Record corrections/issues.

Evidence to capture:
- finding before verification;
- verification check;
- issue/correction;
- verified finding.

## Trajectory 4 — Report Agent
Input:
verified findings.

Actions:
1. Prioritize critical/high-risk items.
2. Format evidence.
3. Produce decision-support report.
4. Mark human approval requirement.

Evidence to capture:
- verified input;
- report generation;
- final report.

## What to show in the video
Do not merely show the final answer. Show one complete execution so judges can see the workflow and the role of each agent.
