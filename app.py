import streamlit as st
import pandas as pd
import sqlite3
import config
import os
import datetime
from logger import logger

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Tech Intelligence Pipeline", page_icon="🎯", layout="wide"
)

logger.info("Streamlit app loaded")

# --- HEADER ---
st.title("📊 Career Market Engine")
st.markdown("### Automated Career Market Analysis")

# --- DATA LOAD ---
if not os.path.exists(config.DB_PATH):
    logger.error(f"Database not found at {config.DB_PATH}")
    st.error("Warehouse not found. Run the pipeline first.")
else:
    try:
        conn = sqlite3.connect(config.DB_PATH)

        # Simple query for the core data
        df = pd.read_sql_query(
            "SELECT company, title, location, link FROM global_jobs", conn
        )
        
        logger.info(f"Loaded {len(df)} jobs from database")

        # --- SIDEBAR ---
        st.sidebar.header("Controls")
        search = st.sidebar.text_input("Search Company or Title")

        # Get unique locations and sort them
        locations = sorted(df["location"].unique().tolist())
        location_filter = st.sidebar.multiselect("Filter by Location", options=locations)

        # Sidebar Status (Honest version)
        st.sidebar.markdown("---")
        st.sidebar.subheader("System Status")
        # Just check the file date
        last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(config.DB_PATH))
        st.sidebar.write(f"**Data Last Updated:** {last_mod.strftime('%b %d, %H:%M')}")

        # --- FILTERING LOGIC ---
        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[
                filtered_df["company"].str.contains(search, case=False)
                | filtered_df["title"].str.contains(search, case=False)
            ]
            logger.info(f"Search filter applied: {search} -> {len(filtered_df)} results")
            
        if location_filter:
            filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]
            logger.info(f"Location filter applied: {location_filter} -> {len(filtered_df)} results")

        # --- METRICS ---
        col1, col2 = st.columns(2)
        col1.metric("Roles Analyzed", len(filtered_df))
        col2.metric("Market Sources", filtered_df["company"].nunique())

        # --- MAIN TABLE ---
        st.dataframe(
            filtered_df,
            column_config={
                "link": st.column_config.LinkColumn("Apply"),
                "company": "Company",
                "title": "Role Title",
                "location": "Location",
            },
            use_container_width=True,
            hide_index=True,
        )

        conn.close()

        st.info("💡 Pro-tip: Filter for 'Remote' to see work-from-home opportunities.")
        
    except sqlite3.Error as e:
        logger.error(f"Database error in Streamlit app: {e}", exc_info=True)
        st.error(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in Streamlit app: {e}", exc_info=True)
        st.error(f"Unexpected error: {e}")
