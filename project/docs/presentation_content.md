# Presentation Content — 15 Slides

## Slide 1 — Title
Care Transition Efficiency & Placement Outcome Analytics
- Python + Streamlit Data Analytics Project
- UAC aggregate operational data

## Slide 2 — Background
- UAC care is a multi-stage pipeline.
- Stages include CBP custody, HHS transfer, HHS care and discharge.
- Capacity counts alone do not describe process movement.

## Slide 3 — Problem Statement
- How efficiently are transfers occurring?
- Are discharges keeping pace with inflows?
- When does active load accumulate?
- Which periods show potential bottlenecks?

## Slide 4 — Objectives
- Measure transfer efficiency.
- Evaluate discharge effectiveness.
- Analyze backlog/active-load change.
- Identify temporal patterns.
- Build an interactive dashboard.

## Slide 5 — Care Pipeline
CBP custody → Transfer → HHS care → Discharge → Sponsor placement/reunification
- Explain that source data are aggregate reporting counts.

## Slide 6 — Dataset
- Source rows: 1,170
- Valid dated observations: 720
- Variables: 6 original columns
- Date range: 2023-01-12 to 2025-12-21
- Rows without valid dates: 450

## Slide 7 — Data Preparation
- Date parsing
- Numeric conversion
- Comma cleanup
- Missing/duplicate checks
- Chronological sorting
- Feature engineering

## Slide 8 — KPI Framework
- Transfer Efficiency = Transfers / CBP Custody × 100
- Discharge Effectiveness = Discharges / HHS Care × 100
- Aggregate Throughput = Discharges / Intake × 100
- Active Load = CBP Custody + HHS Care
- Load Change = Current − Previous observation

## Slide 9 — EDA Results
- Total intake: 67,337
- Total transfers: 92,641
- Total discharges: 124,853
- Maximum active load: 11,762
- Show flow and active-load charts.

## Slide 10 — Efficiency
- Weighted transfer efficiency: 75.03%
- Weighted discharge effectiveness: 2.86%
- Explain that these are ratio indicators.

## Slide 11 — Bottleneck Analysis
- High/Critical observations: 180
- Critical observations: 72
- Largest load increase: 730
- Explain project-defined scoring.

## Slide 12 — Temporal Analysis
- Monthly performance
- Weekday vs weekend
- Rolling indicators
- Use the dashboard charts.

## Slide 13 — Streamlit Dashboard
- Filters
- KPI cards
- Pipeline snapshot
- Efficiency charts
- Backlog charts
- Data explorer/download

## Slide 14 — Recommendations
- Monitor active load + flow together.
- Investigate sustained low-efficiency periods.
- Use alerts as review signals.
- Add case-level data for deeper analysis.

## Slide 15 — Conclusion & Limitations
- Dashboard provides a process-efficiency lens.
- Aggregate data cannot provide individual duration.
- Descriptive patterns do not prove causation.
- Future scope: case-level duration and predictive analysis.
