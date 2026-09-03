# Care Transition Efficiency & Placement Outcome Analytics

## Abstract
This project analyzes an aggregate UAC operational dataset through a process-efficiency lens rather than a capacity-only lens. The source contains 720 valid dated reporting observations from 2023-01-12 through 2025-12-21, after excluding 450 rows without valid dates. The analysis measures reported intake, CBP custody, CBP transfers, HHS care, and HHS discharges. Derived indicators include transfer efficiency, discharge effectiveness, aggregate pipeline throughput, active-load change, a project-defined outcome stability score, and a project-defined bottleneck score. Results show 67,337 reported intake observations in total, 92,641 reported transfers, and 124,853 reported discharges. The weighted transfer efficiency is 75.03% and weighted discharge effectiveness is 2.86%. The maximum combined active load is 11,762. Because the data are aggregate rather than individual-level, the project does not estimate individual time-to-placement or make causal claims.

## Keywords
UAC, process analytics, transition efficiency, backlog, bottleneck detection, Streamlit, data visualization

## 1. Introduction
The UAC care system can be viewed as a multi-stage operational pipeline: CBP custody, transfer to HHS, HHS care, and discharge to a sponsor or other appropriate placement. Monitoring only the number of children in custody can hide changes in the rate at which cases move through the system. This project therefore combines flow measures, active-load measures, and outcome indicators.

## 2. Problem Statement
Aggregate custody counts provide important capacity information but do not by themselves show whether transfers and discharges are keeping pace with incoming activity. A structured transition analytics framework can reveal periods of accumulation, changes in discharge performance, and recurring pressure patterns.

## 3. Objectives
1. Measure CBP-to-HHS transfer efficiency.
2. Evaluate HHS discharge effectiveness.
3. Compare aggregate entries and exits.
4. Detect periods of active-load accumulation.
5. Examine temporal and weekday/weekend patterns.
6. Provide an interactive dashboard for decision support.
7. Clearly communicate data limitations.

## 4. Dataset
The source CSV has 6 original variables and 1,170 rows, of which 720 have valid dates. The date range is 2023-01-12 to 2025-12-21. Rows without valid dates were excluded from chronological analysis. The five count variables were converted to numeric values after removing comma formatting.

## 5. Data Preprocessing
- Renamed long source columns to concise analytical names.
- Parsed reporting dates.
- Removed rows without valid dates.
- Converted count fields to numeric.
- Sorted observations chronologically.
- Checked duplicate dates and negative count cells.
- Preserved aggregate counts without fabricating individual records.
- Created reproducible derived variables.

## 6. Methodology
### 6.1 Transfer Efficiency
Transfer Efficiency = CBP Transfers / CBP Custody × 100. This is a ratio indicator and should not be interpreted as elapsed transition time.

### 6.2 Discharge Effectiveness
Discharge Effectiveness = HHS Discharges / HHS Care × 100.

### 6.3 Aggregate Pipeline Throughput
Aggregate Throughput = HHS Discharges / CBP Intake × 100. Because entries and exits may represent different cohorts and time periods, this ratio can exceed 100%.

### 6.4 Active Load and Accumulation
Active Load = CBP Custody + HHS Care. Report-to-report load change is the difference between consecutive available reporting observations. The source does not provide a complete daily series, so this is not always a calendar-day change.

### 6.5 Outcome Stability
A project-defined 0–100 score is derived from rolling variability in discharge effectiveness. Higher values indicate lower observed variability. This is an analytical construct, not an official metric.

### 6.6 Bottleneck Detection
The project-defined bottleneck score combines percentile-based pressure from low transfer efficiency, low discharge effectiveness, high active load, and positive load change. Severity bands are data-driven quantiles and are not official standards.

## 7. Exploratory Findings
- Total reported intake: 67,337
- Total reported transfers: 92,641
- Total reported discharges: 124,853
- Weighted transfer efficiency: 75.03%
- Weighted discharge effectiveness: 2.86%
- Aggregate throughput: 185.42%
- Maximum CBP custody: 531
- Maximum HHS care: 11,516
- Maximum combined active load: 11,762
- Largest report-to-report active-load increase: 730
- Largest report-to-report active-load decrease: -922
- High/Critical bottleneck observations: 180
- Critical bottleneck observations: 72
- Highest transfer-efficiency observation: 2025-02-13 (230.00%)
- Lowest transfer-efficiency observation: 2025-03-17 (0.00%)
- Highest discharge-effectiveness observation: 2023-01-12 (6.64%)
- Lowest discharge-effectiveness observation: 2025-11-30 (0.00%)

## 8. Weekday vs Weekend
The dashboard provides descriptive comparisons of average intake, transfers, discharges, transfer efficiency, and discharge effectiveness for weekdays and weekends. These comparisons should be interpreted descriptively unless formal statistical tests are added.

## 9. Recommendations
1. Monitor active-load change and flow indicators together rather than relying on custody counts alone.
2. Review periods with sustained low transfer or discharge indicators alongside rising active load.
3. Use monthly and rolling indicators to distinguish isolated spikes from persistent pressure.
4. Treat bottleneck alerts as triage signals for further operational investigation, not as proof of a cause.
5. If case-level data become available, add actual transition duration, stage duration, location, and case-management attributes.

## 10. Limitations
1. The dataset is aggregate, not individual-level.
2. Exact individual processing time cannot be computed.
3. Transfer efficiency is a ratio, not a literal speed measure.
4. Aggregate throughput is not a unique-child cohort conversion rate.
5. Discharge counts are interpreted as exits based on the supplied column definition.
6. Bottleneck thresholds are project-defined.
7. Descriptive patterns do not establish causation.

## 11. Conclusion
The project provides a reproducible framework for viewing UAC operational data as a transition pipeline. By combining flow activity, active load, efficiency ratios, temporal analysis, and transparent bottleneck indicators, the dashboard can highlight periods requiring closer review while avoiding unsupported claims about individual outcomes or causal mechanisms.
