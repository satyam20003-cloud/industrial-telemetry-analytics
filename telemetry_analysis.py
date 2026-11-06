import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. Generate Realistic Industrial Telemetry Dataset
np.random.seed(42)
n_records = 1200

machine_ids = [f"MCH-{i:03d}" for i in np.random.randint(101, 115, size=n_records)]
temperature = np.random.normal(loc=72.0, scale=10.0, size=n_records)
vibration = np.random.normal(loc=4.5, scale=1.5, size=n_records)
pressure = np.random.normal(loc=101.3, scale=8.0, size=n_records)
rpm = np.random.normal(loc=1800, scale=250, size=n_records)

# Induce realistic machine failure criteria
failure_prob = (
    (temperature > 85.0) * 0.45 +
    (vibration > 6.5) * 0.35 +
    (pressure > 115.0) * 0.20
)
failure_flag = (np.random.rand(n_records) < failure_prob).astype(int)

df = pd.DataFrame({
    'machine_id': machine_ids,
    'temperature_c': np.round(temperature, 2),
    'vibration_mms': np.round(vibration, 2),
    'pressure_psi': np.round(pressure, 2),
    'rpm': np.round(rpm, 1),
    'failure_risk': failure_flag
})

# Save raw dataset
df.to_csv('data/sensor_telemetry.csv', index=False)
print("Dataset created: data/sensor_telemetry.csv")

# 2. Exploratory Data Analysis & Visualizations
sns.set_theme(style="whitegrid")

# Heatmap
plt.figure(figsize=(7, 5))
numeric_df = df.drop(columns=['machine_id'])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Industrial Telemetry Correlation Matrix')
plt.tight_layout()
plt.savefig('visualizations/correlation_heatmap.png')
plt.close()

# Distribution Plot
plt.figure(figsize=(7, 5))
sns.kdeplot(data=df, x='temperature_c', hue='failure_risk', common_norm=False, fill=True, palette='Set1')
plt.title('Temperature Distribution by Failure Risk Flag')
plt.xlabel('Operating Temperature (°C)')
plt.tight_layout()
plt.savefig('visualizations/failure_risk_distribution.png')
plt.close()
print("Charts saved in visualizations/")

# 3. Model Training & Evaluation
X = df[['temperature_c', 'vibration_mms', 'pressure_psi', 'rpm']]
y = df['failure_risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

print("\n--- Model Evaluation ---")
print(f"ROC-AUC Score: {roc_auc:.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))