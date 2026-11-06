-- Schema setup
CREATE TABLE IF NOT EXISTS sensor_telemetry (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id VARCHAR(20) NOT NULL,
    temperature_c DECIMAL(5,2),
    vibration_mms DECIMAL(5,2),
    pressure_psi DECIMAL(5,2),
    rpm DECIMAL(6,1),
    failure_risk INT
);

-- KPI Query 1: Machine telemetry operational summaries
SELECT 
    machine_id,
    COUNT(*) AS total_logs,
    ROUND(AVG(temperature_c), 2) AS avg_temp,
    ROUND(MAX(temperature_c), 2) AS peak_temp,
    ROUND(AVG(vibration_mms), 2) AS avg_vibration,
    SUM(failure_risk) AS total_failures
FROM sensor_telemetry
GROUP BY machine_id
HAVING total_failures > 5
ORDER BY total_failures DESC;

-- KPI Query 2: Rolling Average & Anomaly Detection (Window Function)
WITH RollingMetrics AS (
    SELECT 
        machine_id,
        temperature_c,
        vibration_mms,
        AVG(temperature_c) OVER(
            PARTITION BY machine_id 
            ORDER BY record_id 
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_temp
    FROM sensor_telemetry
)
SELECT 
    machine_id,
    temperature_c,
    ROUND(rolling_avg_temp, 2) AS rolling_avg_temp,
    CASE 
        WHEN temperature_c > (rolling_avg_temp * 1.25) THEN 'CRITICAL SPIKE'
        ELSE 'NORMAL'
    END AS telemetry_status
FROM RollingMetrics
WHERE temperature_c > (rolling_avg_temp * 1.25);