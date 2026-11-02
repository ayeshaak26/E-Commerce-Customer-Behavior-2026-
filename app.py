import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="RFM Customer Segmentation Engine", page_icon="🎯", layout="wide"
)

st.title("🎯 Data-Driven Customer Segmentation Dashboard")
st.write(
    "Ingesting multidimensional transaction matrices via local SQL architecture to map custom RFM behavioral segmentations."
)

# Connect to our computed local database asset
db_path = "ecommerce_behavior.db"


@st.cache_data
def fetch_segmented_data(path):
    conn = sqlite3.connect(path)

    # Master analytical query combining our exact schema column footprints
    query = """
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
            WHEN rfm_cell_id IN ('553', '551', '552', '541', '542', '453', '452', '451') THEN 'Recent/New Ingestions'
            WHEN rfm_cell_id IN ('512', '511', '422', '421', '412', '411', '311') THEN 'Promising/New'
            WHEN rfm_cell_id IN ('532', '531', '432', '431', '332', '322', '321') THEN 'Needs Attention'
            WHEN rfm_cell_id IN ('331', '321', '312', '221', '213', '231', '241', '251') THEN 'About to Churn'
            WHEN rfm_cell_id IN ('255', '254', '245', '244', '253', '252', '243', '242', '235', '234') THEN 'High Risk / Cant Lose Them'
            WHEN rfm_cell_id IN ('155', '154', '145', '144', '214', '215', '115', '114') THEN 'At Severe Risk'
            ELSE 'Lost / Hibernating'
        END AS customer_behavior_segment
    FROM rfm_concatenated;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


try:
    df_master = fetch_segmented_data(db_path)

    # Upper Overview Row: Dynamic KPIs
    st.markdown("### 📈 Core Operational Performance Indicators")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Client Cohort Analyzed", f"{len(df_master):,}")
    kpi2.metric(
        "Total Historical Revenue", f"${df_master['total_spending_usd'].sum():,.2f}"
    )
    kpi3.metric(
        "Gross Products Ordered", f"{int(df_master['total_items_purchased'].sum()):,}"
    )

    st.markdown("---")

    # Segment drill down layout configuration
    st.subheader("🔍 Cohort Slicing & Targeted Marketing Playbooks")

    segment_list = list(df_master["customer_behavior_segment"].unique())
    selected_segment = st.selectbox(
        "Select Client Performance Tier to Inspect:", sorted(segment_list)
    )

    # Filter data live on layout update
    df_filtered = df_master[
        df_master["customer_behavior_segment"] == selected_segment
    ]

    col_strategy, col_table = st.columns([1, 2])

    with col_strategy:
        st.info(f"#### 🎯 Strategic Action Plan: {selected_segment}")

        # Business Logic playbooks mapped to corporate tier decisions
        if selected_segment == "Champions":
            st.success(
                "**Retention Campaign Plan:**\n* Provide VIP early access rewards.\n* Introduce a high-tier referral bonus code.\n* Keep transaction friction at zero."
            )
        elif selected_segment == "Loyal Customers":
            st.success(
                "**Value Optimization Plan:**\n* Pitch cross-sell multi-packs.\n* Ask for proactive user review postings.\n* Trigger custom loyalty tier perks."
            )
        elif selected_segment in [
            "At Severe Risk",
            "High Risk / Cant Lose Them",
            "About to Churn",
        ]:
            st.error(
                "**Re-engagement Plan:**\n* Issue limited-time high value coupons.\n* Trigger exit-intent user surveys.\n* Connect via high priority customer support check-ins."
            )
        else:
            st.warning(
                "**Nurture Campaign Plan:**\n* Focus on welcome bundle discounts.\n* Automate email educational drip flows.\n* Suggest highly trending product categories."
            )

        st.metric("Total Members in Group", f"{len(df_filtered):,}")
        st.metric(
            "Group Financial Value", f"${df_filtered['total_spending_usd'].sum():,.2f}"
        )

    with col_table:
        st.write(f"#### Active Target Rosters ({selected_segment})")
        st.dataframe(
            df_filtered[
                [
                    "customer_id",
                    "customer_name",
                    "country",
                    "recency_days",
                    "total_spending_usd",
                ]
            ].head(100),
            use_container_width=True,
        )

except Exception as e:
    st.error(
        f"⚠️ Database parsing error occurred. Please verify your database path is correct. Details: {e}"
    )
