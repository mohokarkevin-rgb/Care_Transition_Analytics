import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Care Transition Analytics", page_icon="📊", layout="wide")
DATA = Path(__file__).resolve().parents[1] / "outputs" / "cleaned_data" / "cleaned_uac_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA, parse_dates=["date"])

df = load_data()

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.caption("Aggregate operational analytics for CBP → HHS transitions, discharge activity, active load and potential bottlenecks.")

with st.sidebar:
    st.header("Filters")
    dmin, dmax = df.date.min().date(), df.date.max().date()
    dates = st.date_input("Reporting date range", (dmin, dmax), min_value=dmin, max_value=dmax)
    if isinstance(dates, tuple) and len(dates) == 2:
        start, end = dates
    else:
        start, end = dmin, dmax
    day_type = st.selectbox("Day type", ["All", "Weekday", "Weekend"])
    severity = st.multiselect("Bottleneck severity", ["Low","Moderate","High","Critical"],
                              default=["Low","Moderate","High","Critical"])
    st.divider()
    st.info("Severity thresholds are project-defined analytical bands, not official government standards.")

f = df[(df.date.dt.date >= start) & (df.date.dt.date <= end)].copy()
if day_type != "All":
    f = f[f.is_weekend.eq(day_type == "Weekend")]
if severity:
    f = f[f.bottleneck_level.astype(str).isin(severity)]

st.subheader("Executive KPIs")
k = st.columns(7)
vals = [
    ("Reporting observations", len(f), "{:,.0f}"),
    ("Total intake", f.cbp_intake.sum(), "{:,.0f}"),
    ("Total transfers", f.cbp_transfers.sum(), "{:,.0f}"),
    ("Total discharges", f.hhs_discharges.sum(), "{:,.0f}"),
    ("Weighted transfer efficiency", (f.cbp_transfers.sum()/f.cbp_custody.sum()*100 if f.cbp_custody.sum() else np.nan), "{:.2f}%"),
    ("Weighted discharge effectiveness", (f.hhs_discharges.sum()/f.hhs_care.sum()*100 if f.hhs_care.sum() else np.nan), "{:.2f}%"),
    ("Max active load", f.total_active_load.max() if not f.empty else np.nan, "{:,.0f}")
]
for col, (label, value, fmt) in zip(k, vals):
    col.metric(label, fmt.format(value) if pd.notna(value) else "N/A")

if f.empty:
    st.error("No observations match the selected filters.")
    st.stop()

a,b,c = st.columns(3)
te = f.cbp_transfers.sum()/f.cbp_custody.sum()*100 if f.cbp_custody.sum() else np.nan
de = f.hhs_discharges.sum()/f.hhs_care.sum()*100 if f.hhs_care.sum() else np.nan
avg_change = f.report_to_report_load_change.mean()
a.metric("Selected-period transfer efficiency", f"{te:.2f}%")
b.metric("Selected-period discharge effectiveness", f"{de:.2f}%")
c.metric("Mean report-to-report load change", f"{avg_change:,.1f}")

tabs = st.tabs(["Overview","Care Pipeline","Efficiency","Backlog & Bottlenecks","Temporal Analysis","Outcome Stability","Data Explorer","Methodology"])

with tabs[0]:
    st.subheader("Reported Flow Activity")
    fig = px.line(f, x="date", y=["cbp_intake","cbp_transfers","hhs_discharges"],
                  labels={"value":"Reported children","date":"Date","variable":"Flow"},
                  title="Intake, Transfers and Discharges")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(f, x="date", y=["cbp_custody","hhs_care","total_active_load"],
                  labels={"value":"Reported children","date":"Date","variable":"Load"},
                  title="CBP, HHS and Combined Active Load")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Aggregate Care Pipeline Snapshot")
    latest = f.iloc[-1]
    labels = ["CBP custody","CBP transfers","HHS care","HHS discharges"]
    values = [latest.cbp_custody, latest.cbp_transfers, latest.hhs_care, latest.hhs_discharges]
    fig = go.Figure(go.Funnel(y=labels, x=values, textinfo="value+percent initial"))
    fig.update_layout(title=f"Latest selected reporting observation: {latest.date.date()}")
    st.plotly_chart(fig, use_container_width=True)
    st.warning("Aggregate snapshot only: these quantities should not be interpreted as unique children flowing through every stage.")

