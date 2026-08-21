# 🌍 Real-Time Air Quality Analytics Dashboard
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automation-2088FF?logo=githubactions)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Data%20Processing-013243?logo=numpy)
![SQL](https://img.shields.io/badge/SQL-Analytics-orange)
![REST API](https://img.shields.io/badge/REST%20API-Data%20Collection-green)
> **An automated data analytics pipeline for monitoring air quality and weather conditions across major Indian cities using Python, REST APIs, PostgreSQL, GitHub Actions, SQL, and Power BI.**

---

## 📌 Project Overview

The **Real-Time Air Quality Analytics Dashboard** is an end-to-end data analytics project designed to collect, store, analyze, and visualize air-quality and weather data across major Indian cities.

The system automatically collects environmental data through APIs, processes the data using Python, stores historical observations in PostgreSQL, and updates the database automatically using GitHub Actions.

The processed data is then connected to **Power BI** to create interactive dashboards for:
- AQI monitoring
- City-level pollution comparison
- Historical pollution trends
- PM2.5 and PM10 analysis
- Weather vs pollution analysis
- Correlation analysis
- City rankings

The project demonstrates a complete analytics workflow from **API data collection → ETL → SQL → Cloud Database → Automation → Business Intelligence**.

---

## 🎯 Objectives

The main objectives of this project are:

- Monitor air quality across major Indian cities.
- Collect AQI and pollutant-level data automatically.
- Combine pollution data with weather conditions.
- Store historical observations for trend analysis.
- Automate the data pipeline using GitHub Actions.
- Perform SQL-based data transformation and analysis.
- Build interactive Power BI dashboards.
- Identify relationships between weather variables and pollution levels.

---

# 🏗️ System Architecture

```mermaid
flowchart TD

    A[🌐 Open-Meteo Air Quality API]
    B[🌦️ Open-Meteo Weather API]

    A --> C[🐍 Python Data Collection]
    B --> C

    C --> D[Data Validation & Transformation]
    D --> E[🗄️ Supabase PostgreSQL]

    E --> F[SQL Analytical Views]

    F --> G[📊 Power BI]

    H[⚙️ GitHub Actions] --> C

    H -. Scheduled Hourly Execution .-> C

    G --> I[Interactive Dashboard]

    I --> I1[AQI Overview]
    I --> I2[Historical Trends]
    I --> I3[City Comparison]
    I --> I4[Weather vs Pollution]
```

---

