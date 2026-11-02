# 🎯 Relational SQL & RFM Customer Behavioral Segmentation Pipeline

An end-to-end analytical engineering project that processes over 100,000 multi-dimensional customer transaction profiles. This pipeline constructs a local database engine via SQLite, executes advanced SQL Common Table Expressions (CTEs), and uses statistical window functions (`NTILE`) to group the user base into actionable behavioral cohorts.

## 🚀 Key Engineering & Analytical Accomplishments
* **Production Volume Managed:** Processed 100,000 customer transaction histories.
* **Advanced Relational Scripting:** Architected complex nested SQL queries using Common Table Expressions (CTEs) to segment customer performance vectors simultaneously.
* **Statistical Distribution Mapping:** Utilized the `NTILE(5)` window function across Recency, Frequency, and Monetary constraints to distribute scores into precise statistical quintiles.

---

## 📦 Getting Started & Dataset Access

To interact with this business dashboard locally, follow these steps:

1. **Download the Source Data:** Download the raw data file directly from Kaggle: [🔗 Kaggle: E-Commerce Customer Behavior (2026)](https://www.kaggle.com/datasets/datascikhan/e-commerce-customer-behavior-dataset-2026?resource=download).
2. **Place Files Together:** Extract the downloaded `ecommerce_customer_behavior_2026.csv` file into this exact folder directory.
3. **Execute the App:** Open your terminal or command prompt (`cmd`) in this folder and run:
   ```bash
   streamlit run app.py
   ```

---

## 💻 Tech Stack & Tooling
* **Database Engine:** SQL (SQLite3 relational architecture)
* **Programming & Ingestion:** Python, Pandas, NumPy
* **Business Frontend:** Streamlit Dashboard Framework
