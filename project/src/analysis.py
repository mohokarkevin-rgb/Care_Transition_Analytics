import pandas as pd
import numpy as np

def add_bottleneck_score(df):
    df = df.copy()
    pct = lambda s: s.rank(pct=True).fillna(0.5)
    low_transfer = 1 - pct(df["transfer_efficiency"])
    low_discharge = 1 - pct(df["discharge_effectiveness"])
    load_pressure = pct(df["total_active_load"])
    increase_pressure = pct(df["report_to_report_load_change"].clip(lower=0))
    df["bottleneck_score"] = 100*(0.30*low_transfer + 0.30*low_discharge + 0.25*load_pressure + 0.15*increase_pressure)
    q1,q2,q3 = df["bottleneck_score"].quantile([.50,.75,.90])
    df["bottleneck_level"] = pd.cut(df["bottleneck_score"], [-np.inf,q1,q2,q3,np.inf],
                                    labels=["Low","Moderate","High","Critical"], include_lowest=True)
    return df
