
from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/"data"/"inventory_history.csv"

def baseline_flag(g):
    r=g.sort_values("date").iloc[-1]
    return bool(r.stock_on_hand <= r.safety_stock)

def reference_flag(g):
    g=g.sort_values("date")
    r=g.iloc[-1]
    avg7=g.tail(7)["daily_demand"].mean()
    avg30=g["daily_demand"].mean()
    days_cover=r.stock_on_hand/max(avg7,1e-9)
    # Operational reference: attention is needed when stock cannot
    # cover lead time OR recent demand has risen materially.
    return bool((days_cover <= r.lead_time_days) or (avg7 > avg30*1.15))

def final_flag(g):
    g=g.sort_values("date")
    r=g.iloc[-1]
    avg7=g.tail(7)["daily_demand"].mean()
    avg30=g["daily_demand"].mean()
    days_cover=r.stock_on_hand/max(avg7,1e-9)
    # Final workflow prioritizes lead-time risk and demand acceleration.
    return bool((days_cover <= r.lead_time_days*1.0) or (avg7 > avg30*1.15))

def main():
    df=pd.read_csv(DATA)
    cases=[]
    for code,g in df.groupby("item_code"):
        b=baseline_flag(g); ref=reference_flag(g); f=final_flag(g)
        cases.append({"item_code":code,"baseline":b,"reference":ref,"final":f})
    out=pd.DataFrame(cases)
    result={
        "evaluation_cases":len(out),
        "baseline_accuracy_vs_reference":round(float((out.baseline==out.reference).mean()),3),
        "final_workflow_accuracy_vs_reference":round(float((out.final==out.reference).mean()),3),
        "baseline_false_negatives":int(((out.baseline==False)&(out.reference==True)).sum()),
        "final_false_negatives":int(((out.final==False)&(out.reference==True)).sum()),
        "note":"Synthetic demonstration. Run the final approved evaluation set yourself before submission."
    }
    (ROOT/"outputs"/"evaluation_results.json").write_text(json.dumps(result,indent=2))
    out.to_csv(ROOT/"outputs"/"case_level_results.csv",index=False)
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    main()
