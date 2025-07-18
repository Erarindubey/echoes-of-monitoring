```markdown
# 🌐 Echoes of Monitoring

*A containerized orchestration and observability stack for resilient data workflows.*

---

## 📦 Overview

**Echoes of Monitoring** integrates Apache Airflow, Spark, Prometheus, Flask, and Grafana into a modular pipeline that processes data, exposes metrics, and delivers real-time insights—now with email alert capabilities. Built for visibility, recovery, and operational grace.

---

## ⚙️ Tech Stack

| Layer             | Tool                                      |
|------------------|-------------------------------------------|
| Orchestration     | Apache Airflow v3.0.3                     |
| Processing        | Apache Spark v3.5.0 with Hadoop 3         |
| Monitoring        | Prometheus                                |
| Visualization     | Grafana                                   |
| Notification      | SMTP Email Alerts via Python              |
| Metric Endpoint   | Flask                                     |
| Language          | Python 3.10                               |
| Containerization  | Docker & Docker Compose                   |

---

## 🧩 Core Modules

### 1. Airflow DAGs
- Modular PythonOperator-based pipelines
- Retry and logging via `@recovery_wrapper`
- DAG: `echoes_of_monitoring`

### 2. Spark Pipeline
- Reads CSV from `/opt/input`
- Writes Parquet to `/opt/output/streamline2_run`
- Fully dockerized execution via `spark-submit`

### 3. Prometheus Metric Export
- Custom Flask app at `/metrics`
- Tracks:
  - `files_copied`
  - `file_copy_errors`

### 4. Grafana Dashboards
- Time series for DAG runtime, error frequency, system metrics
- Prometheus integrated panels

### 5. Email Alerting
- SMTP integration using app password
- Triggers:
  - DAG completion summary
  - Error exception logging
- Configurable recipients and format

---

## 🧪 Setup & Deployment

### 📁 Clone the Repository
```bash
git clone https://github.com/Erarindubey/echoes-of-monitoring.git
cd echoes-of-monitoring
```

### 🏗️ Build & Run
```bash
docker-compose up --build
```
NOTE:- Prometheus files are present but the main prometheus directory was excluded from git as it exceeds the size please refer to this link and download PROMETHEUS 

#👉 [Download Prometheus v3.4.2 for Windows (amd64)](https://sourceforge.net/projects/prometheus.mirror/files/v3.4.2/)
#This ZIP file includes:
#- prometheus.exe
#- promtool.exe
#- prometheus.yml (default config)
# [Prometheus download page](https://prometheus.io/download/) 

Note:- For each time you start prometheus server and airflow server please attach both to a bridge network 
i would recomment using 

```bash
docker network connect monitoring_net <Container_name>
```

---

## 📬 Sample Email Alert

```
Subject: Echoes of Monitoring - DAG Completed
Body:
12 files processed in 123.57 seconds
0 errors logged
```

---

## 🖼️ Diagrams & Architecture

- UML Component Diagram: Shows modular interaction between DAG, Flask metrics, Prometheus, Grafana, and Email Service
- Use Case Diagram: Actors like System Administrator & Pipeline Engineer interacting with metrics, logs, and alerts

---

## 🎯 Achievements

✅ Self-healing DAGs with structured retry logic  
✅ Visualized metrics with Grafana & Prometheus  
✅ SMTP email integration for alerting  
✅ Containerized orchestration with persistent networking  

---

## 🚀 Future Enhancements

- Prometheus Alert Manager hooks  
- Historical DAG performance aggregation  
- Kafka stream monitoring support  

---

## 📄 License

MIT — feel free to fork, customize, and enhance.

---

## 🤝 Credits

Designed and engineered by [Arin Dubey](https://github.com/Erarindubey)

---
