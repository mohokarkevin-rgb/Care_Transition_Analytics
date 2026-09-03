import numpy as np
import pandas as pd

RENAME = {
    "Date":"date",
    "Children apprehended and placed in CBP custody*":"cbp_intake",
    "Children in CBP custody":"cbp_custody",
    "Children transferred out of CBP custody":"cbp_transfers",
    "Children in HHS Care":"hhs_care",
    "Children discharged from HHS Care":"hhs_discharges"
}
NUMERIC = ["cbp_intake","cbp_custody","cbp_transfers","hhs_care","hhs_discharges"]

def clean_data(df):
    df = df.rename(columns=RENAME).copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    quality = {
        "source_rows": len(df),
        "invalid_dates": int(df["date"].isna().sum()),
        "duplicate_dates": 0,
        "negative_cells": 0,
    }
    df = df.dropna(subset=["date"]).copy()
    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",","",regex=False).str.strip(), errors="coerce")
    quality["duplicate_dates"] = int(df["date"].duplicated().sum())
    quality["negative_cells"] = int((df[NUMERIC] < 0).sum().sum())
    df = df.sort_values("date").reset_index(drop=True)
    df[NUMERIC] = df[NUMERIC].fillna(0)
    return df, quality
