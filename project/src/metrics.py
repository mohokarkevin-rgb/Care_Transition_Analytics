import numpy as np
import pandas as pd

def safe_ratio(num, den):
    return np.where(den != 0, num / den * 100, np.nan)

def add_metrics(df):
    df = df.copy()
    df["transfer_efficiency"] = safe_ratio(df["cbp_transfers"], df["cbp_custody"])
    df["discharge_effectiveness"] = safe_ratio(df["hhs_discharges"], df["hhs_care"])
    df["pipeline_throughput"] = safe_ratio(df["hhs_discharges"], df["cbp_intake"])
    df["total_active_load"] = df["cbp_custody"] + df["hhs_care"]
    df["report_to_report_load_change"] = df["total_active_load"].diff()
    df["load_change_rate"] = safe_ratio(df["report_to_report_load_change"], df["total_active_load"].shift(1))
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["date"].dt.day_name()
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    df["transfer_eff_7obs"] = df["transfer_efficiency"].rolling(7, min_periods=3).mean()
    df["discharge_eff_7obs"] = df["discharge_effectiveness"].rolling(7, min_periods=3).mean()
    std = df["discharge_effectiveness"].rolling(7, min_periods=3).std()
    df["outcome_stability_score"] = (100 / (1 + std)).clip(0, 100)
    return df
