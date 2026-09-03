# Viva Questions and Simple Answers

1. What is the project about?
It analyzes UAC aggregate operational data as a care transition pipeline and measures efficiency, active-load changes and potential bottlenecks.

2. Why did you choose this project?
Because custody counts alone do not show how efficiently cases move through the pipeline.

3. What is EDA?
Exploratory Data Analysis is the process of understanding data structure, distributions, trends, relationships and anomalies.

4. Why Python?
Python provides Pandas, NumPy, Plotly and Streamlit for data analysis and dashboard development.

5. Why Streamlit?
It converts Python analytics into an interactive web application quickly.

6. What is Transfer Efficiency?
CBP transfers divided by CBP custody multiplied by 100.

7. Does Transfer Efficiency measure actual time?
No. It is a ratio indicator, not elapsed transition time.

8. What is Discharge Effectiveness?
HHS discharges divided by HHS care multiplied by 100.

9. What is Pipeline Throughput?
Aggregate HHS discharges divided by reported CBP intake multiplied by 100.

10. Why can throughput exceed 100%?
Because aggregate entries and exits can represent different cohorts and reporting periods.

11. What is backlog in this project?
We use active load and its report-to-report change as a proxy for accumulation pressure.

12. Can you calculate individual processing time?
No, because the dataset is aggregate and has no individual case IDs or timelines.

13. What is a bottleneck?
A period where flow is constrained or active load/pressure increases relative to other periods.

14. How is bottleneck severity calculated?
Using a project-defined weighted score based on percentile pressure from low efficiency, high load and positive load change.

15. Are your thresholds official?
No. They are project-defined analytical thresholds.

16. What is correlation?
A statistical association between variables.

17. Does correlation mean causation?
No.

18. What is Streamlit used for?
For building the interactive dashboard.

19. Why Plotly?
For interactive charts with hover and filtering support.

20. What is the biggest limitation?
The data are aggregate rather than individual-level.

21. What is future scope?
Case-level duration analysis, forecasting, geographic analysis and richer case-management variables.

22. What is active load?
CBP custody plus HHS care.

23. What did you do during preprocessing?
Date conversion, numeric conversion, invalid-date removal, sorting, quality checks and feature engineering.

24. What is outcome stability?
A project-defined score based on variability in discharge effectiveness; higher means more stable.

25. What is the purpose of the dashboard?
To provide an interactive monitoring and decision-support layer for transition efficiency and potential pressure periods.
