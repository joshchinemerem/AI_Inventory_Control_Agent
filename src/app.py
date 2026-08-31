
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.inventory_agent import InventoryWorkflow


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Inventory Control Agent",
    page_icon="📦",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📦 AI Inventory Control Agent")
st.subheader("Inventory Risk & Reorder Decision Support")

st.markdown(
    """
    **AI-powered inventory monitoring for stockout-risk detection,
    replenishment recommendations, and human-approved procurement decisions.**
    """
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown(
    """
    **Workflow**

    1. Data Agent
    2. Inventory Risk Agent
    3. Verification Agent
    4. Report Agent
    """
)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload Inventory CSV",
    type=["csv"]
)

run_analysis = st.sidebar.button(
    "🚀 Run Inventory Analysis",
    type="primary",
    use_container_width=True
)

st.sidebar.divider()

st.sidebar.caption(
    "Final procurement decisions require human approval."
)


# =========================================================
# RUN ANALYSIS
# =========================================================

if run_analysis:

    if uploaded_file is not None:

        data_path = ROOT / "data" / "uploaded_inventory.csv"
        data_path.write_bytes(uploaded_file.getvalue())

    else:

        data_path = ROOT / "data" / "inventory_history.csv"

    output_path = ROOT / "outputs" / "inventory_report.json"

    try:

        workflow = InventoryWorkflow()

        report = workflow.run(
            str(data_path),
            str(output_path)
        )

        st.session_state["report"] = report

        st.success(
            "✅ Inventory analysis completed successfully."
        )

    except Exception as e:

        st.error(
            f"Analysis failed: {e}"
        )


# =========================================================
# DISPLAY REPORT
# =========================================================

if "report" in st.session_state:

    report = st.session_state["report"]

    summary = report["summary"]

    findings = report["findings"]


    # =====================================================
    # EXECUTIVE KPIs
    # =====================================================

    st.header("📊 Executive Inventory Summary")

    total_items = summary["items_reviewed"]

    critical = summary["critical"]
    high = summary["high"]
    medium = summary["medium"]
    low = summary["low"]

    attention_items = critical + high + medium

    verification_issues = summary["verification_issues"]


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Items Reviewed",
        total_items
    )

    col2.metric(
        "🔴 Critical",
        critical
    )

    col3.metric(
        "⚠️ Need Attention",
        attention_items
    )

    col4.metric(
        "✅ Verification Issues",
        verification_issues
    )


    st.divider()


    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    st.header("📈 Risk Distribution")

    risk_data = pd.DataFrame(
        {
            "Risk Level": [
                "Critical",
                "High",
                "Medium",
                "Low"
            ],
            "Items": [
                critical,
                high,
                medium,
                low
            ]
        }
    )

    st.bar_chart(
        risk_data.set_index("Risk Level")
    )


    # =====================================================
    # PRIORITY TABLE
    # =====================================================

    st.header("🚨 Inventory Priority List")

    table_data = []

    for item in findings:

        evidence = item["evidence"]

        table_data.append(
            {
                "Item Code": item["item_code"],
                "Item": item["item_name"],
                "Risk": item["risk_level"],
                "Stock": evidence["latest_stock"],
                "Days Cover": item["days_of_cover"],
                "Lead Time": evidence["lead_time_days"],
                "Reorder Point": evidence["reorder_point"],
                "Recommended Order": item[
                    "recommended_order_qty"
                ]
            }
        )

    priority_df = pd.DataFrame(table_data)

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CRITICAL ITEMS
    # =====================================================

    critical_items = [
        item
        for item in findings
        if item["risk_level"] == "CRITICAL"
    ]

    if critical_items:

        st.header("🔴 Critical Inventory Items")

        for item in critical_items:

            evidence = item["evidence"]

            with st.expander(
                f"{item['item_code']} — "
                f"{item['item_name']} | "
                f"{item['days_of_cover']} days cover"
            ):

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Current Stock",
                    evidence["latest_stock"]
                )

                col2.metric(
                    "Reorder Point",
                    evidence["reorder_point"]
                )

                col3.metric(
                    "Recommended Order",
                    item["recommended_order_qty"]
                )


                st.markdown("### Why is this item critical?")

                for reason in item["reasons"]:

                    st.write(
                        f"• {reason}"
                    )


                st.markdown("### Evidence Used")

                evidence_df = pd.DataFrame(
                    {
                        "Metric": [
                            "30-Day Average Demand",
                            "7-Day Average Demand",
                            "Lead Time",
                            "Safety Stock",
                            "Demand Variability"
                        ],
                        "Value": [
                            evidence["30_day_avg_demand"],
                            evidence["7_day_avg_demand"],
                            evidence["lead_time_days"],
                            evidence["safety_stock"],
                            evidence["demand_std"]
                        ]
                    }
                )

                st.table(evidence_df)


    # =====================================================
    # REORDER RECOMMENDATIONS
    # =====================================================

    st.header("🛒 Reorder Recommendations")

    reorder_items = [
        item
        for item in findings
        if item["recommended_order_qty"] > 0
    ]

    reorder_df = pd.DataFrame(
        [
            {
                "Item Code": item["item_code"],
                "Item": item["item_name"],
                "Risk": item["risk_level"],
                "Recommended Order Qty":
                    item["recommended_order_qty"],
                "Reason": "; ".join(item["reasons"])
            }
            for item in reorder_items
        ]
    )

    st.dataframe(
        reorder_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.header("📥 Export Report")

    report_json = __import__("json").dumps(
        report,
        indent=2
    )

    st.download_button(
        label="⬇️ Download Inventory Risk Report",
        data=report_json,
        file_name="inventory_risk_report.json",
        mime="application/json"
    )


    # =====================================================
    # AGENT WORKFLOW
    # =====================================================

    st.header("🤖 Agentic Workflow")

    workflow_col1, workflow_col2, workflow_col3, workflow_col4 = (
        st.columns(4)
    )

    workflow_col1.info(
        "**1. Data Agent**\n\n"
        "Validates and prepares inventory data."
    )

    workflow_col2.warning(
        "**2. Inventory Risk Agent**\n\n"
        "Calculates stockout risk and reorder quantities."
    )

    workflow_col3.success(
        "**3. Verification Agent**\n\n"
        "Checks recommendations for consistency."
    )

    workflow_col4.info(
        "**4. Report Agent**\n\n"
        "Produces the final decision-support report."
    )


    # =====================================================
    # HUMAN APPROVAL
    # =====================================================

    st.divider()

    st.warning(
        "👤 **Human Approval Required**\n\n"
        "The AI provides inventory recommendations and decision "
        "support. Procurement officers must review and approve "
        "replenishment decisions before purchase orders are issued."
    )


else:

    # =====================================================
    # INITIAL SCREEN
    # =====================================================

    st.info(
        "Upload an inventory CSV or use the default dataset, "
        "then click **Run Inventory Analysis**."
    )

    st.markdown(
        """
        ### What this system does

        **📊 Analyze**
        Inventory history, demand, stock levels, lead times,
        and safety stock.

        **🚨 Detect**
        Critical, high, medium, and low inventory-risk conditions.

        **🛒 Recommend**
        Replenishment quantities based on recent demand and
        inventory position.

        **🔍 Verify**
        Check recommendations before presenting them to the user.

        **👤 Support decisions**
        Keep the final procurement decision under human control.
        """
    )

