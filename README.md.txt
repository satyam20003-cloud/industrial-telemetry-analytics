# Industrial Telemetry & Predictive Maintenance Analytics

An end-to-end operational data analytics framework designed to analyze multi-sensor industrial telemetry, identify equipment operating anomalies, and predict machine failure risk.

##  Architecture & Features
- **Exploratory Data Analysis (EDA):** Analyzed multi-variable correlation among vibration, pressure, temperature, and RPM to define operating tolerance thresholds.
- **Predictive Analytics:** Trained a Random Forest classifier utilizing stratified cross-validation to assess failure probabilities under operational loads.
- **SQL Analytics Pipeline:** Formulated production-grade SQL queries with aggregations, partitioning, and window functions to compute rolling performance averages.

##  Tech Stack
- **Languages:** Python (Pandas, NumPy, Scikit-Learn)
- **Data Querying:** SQL (MySQL/PostgreSQL compatible)
- **Data Visualization:** Matplotlib, Seaborn

##  Key Analytical Insights
1. **Operating Temperature Thresholds:** Operating temperatures exceeding 85°C show a strong positive correlation with mechanical failure flags.
2. **Multi-Sensor Compounding:** High vibration (>6.5 mm/s) accompanied by pressure surges (>115 PSI) compounds breakdown probability significantly.

##  Visual Outputs
- Correlation Matrix: `visualizations/correlation_heatmap.png`
- Risk Distribution: `visualizations/failure_risk_distribution.png`

##  Execution Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/industrial-telemetry-analytics.git
   cd industrial-telemetry-analytics