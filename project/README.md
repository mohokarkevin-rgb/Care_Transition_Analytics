# Care Transition Efficiency & Placement Outcome Analytics

## Overview
A reproducible Python + Streamlit analytics project for the supplied UAC aggregate operational dataset.

## Actual dataset
- Source rows: 1170
- Valid dated observations used: 720
- Excluded rows with missing/invalid dates: 450
- Date range: 2023-01-12 to 2025-12-21

## Technology
Python, Pandas, NumPy, Matplotlib, Plotly, Streamlit, Jupyter, Pytest.

## Run
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```
On Windows you can also double-click `run_dashboard.bat`.

## Main KPIs
- Transfer Efficiency = CBP transfers / CBP custody × 100
- Discharge Effectiveness = HHS discharges / HHS care × 100
- Pipeline Throughput = HHS discharges / CBP intake × 100
- Active Load = CBP custody + HHS care
- Report-to-Report Load Change = current active load − previous available reporting observation
- Project-defined Outcome Stability Score
- Project-defined Bottleneck Score

## Actual headline results
- Total reported intake: 67,337
- Total reported transfers: 92,641
- Total reported discharges: 124,853
- Weighted transfer efficiency: 75.03%
- Weighted discharge effectiveness: 2.86%
- Aggregate throughput: 185.42%
- Maximum combined active load: 11,762

## Important limitations
This is aggregate reporting data, not individual case data. Exact child-level transition duration cannot be calculated. Ratio metrics are not literal elapsed-time measures. Aggregate throughput can exceed 100% because entries and exits can reflect different cohorts/time periods. Bottleneck bands are project-defined. Descriptive relationships do not establish causation.


## Streamlit Cloud deployment
Main file path: `app.py` (root). The app searches for the cleaned dataset in `outputs/cleaned_data/cleaned_uac_data.csv` or `data/cleaned_uac_data.csv`, and can also process the original CSV.
