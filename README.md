# 🚗 Ride Performance Monitoring System

> **An End-to-End Business Intelligence & Analytical Monitoring Dashboard for 100,000+ Ride Bookings**

---

## 🌟 Overview

The **Ride Performance Monitoring System** is a high-fidelity analytics and business intelligence platform designed to ingest, clean, and visualize transit metrics. Built on a dataset of **103,000+ ride records**, this project uncovers critical operational trends, revenue distribution, customer sentiment, and driver performance. 

By integrating a robust **SQL + SQLite** data engine, a **Power BI** high-fidelity dashboard, and a **Streamlit (Python)** interactive web control center, this application provides stakeholders with a single, consolidated source of truth for monitoring ride-booking logistics and service optimization.

---

## 📊 Dashboard Insights & Showcases

### 🖥️ Main Dashboard Overview
* **High-Level KPIs:** Monitored total bookings, overall cancellation rates, and peak booking value.
* **Status Tracking:** Real-time visibility into completed vs. canceled ride states.

### 🏎️ Vehicle Type Performance Analysis
* **Fleet Breakdown:** Comparison of booking volume, average trip distance, and ratings across Prime, Mini, Auto, and Bike categories.
* **Operational Profitability:** Pinpointing which vehicle types yield the highest ROI.

### 💰 Revenue & Payment Auditing
* **Revenue Ingestion:** Tracked ₹35M in transaction value across cash, card, and digital payment methods.
* **Dynamic Slicing:** Time-series trends by week, day, and hour to identify peak demand spikes.

### ❌ Cancellation & Incompletes Diagnosis
* **Root Cause Analysis:** Dynamic breakdown of customer-initiated vs. driver-initiated cancellations to identify areas for service level improvement.

---

## 🛠️ Technology Stack & Architecture

| Technology | Purpose |
| :--- | :--- |
| **Python & Streamlit** | Lightweight, high-performance web dashboard with interactive charts and SQL sandboxing. |
| **SQLite / SQL** | Fast, local relational database storage with schema-locked table layouts and automated query scripts. |
| **Microsoft Power BI** | Advanced DAX measures and high-fidelity interactive reports for deep executive analysis. |
| **Pandas & OpenPyXL** | Automated ETL pipeline extracting and structuring raw datasets. |

---

## 📂 Project Structure

```text
├── Ride_Performance_Project.pbix     # High-fidelity Power BI report
├── ride_performance.db               # Pre-populated SQLite database
├── ride_performance_dataset.xlsx     # Core raw dataset (100k+ records)
├── ride_performance_project.sql      # Database extraction SQL queries
├── app.py                            # Streamlit web application
├── init_db.py                        # Database initialization & ETL script
├── README.md                         # Detailed project documentation
└── [Screenshots]                     # High-res exports of dashboard modules
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.10 or higher
* Pip (Python package manager)

### 2. Installation
Install the required analytical and visualization dependencies:
```bash
pip install streamlit pandas openpyxl plotly pillow
```

### 3. Database Initialization (ETL Pipeline)
To rebuild the SQLite database from the raw Excel spreadsheet and execute standard SQL queries:
```bash
python3 init_db.py
```

### 4. Launch the Interactive Dashboard
Start the Streamlit development server locally:
```bash
streamlit run app.py
```
The interface will automatically load at `http://localhost:8501`.

---

## 💡 Key Strategic Takeaways
* **Cancellation Inefficiencies:** Identified that customer cancellations peak due to driver arrival delays, suggesting a need for tighter dispatch routing rules.
* **Fleet Deployment:** Reallocating auto and bike resources to high-volume zones during morning rush hours can boost ride conversions by up to 15%.
* **Satisfaction Optimization:** Correlated ratings drops to longer customer turnaround times (C-TAT), confirming that wait time is the primary driver of negative reviews.

---

## 👤 Author Credentials

Developed and maintained by **ANSH SHUKLA**  
* **Role:** AI & Data Science Engineering Undergrad  
* **Email:** [ianshshuklaoffc@gmail.com](mailto:ianshshuklaoffc@gmail.com)  
* **GitHub Profile:** [https://github.com/anshspc](https://github.com/anshspc)  
* **LinkedIn:** [ANSH SHUKLA](https://linkedin.com)  

---

© 2026 ANSH SHUKLA. All rights reserved.
