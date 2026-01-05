import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import text

from app.db import engine

st.set_page_config(
    page_title="Job Market Intelligence",
    layout="wide",
)

st.title("📊 Job Market Intelligence Dashboard")


@st.cache_data(ttl=300)
def load_job_counts():
    query = """
    SELECT COUNT(*) AS total_jobs FROM jobs
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def load_skill_counts(limit=20):
    query = f"""
    SELECT s.name AS skill, COUNT(*) AS count
    FROM job_skills js
    JOIN skills s ON s.id = js.skill_id
    GROUP BY s.name
    ORDER BY count DESC
    LIMIT {limit}
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def load_jobs_by_skill(skill: str):
    query = """
    SELECT j.title, j.location, j.url
    FROM jobs j
    JOIN job_skills js ON js.job_id = j.id
    JOIN skills s ON s.id = js.skill_id
    WHERE s.name = :skill
    LIMIT 50
    """
    return pd.read_sql(text(query), engine, params={"skill": skill})


# ------------------------
# Metrics
# ------------------------

col1, col2 = st.columns(2)

job_count_df = load_job_counts()
col1.metric("Total Jobs", int(job_count_df.iloc[0]["total_jobs"]))

skill_df = load_skill_counts()
col2.metric("Total Skills Tracked", skill_df.shape[0])

st.divider()

# ------------------------
# Skill distribution
# ------------------------

st.subheader("🔥 Top Skills in Demand")

fig = px.bar(
    skill_df,
    x="skill",
    y="count",
    text="count",
    title="Top Skills by Job Mentions",
)

fig.update_layout(xaxis_title="Skill", yaxis_title="Job Count")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ------------------------
# Drill-down
# ------------------------

st.subheader("🔎 Explore Jobs by Skill")

selected_skill = st.selectbox("Select a skill", skill_df["skill"].tolist())

jobs_df = load_jobs_by_skill(selected_skill)

st.dataframe(
    jobs_df,
    use_container_width=True,
)