with tabs[2]:
    metric = st.selectbox("Efficiency metric", ["transfer_efficiency","discharge_effectiveness","pipeline_throughput"],
                           format_func=lambda x: x.replace("_"," ").title())
    fig = px.line(f, x="date", y=metric, title=metric.replace("_"," ").title()+" Over Time",
                  labels={metric:"Percent","date":"Date"})
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(f, x="date", y=["cbp_transfers","hhs_discharges"],
                  title="Transfers vs Discharges", labels={"value":"Reported children","date":"Date","variable":"Flow"})
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    fig = px.line(f, x="date", y="total_active_load", title="Combined Active Load")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.bar(f, x="date", y="report_to_report_load_change",
                 title="Report-to-Report Change in Active Load",
                 labels={"report_to_report_load_change":"Change","date":"Date"})
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Highest Bottleneck Scores")
    cols = ["date","bottleneck_score","bottleneck_level","report_to_report_load_change",
            "transfer_efficiency","discharge_effectiveness","total_active_load"]
    st.dataframe(f.nlargest(15,"bottleneck_score")[cols], use_container_width=True, hide_index=True)

with tabs[4]:
    m = f.assign(month=f.date.dt.to_period("M").astype(str)).groupby("month").agg(
        Intake=("cbp_intake","sum"), Transfers=("cbp_transfers","sum"),
        Discharges=("hhs_discharges","sum"), Avg_Transfer_Efficiency=("transfer_efficiency","mean"),
        Avg_Discharge_Effectiveness=("discharge_effectiveness","mean"),
        Avg_Active_Load=("total_active_load","mean")).reset_index()
    st.dataframe(m, use_container_width=True, hide_index=True)
    fig = px.bar(m, x="month", y=["Intake","Transfers","Discharges"], title="Monthly Flow Activity")
    st.plotly_chart(fig, use_container_width=True)
    w = f.groupby(f.is_weekend.map({False:"Weekday",True:"Weekend"})).agg(
        Avg_Intake=("cbp_intake","mean"), Avg_Transfers=("cbp_transfers","mean"),
        Avg_Discharges=("hhs_discharges","mean"), Avg_Transfer_Efficiency=("transfer_efficiency","mean"),
        Avg_Discharge_Effectiveness=("discharge_effectiveness","mean")).reset_index(names="Period")
    st.subheader("Weekday vs Weekend")
    st.dataframe(w, use_container_width=True, hide_index=True)

with tabs[5]:
    fig = px.line(f, x="date", y="outcome_stability_score",
                  title="Project-defined Outcome Stability Score (0–100; higher = more stable)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The score is based on rolling variability in discharge effectiveness. It is not an official government metric.")

with tabs[6]:
    st.dataframe(f, use_container_width=True, hide_index=True)
    st.download_button("Download filtered CSV", f.to_csv(index=False), "filtered_uac_analytics.csv", "text/csv")

with tabs[7]:
    st.markdown("""
**Transfer Efficiency:** CBP transfers / CBP custody × 100.

**Discharge Effectiveness:** HHS discharges / HHS care × 100.

**Pipeline Throughput:** HHS discharges / CBP intake × 100. This is an aggregate flow comparison and can exceed 100% because entries and exits may represent different cohorts/time periods.

**Active Load:** CBP custody + HHS care.

**Report-to-Report Load Change:** current combined active load minus the previous available reporting observation.

**Bottleneck Score:** a project-defined weighted score using percentile-based pressure from low transfer performance, low discharge performance, high active load, and positive load change.

**Limitations:** the dataset is aggregate, not individual-level; exact time-to-placement cannot be computed; correlation does not establish causation; thresholds are analytical and not official standards.
""")
