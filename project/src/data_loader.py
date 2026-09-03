from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"

def load_raw_data(path=DATA_PATH):
    return pd.read_csv(path)
