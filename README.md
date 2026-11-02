# 🎯 Relational SQL & RFM Customer Behavioral Segmentation Pipeline

An end-to-end analytical engineering project that processes over 100,000 multi-dimensional customer transaction profiles. This pipeline constructs a local database engine via SQLite, executes advanced SQL Common Table Expressions (CTEs), and uses statistical window functions (`NTILE`) to group the user base into actionable behavioral cohorts.

## 🚀 Key Engineering & Analytical Accomplishments
* **Production Volume Managed:** Processed 100,000 customer transaction histories.
* **Advanced Relational Scripting:** Architected complex nested SQL queries using Common Table Expressions (CTEs) to segment customer performance vectors simultaneously.
* **Statistical Distribution Mapping:** Utilized the `NTILE(5)` window function across Recency, Frequency, and Monetary constraints to distribute scores into precise statistical quintiles.
* **Business-to-Tech Optimization:** Linked calculated relational metrics to live, distinct marketing playbooks (e.g., *Champions*, *At Severe Risk*, *Loyal Customers*) to dictate automated corporate communication paths.

---

## 📦 Getting Started & Dataset Access

To interact with the live business dashboard, you will need to provide the raw client transactional database files:

1. **Download the Source Data:** Download the raw uncompressed data file directly from the official Kaggle repository: [🔗 Kaggle: E-Commerce Customer Behavior (2026)](https://kaggle.com).
2. **Launch the Production UI:** Open the live executive interface server: [🚀 Launch Live Customer Segmentation Dashboard](https://streamlit.io) *(Replace with your actual Streamlit link!)*
3. **Local Database Verification:** Running the repository's Jupyter Notebook locally will automatically initialize a standalone relational `ecommerce_behavior.db` file in your path and run the processing pipeline.

---

## 🛠️ Data Pipeline & SQL Architecture

The data engine runs sequentially through the following automated processing blocks:

```sql
WITH rfm_base AS (
    SELECT 
        customer_id, customer_name, country, preferred_category,
        recency_days, total_spending_usd, total_items_purchased
    FROM customer_analytics
),
rfm_scores AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY total_items_purchased ASC) AS f_score,
        NTILE(5) OVER (ORDER BY total_spending_usd ASC) AS m_score
    FROM rfm_base
),
rfm_concatenated AS (
    SELECT *,
        (r_score || f_score || m_score) AS rfm_cell_id
    FROM rfm_scores
)
SELECT *,
    CASE
        WHEN rfm_cell_id IN ('555', '554', '544', '454', '455', '445') THEN 'Champions'
        WHEN rfm_cell_id IN ('543', '444', '435', '355', '354', '345', '344', '335') THEN 'Loyal Customers'
        WHEN rfm_cell_id IN ('255', '254', '245', '244', '253', '252', '243', '242') THEN 'High Risk / Cant Lose Them'
        WHEN rfm_cell_id IN ('155', '154', '145', '144', '115', '114') THEN 'At Severe Risk'
        ELSE 'Nurture / Growth Tier'
    END AS customer_behavior_segment
FROM rfm_concatenated;
```

---

## 💻 Tech Stack & Tooling
* **Database Engine:** SQL (SQLite3 relational architecture)
* **Programming & Ingestion:** Python 3.13, Pandas, NumPy
* **Business Frontend:** Streamlit Production Cloud (KPI Metrics & Columnar Dataframes)
* **Development Workspace:** Jupyter Notebook (`.ipynb` file tracking)

---

## 📁 Repository Map
* `/notebooks`: Contains the `sql_segmentation_pipeline.ipynb` tracking variable creation and database structure.
* `/sql_queries`: Standalone `.sql` text files hosting un-abstracted production query layers.
* `app.py`: Streamlit cloud script managing interactive cohort filtering sliders.
* `requirements.txt`: System environmental specifications document.
