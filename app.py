import streamlit as st
import pandas as pd
import sqlite3
import config
import os
import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Tech Intelligence Pipeline", page_icon="🎯", layout="wide"
)

# --- HEADER ---
st.title("📊 Career Market Engine")
st.markdown("### Automated Career Market Analysis")

# --- DATA LOAD ---
if not os.path.exists(config.DB_PATH):
    st.error("Warehouse not found. Run the pipeline first.")
else:
    conn = sqlite3.connect(config.DB_PATH)

    # Simple query for the core data
    df = pd.read_sql_query(
        "SELECT company, title, location, link FROM global_jobs", conn
    )

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
    st.sidebar.info("Status: Local Manual Run")

    # --- FILTERING LOGIC ---
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[
            filtered_df["company"].str.contains(search, case=False)
            | filtered_df["title"].str.contains(search, case=False)
        ]
    if location_filter:
        filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]

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
