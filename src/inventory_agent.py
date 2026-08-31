
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd
import numpy as np
import json, argparse

ROOT = Path(__file__).resolve().parents[1]

@dataclass
class Finding:
    item_code: str
    item_name: str
    risk_level: str
    days_of_cover: float
    avg_daily_demand: float
    projected_lead_time_demand: float
    recommended_order_qty: float
    reasons: list[str]
    evidence: dict

class DataAgent:
    name = "Data Agent"
    def run(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        required = {"date","item_code","item_name","category","unit",
                    "stock_on_hand","daily_demand","receipts","lead_time_days","safety_stock"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        df["date"] = pd.to_datetime(df["date"])
        return df.sort_values(["item_code","date"])

class AnalysisAgent:
    name = "Inventory Risk Agent"
    def run(self, df: pd.DataFrame) -> list[Finding]:
        findings = []
        for code, g in df.groupby("item_code"):
            g = g.sort_values("date")
            latest = g.iloc[-1]
            avg30 = float(g["daily_demand"].mean())
            avg7 = float(g.tail(7)["daily_demand"].mean())
            variability = float(g["daily_demand"].std(ddof=0))
            lead = float(latest["lead_time_days"])
            safety = float(latest["safety_stock"])
            stock = float(latest["stock_on_hand"])
            days_cover = stock / max(avg7, 1e-9)
            lead_demand = avg7 * lead
            reorder_point = lead_demand + safety
            # Conservative order quantity: replenish to 30 days of recent demand.
            target = avg7 * 30 + safety
            order_qty = max(0.0, target - stock)

            reasons = []
            if stock <= reorder_point:
                reasons.append("stock is at or below the reorder point")
            if days_cover <= lead:
                reasons.append("days of cover is no greater than supplier lead time")
            if avg7 > avg30 * 1.15:
                reasons.append("recent demand is materially above the 30-day average")
            if variability > avg30 * 0.25:
                reasons.append("demand variability is relatively high")

            if days_cover <= lead * 0.75:
                risk = "CRITICAL"
            elif days_cover <= lead:
                risk = "HIGH"
            elif days_cover <= lead * 1.5:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            findings.append(Finding(
                item_code=code,
                item_name=str(latest["item_name"]),
                risk_level=risk,
                days_of_cover=round(days_cover,2),
                avg_daily_demand=round(avg7,2),
                projected_lead_time_demand=round(lead_demand,2),
                recommended_order_qty=round(order_qty,2),
                reasons=reasons or ["stock position currently provides more cover than the defined lead-time threshold"],
                evidence={
                    "latest_stock": round(stock,2),
                    "30_day_avg_demand": round(avg30,2),
                    "7_day_avg_demand": round(avg7,2),
                    "lead_time_days": lead,
                    "safety_stock": safety,
                    "reorder_point": round(reorder_point,2),
                    "demand_std": round(variability,2),
                }
            ))
        return findings

class VerificationAgent:
    name = "Verification Agent"
    def run(self, findings: list[Finding]) -> tuple[list[Finding], list[str]]:
        issues = []
        verified = []
        for f in findings:
            if f.recommended_order_qty < 0:
                issues.append(f"{f.item_code}: negative order quantity corrected to zero")
                f.recommended_order_qty = 0
            if f.days_of_cover < 0:
                issues.append(f"{f.item_code}: negative days-of-cover detected")
            if f.risk_level in {"CRITICAL","HIGH"} and not f.reasons:
                issues.append(f"{f.item_code}: high risk without an explanation")
            verified.append(f)
        return verified, issues

class ReportAgent:
    name = "Report Agent"
    def run(self, findings: list[Finding], verification_issues: list[str], output_path: str):
        priority = {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3}
        ordered = sorted(findings, key=lambda x:(priority[x.risk_level], -x.days_of_cover))
        report = {
            "title": "AI Inventory Control Agent — Inventory Risk Report",
            "method": "Data Agent → Inventory Risk Agent → Verification Agent → Report Agent",
            "summary": {
                "items_reviewed": len(findings),
                "critical": sum(x.risk_level=="CRITICAL" for x in findings),
                "high": sum(x.risk_level=="HIGH" for x in findings),
                "medium": sum(x.risk_level=="MEDIUM" for x in findings),
                "low": sum(x.risk_level=="LOW" for x in findings),
                "verification_issues": len(verification_issues),
            },
            "findings": [asdict(x) for x in ordered],
            "verification_notes": verification_issues,
            "human_approval_required": True,
        }
        Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

class InventoryWorkflow:
    def __init__(self):
        self.data_agent = DataAgent()
        self.analysis_agent = AnalysisAgent()
        self.verification_agent = VerificationAgent()
        self.report_agent = ReportAgent()

    def run(self, csv_path: str, output_path: str):
        df = self.data_agent.run(csv_path)
        findings = self.analysis_agent.run(df)
        findings, issues = self.verification_agent.run(findings)
        return self.report_agent.run(findings, issues, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(ROOT/"data"/"inventory_history.csv"))
    parser.add_argument("--output", default=str(ROOT/"outputs"/"inventory_report.json"))
    args = parser.parse_args()
    report = InventoryWorkflow().run(args.data, args.output)
    print(json.dumps(report["summary"], indent=2))
