# 8–10 Minute Seminar Speech

Good morning everyone. Today I am presenting my project, **Care Transition Efficiency & Placement Outcome Analytics**.

The main idea of this project is to look at the UAC program not only as a system that reports how many children are in custody, but as a multi-stage care transition pipeline.

The pipeline can be described as CBP custody, transfer to HHS, HHS care, and finally discharge for appropriate placement or reunification.

The problem we identified is that aggregate custody numbers alone do not tell us how efficiently children are moving through the system. We therefore asked four questions: how efficiently are transfers occurring, whether discharges are keeping pace with inflows, when active load accumulates, and whether performance patterns change over time.

Our dataset contains 1,170 source rows and six original variables. After parsing the dates, 450 rows without valid dates were excluded, leaving 720 valid observations. The reporting period runs from 2023-01-12 to 2025-12-21.

The first step was data preprocessing. We cleaned the column names, converted the date field to a proper datetime type, converted count columns into numeric values, handled comma formatting, checked missing values, duplicate dates and negative values, and sorted the observations chronologically.

After cleaning, we performed exploratory data analysis. We examined daily flow activity, active load, monthly trends, weekday and weekend patterns, and relationships among the operational variables.

Next, we created our KPIs. The first KPI is Transfer Efficiency. It is calculated as CBP transfers divided by CBP custody multiplied by 100. Importantly, this is a ratio indicator and not a literal measure of elapsed transition time.

The second KPI is Discharge Effectiveness, calculated as HHS discharges divided by HHS care multiplied by 100.

The third is Aggregate Pipeline Throughput, calculated as HHS discharges divided by reported intake multiplied by 100. This value can be above 100 percent because aggregate entries and exits can refer to different cohorts and reporting periods.

We also calculate Active Load as CBP custody plus HHS care. The change in active load between consecutive available reporting observations helps identify periods of accumulation.

From the actual dataset, total reported intake is 67,337, total reported transfers are 92,641, and total reported discharges are 124,853. The weighted transfer efficiency is 75.03 percent and weighted discharge effectiveness is 2.86 percent. The maximum combined active load is 11,762.

We also created a bottleneck detection framework. It combines data-driven pressure from low transfer efficiency, low discharge effectiveness, high active load and positive load change. The severity bands are defined for this project using the distribution of the data. They are not official government standards.

The project identified 180 High or Critical observations and 72 Critical observations under this analytical framework. The largest report-to-report increase in active load was 730.

The next component is the Streamlit dashboard. It contains an executive overview, a care pipeline snapshot, efficiency analysis, backlog and bottleneck analysis, temporal analysis, outcome stability, a data explorer and a methodology section.

The dashboard also provides date filtering, weekday or weekend filtering, bottleneck severity filtering, interactive Plotly charts and CSV download.

One important limitation is that the dataset is aggregate. We do not have an individual child identifier or individual case timeline. Therefore, we cannot calculate the actual number of days a particular child spent between CBP transfer and HHS discharge. We also cannot make causal claims from these descriptive patterns.

For future scope, if case-level data becomes available, we could calculate actual stage duration, time-to-placement, location-level performance, case complexity, and potentially build forecasting models.

To conclude, this project provides a structured way to monitor the care pipeline using flow indicators, active-load indicators, efficiency ratios, temporal analysis and transparent bottleneck signals. The goal is not to replace operational judgment, but to provide a data-driven monitoring layer that helps identify periods that deserve further investigation.

Thank you.
