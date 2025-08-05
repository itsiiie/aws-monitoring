import streamlit as st
import os
import json

st.set_page_config(page_title="AWS Free Tier Usage Monitor", layout="centered")
st.title("📊 AWS Free Tier Usage Monitor")

# ---------- Load cost report ----------
cost_path = "reports/latest_cost_report.json"
if os.path.exists(cost_path):
    with open(cost_path, "r") as f:
        try:
            cost_data = json.load(f)
            st.header("💰 AWS Free Tier Cost Report")
            for item in cost_data.get("cost_data", []):
                service = item.get("Service", "Unknown")
                cost = item.get("Cost", 0.0)
                st.write(f"**{service}**: ${cost}")
            total = cost_data.get("total", 0.0)
            st.subheader(f"**Total Cost**: ${total}")
        except json.JSONDecodeError:
            st.error("❌ Failed to parse cost report JSON.")
else:
    st.warning("⚠️ No cost report data found. Please run `main.py` first.")


# ---------- Load usage report ----------
usage_path = "reports/latest_usage_report.json"
if os.path.exists(usage_path):
    with open(usage_path, "r") as f:
        try:
            usage_data = json.load(f)
            st.header("📦 AWS Free Tier Usage Report")
            for service, usage in usage_data.items():
                st.write(f"**{service}**: {usage}")
        except json.JSONDecodeError:
            st.error("❌ Failed to parse usage report JSON.")
else:
    st.warning("⚠️ No usage report data found. Please run `main.py` first.")
