import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DATA PATH
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent

# If app.py is inside dashboard/
BASE_DIR = CURRENT_DIR.parent

DATA_LOCATIONS = [
    BASE_DIR / "outputs" / "cleaned_data" / "cleaned_uac_data.csv",
    BASE_DIR / "data" / "cleaned_uac_data.csv",
    BASE_DIR / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv",
    CURRENT_DIR / "outputs" / "cleaned_data" / "cleaned_uac_data.csv",
    CURRENT_DIR / "data" / "cleaned_uac_data.csv",
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data_file = None

    for path in DATA_LOCATIONS:
        if path.exists():
            data_file = path
            break

    if data_file is None:
        st.error("❌ Dataset not found.")

        st.write("The application searched these locations:")

        for path in DATA_LOCATIONS:
            st.code(str(path))

        st.stop()

    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        st.error(f"❌ Unable to read dataset: {e}")
        st.stop()

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # --------------------------------------------------------
    # Rename common column variations
    # --------------------------------------------------------

    rename_map = {
        "date": "date",

        "children_apprehended_and_placed_in_cbp_custody":
            "cbp_intake",

        "children_in_cbp_custody":
            "cbp_custody",

        "children_transferred_out_of_cbp_custody":
            "cbp_transfers",

        "children_in_hhs_care":
            "hhs_care",

        "children_discharged_from_hhs_care":
            "hhs_discharges",
    }

    for old_name, new_name in rename_map.items():

        if old_name in df.columns:
            df.rename(
                columns={old_name: new_name},
                inplace=True
            )

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    if "date" not in df.columns:
        st.error("❌ Date column not found in dataset.")
        st.write("Available columns:")
        st.write(list(df.columns))
        st.stop()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Remove invalid dates
    # --------------------------------------------------------

    df = df.dropna(subset=["date"]).copy()

    # --------------------------------------------------------
    # Convert numerical columns
    # --------------------------------------------------------

    numeric_columns = [
        "cbp_intake",
        "cbp_custody",
        "cbp_transfers",
        "hhs_care",
        "hhs_discharges",
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        else:

            df[column] = 0

    # --------------------------------------------------------
    # Sort by date
    # --------------------------------------------------------

    df = df.sort_values("date").reset_index(drop=True)

    # --------------------------------------------------------
    # Active load
    # --------------------------------------------------------

    df["total_active_load"] = (
        df["cbp_custody"].fillna(0)
        + df["hhs_care"].fillna(0)
    )

    # --------------------------------------------------------
    # Transfer efficiency
    # --------------------------------------------------------

    df["transfer_efficiency"] = np.where(
        df["cbp_custody"] > 0,
        (
            df["cbp_transfers"]
            / df["cbp_custody"]
        ) * 100,
        np.nan
    )

    # --------------------------------------------------------
    # Discharge effectiveness
    # --------------------------------------------------------

    df["discharge_effectiveness"] = np.where(
        df["hhs_care"] > 0,
        (
            df["hhs_discharges"]
            / df["hhs_care"]
        ) * 100,
        np.nan
    )

    # --------------------------------------------------------
    # Pipeline throughput
    # --------------------------------------------------------

    df["pipeline_throughput"] = np.where(
        df["cbp_intake"] > 0,
        (
            df["hhs_discharges"]
            / df["cbp_intake"]
        ) * 100,
        np.nan
    )

    # --------------------------------------------------------
    # Weekend indicator
    # --------------------------------------------------------

    df["is_weekend"] = (
        df["date"].dt.dayofweek >= 5
    )

    # --------------------------------------------------------
    # Report-to-report load change
    # --------------------------------------------------------

    df["report_to_report_load_change"] = (
        df["total_active_load"].diff()
    )

    df["report_to_report_load_change"] = (
        df["report_to_report_load_change"]
        .fillna(0)
    )

    # --------------------------------------------------------
    # Bottleneck score
    # --------------------------------------------------------

    transfer_pressure = (
        100 - df["transfer_efficiency"]
    ).clip(lower=0)

    discharge_pressure = (
        100 - df["discharge_effectiveness"]
    ).clip(lower=0)

    load_pressure = (
        df["total_active_load"]
        .rank(pct=True)
        * 100
    )

    increase_pressure = (
        df["report_to_report_load_change"]
        .clip(lower=0)
        .rank(pct=True)
        * 100
    )

    df["bottleneck_score"] = (
        transfer_pressure * 0.30
        + discharge_pressure * 0.30
        + load_pressure * 0.25
        + increase_pressure * 0.15
    )

    # --------------------------------------------------------
    # Bottleneck severity
    # --------------------------------------------------------

    df["bottleneck_level"] = pd.cut(
        df["bottleneck_score"],
        bins=[
            -np.inf,
            25,
            50,
            75,
            np.inf
        ],
        labels=[
            "Low",
            "Moderate",
            "High",
            "Critical"
        ]
    )

    # --------------------------------------------------------
    # Outcome stability score
    # --------------------------------------------------------

    rolling_variability = (
        df["discharge_effectiveness"]
        .rolling(
            window=7,
            min_periods=2
        )
        .std()
    )

    df["outcome_stability_score"] = (
        100 - rolling_variability.fillna(0) * 10
    ).clip(
        lower=0,
        upper=100
    )

    return df


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title(
    "Care Transition Efficiency & Placement Outcome Analytics"
)

st.caption(
    "Aggregate operational analytics for CBP → HHS transitions, "
    "discharge activity, active load and potential bottlenecks."
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:

    st.header("🔎 Filters")

    dmin = df["date"].min().date()
    dmax = df["date"].max().date()

    dates = st.date_input(
        "Reporting date range",
        value=(dmin, dmax),
        min_value=dmin,
        max_value=dmax
    )

    if isinstance(dates, tuple) and len(dates) == 2:

        start = dates[0]
        end = dates[1]

    else:

        start = dmin
        end = dmax

    day_type = st.selectbox(
        "Day type",
        [
            "All",
            "Weekday",
            "Weekend"
        ]
    )

    severity = st.multiselect(
        "Bottleneck severity",
        [
            "Low",
            "Moderate",
            "High",
            "Critical"
        ],
        default=[
            "Low",
            "Moderate",
            "High",
            "Critical"
        ]
    )

    st.divider()

    st.info(
        "Severity thresholds are project-defined analytical bands "
        "and are not official government standards."
    )


# ============================================================
# APPLY FILTERS
# ============================================================

f = df[
    (df["date"].dt.date >= start)
    &
    (df["date"].dt.date <= end)
].copy()


if day_type != "All":

    f = f[
        f["is_weekend"]
        .eq(day_type == "Weekend")
    ]


if severity:

    f = f[
        f["bottleneck_level"]
        .astype(str)
        .isin(severity)
    ]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if f.empty:

    st.error(
        "❌ No observations match the selected filters."
    )

    st.stop()


# ============================================================
# EXECUTIVE KPIs
# ============================================================

st.subheader("📊 Executive KPIs")

k = st.columns(7)


transfer_efficiency = np.nan

if f["cbp_custody"].sum() > 0:

    transfer_efficiency = (
        f["cbp_transfers"].sum()
        /
        f["cbp_custody"].sum()
    ) * 100


discharge_effectiveness = np.nan

if f["hhs_care"].sum() > 0:

    discharge_effectiveness = (
        f["hhs_discharges"].sum()
        /
        f["hhs_care"].sum()
    ) * 100


vals = [

    (
        "Reporting observations",
        len(f),
        "{:,.0f}"
    ),

    (
        "Total intake",
        f["cbp_intake"].sum(),
        "{:,.0f}"
    ),

    (
        "Total transfers",
        f["cbp_transfers"].sum(),
        "{:,.0f}"
    ),

    (
        "Total discharges",
        f["hhs_discharges"].sum(),
        "{:,.0f}"
    ),

    (
        "Transfer efficiency",
        transfer_efficiency,
        "{:.2f}%"
    ),

    (
        "Discharge effectiveness",
        discharge_effectiveness,
        "{:.2f}%"
    ),

    (
        "Max active load",
        f["total_active_load"].max(),
        "{:,.0f}"
    )
]


for col, (label, value, fmt) in zip(k, vals):

    if pd.notna(value):

        col.metric(
            label,
            fmt.format(value)
        )

    else:

        col.metric(
            label,
            "N/A"
        )


# ============================================================
# SELECTED PERIOD KPIs
# ============================================================

a, b, c = st.columns(3)


a.metric(
    "Selected-period transfer efficiency",
    f"{transfer_efficiency:.2f}%"
)


b.metric(
    "Selected-period discharge effectiveness",
    f"{discharge_effectiveness:.2f}%"
)


avg_change = f[
    "report_to_report_load_change"
].mean()


c.metric(
    "Mean report-to-report load change",
    f"{avg_change:,.1f}"
)


# ============================================================
# TABS
# ============================================================

tabs = st.tabs(
    [
        "Overview",
        "Care Pipeline",
        "Efficiency",
        "Backlog & Bottlenecks",
        "Temporal Analysis",
        "Outcome Stability",
        "Data Explorer",
        "Methodology"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tabs[0]:

    st.subheader(
        "📈 Reported Flow Activity"
    )

    # --------------------------------------------------------
    # Flow chart
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f["cbp_intake"],
        label="CBP Intake"
    )

    ax.plot(
        f["date"],
        f["cbp_transfers"],
        label="CBP Transfers"
    )

    ax.plot(
        f["date"],
        f["hhs_discharges"],
        label="HHS Discharges"
    )

    ax.set_title(
        "Intake, Transfers and Discharges"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Reported Children")

    ax.legend()

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # Active load chart
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f["cbp_custody"],
        label="CBP Custody"
    )

    ax.plot(
        f["date"],
        f["hhs_care"],
        label="HHS Care"
    )

    ax.plot(
        f["date"],
        f["total_active_load"],
        label="Total Active Load"
    )

    ax.set_title(
        "CBP, HHS and Combined Active Load"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Reported Children")

    ax.legend()

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# TAB 2 — CARE PIPELINE
# ============================================================

with tabs[1]:

    st.subheader(
        "🔄 Aggregate Care Pipeline Snapshot"
    )

    latest = f.iloc[-1]

    labels = [
        "CBP custody",
        "CBP transfers",
        "HHS care",
        "HHS discharges"
    ]

    values = [
        latest["cbp_custody"],
        latest["cbp_transfers"],
        latest["hhs_care"],
        latest["hhs_discharges"]
    ]

    # --------------------------------------------------------
    # Pipeline horizontal bar chart
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    y_positions = np.arange(
        len(labels)
    )

    ax.barh(
        y_positions,
        values
    )

    ax.set_yticks(
        y_positions
    )

    ax.set_yticklabels(
        labels
    )

    ax.invert_yaxis()

    ax.set_xlabel(
        "Reported Children"
    )

    ax.set_title(
        f"Latest Selected Reporting Observation: "
        f"{latest['date'].date()}"
    )

    for i, value in enumerate(values):

        ax.text(
            value,
            i,
            f" {value:,.0f}",
            va="center"
        )

    ax.grid(
        axis="x",
        alpha=0.3
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    st.warning(
        "Aggregate snapshot only: these quantities should not "
        "be interpreted as unique children flowing through every stage."
    )


# ============================================================
# TAB 3 — EFFICIENCY
# ============================================================

with tabs[2]:

    st.subheader(
        "⚡ Transition Efficiency"
    )

    metric = st.selectbox(
        "Select efficiency metric",
        [
            "transfer_efficiency",
            "discharge_effectiveness",
            "pipeline_throughput"
        ],
        format_func=lambda x:
            x.replace(
                "_",
                " "
            ).title()
    )

    # --------------------------------------------------------
    # Efficiency trend
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f[metric]
    )

    ax.set_title(
        metric.replace(
            "_",
            " "
        ).title()
        + " Over Time"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Percent")

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # Transfers vs discharges
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f["cbp_transfers"],
        label="CBP Transfers"
    )

    ax.plot(
        f["date"],
        f["hhs_discharges"],
        label="HHS Discharges"
    )

    ax.set_title(
        "Transfers vs Discharges"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel(
        "Reported Children"
    )

    ax.legend()

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# TAB 4 — BACKLOG & BOTTLENECKS
# ============================================================

with tabs[3]:

    st.subheader(
        "🚨 Backlog & Bottleneck Analysis"
    )

    # --------------------------------------------------------
    # Active load
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f["total_active_load"]
    )

    ax.set_title(
        "Combined Active Load"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel(
        "Active Load"
    )

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # Load change
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.bar(
        f["date"],
        f["report_to_report_load_change"]
    )

    ax.set_title(
        "Report-to-Report Change in Active Load"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Change")

    ax.grid(
        axis="y",
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # Bottleneck table
    # --------------------------------------------------------

    st.subheader(
        "Highest Bottleneck Scores"
    )

    cols = [
        "date",
        "bottleneck_score",
        "bottleneck_level",
        "report_to_report_load_change",
        "transfer_efficiency",
        "discharge_effectiveness",
        "total_active_load"
    ]

    available_cols = [
        col
        for col in cols
        if col in f.columns
    ]

    st.dataframe(
        f.nlargest(
            15,
            "bottleneck_score"
        )[available_cols],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 5 — TEMPORAL ANALYSIS
# ============================================================

with tabs[4]:

    st.subheader(
        "📅 Temporal & Pattern Analysis"
    )

    # --------------------------------------------------------
    # Monthly aggregation
    # --------------------------------------------------------

    m = (
        f.assign(
            month=f["date"]
            .dt
            .to_period("M")
            .astype(str)
        )
        .groupby("month")
        .agg(
            Intake=(
                "cbp_intake",
                "sum"
            ),

            Transfers=(
                "cbp_transfers",
                "sum"
            ),

            Discharges=(
                "hhs_discharges",
                "sum"
            ),

            Avg_Transfer_Efficiency=(
                "transfer_efficiency",
                "mean"
            ),

            Avg_Discharge_Effectiveness=(
                "discharge_effectiveness",
                "mean"
            ),

            Avg_Active_Load=(
                "total_active_load",
                "mean"
            )
        )
        .reset_index()
    )

    st.subheader(
        "Monthly Analysis"
    )

    st.dataframe(
        m,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Monthly flow chart
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    x = np.arange(
        len(m)
    )

    width = 0.25

    ax.bar(
        x - width,
        m["Intake"],
        width,
        label="Intake"
    )

    ax.bar(
        x,
        m["Transfers"],
        width,
        label="Transfers"
    )

    ax.bar(
        x + width,
        m["Discharges"],
        width,
        label="Discharges"
    )

    ax.set_title(
        "Monthly Flow Activity"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Reported Children"
    )

    ax.set_xticks(
        x
    )

    ax.set_xticklabels(
        m["month"],
        rotation=45,
        ha="right"
    )

    ax.legend()

    ax.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # Weekday vs Weekend
    # --------------------------------------------------------

    w = (
        f.groupby(
            f["is_weekend"]
            .map({
                False: "Weekday",
                True: "Weekend"
            })
        )
        .agg(
            Avg_Intake=(
                "cbp_intake",
                "mean"
            ),

            Avg_Transfers=(
                "cbp_transfers",
                "mean"
            ),

            Avg_Discharges=(
                "hhs_discharges",
                "mean"
            ),

            Avg_Transfer_Efficiency=(
                "transfer_efficiency",
                "mean"
            ),

            Avg_Discharge_Effectiveness=(
                "discharge_effectiveness",
                "mean"
            )
        )
        .reset_index(
            names="Period"
        )
    )

    st.subheader(
        "Weekday vs Weekend"
    )

    st.dataframe(
        w,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 6 — OUTCOME STABILITY
# ============================================================

with tabs[5]:

    st.subheader(
        "📈 Outcome Stability"
    )

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        f["date"],
        f["outcome_stability_score"]
    )

    ax.set_title(
        "Project-defined Outcome Stability Score "
        "(0–100; higher = more stable)"
    )

    ax.set_xlabel(
        "Date"
    )

    ax.set_ylabel(
        "Stability Score"
    )

    ax.set_ylim(
        0,
        100
    )

    ax.grid(
        True,
        alpha=0.3
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    st.caption(
        "The score is based on rolling variability in discharge "
        "effectiveness. It is not an official government metric."
    )


# ============================================================
# TAB 7 — DATA EXPLORER
# ============================================================

with tabs[6]:

    st.subheader(
        "🗂️ Data Explorer"
    )

    st.write(
        f"Showing {len(f):,} filtered observations."
    )

    st.dataframe(
        f,
        use_container_width=True,
        hide_index=True
    )

    csv_data = f.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download filtered CSV",
        data=csv_data,
        file_name="filtered_uac_analytics.csv",
        mime="text/csv"
    )


# ============================================================
# TAB 8 — METHODOLOGY
# ============================================================

with tabs[7]:

    st.subheader(
        "📚 Methodology"
    )

    st.markdown(
        """
### Transfer Efficiency

**Transfer Efficiency =**

CBP Transfers ÷ CBP Custody × 100

This indicator measures the relationship between reported
transfers and the reported CBP custody load.

---

### Discharge Effectiveness

**Discharge Effectiveness =**

HHS Discharges ÷ HHS Care × 100

This indicator measures discharge activity relative to the
reported HHS care load.

---

### Pipeline Throughput

**Pipeline Throughput =**

HHS Discharges ÷ CBP Intake × 100

This is an aggregate flow comparison.

It can exceed 100% because entries and exits may represent
different cohorts or reporting periods.

---

### Active Load

**Active Load =**

CBP Custody + HHS Care

This provides an aggregate view of the reported active
population across the two stages.

---

### Report-to-Report Load Change

**Load Change =**

Current Combined Active Load − Previous Available
Reporting Observation

Positive values indicate an increase in the reported active
load compared with the previous available observation.

---

### Bottleneck Score

The project-defined bottleneck score combines pressure from:

- Low transfer efficiency
- Low discharge effectiveness
- High active load
- Positive report-to-report load change

The score is used for analytical prioritization.

The thresholds are project-defined and are **not official
government standards**.

---

### Outcome Stability Score

The outcome stability score is based on rolling variability
in discharge effectiveness.

Higher scores indicate greater consistency.

The score is project-defined and is not an official
government KPI.

---

### Important Limitations

The dataset is aggregate rather than individual-level.

Therefore:

- Exact individual transition time cannot be calculated.
- Individual child placement duration cannot be calculated.
- Aggregate ratios should not be interpreted as individual
  processing times.
- Correlation does not establish causation.
- Project-defined thresholds are not official standards.
- Different reporting periods may represent different cohorts.
"""
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Care Transition Efficiency & Placement Outcome Analytics | "
    "Academic Analytics Project"
)
