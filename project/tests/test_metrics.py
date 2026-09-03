import pandas as pd
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.metrics import safe_ratio

def test_safe_ratio():
    out = safe_ratio(np.array([10.,0.]), np.array([5.,0.]))
    assert out[0] == 200
    assert np.isnan(out[1])

def test_active_load_logic():
    df = pd.DataFrame({"cbp_custody":[10,20], "hhs_care":[100,200]})
    assert (df.cbp_custody + df.hhs_care).tolist() == [110,220]
