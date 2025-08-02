import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
calldata = pd.read_csv("your_cleaned_data.csv")  # Replace with your actual file

st.set_page_config(page_title="Customer Care Call Dashboard", layout="wide")
st.title("📞 Customer Care Call Dashboard")

# ========== METRICS ==========
total_calls = len(calldata)
unique_callers = calldata["CALLER ALIAS"].nunique()
unknown_calls = (calldata["CALLER ALIAS"] == "Unknown Caller").sum()

col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Calls", total_calls)
col2.metric("👥 Unique Callers", unique_callers)
col3.metric("❓ Unknown Callers", unknown_calls)

st.markdown("---")

# ========== TOP CALLERS ==========
st.subheader("🔝 Top 10 Frequent Callers (Excluding Unknowns)")

# Filter out unknown callers
filtered_data = calldata[calldata["CALLER ALIAS"] != "Unknown Caller"]
caller_counts = (
    filtered_data["CALLER ALIAS"].value_counts().reset_index()
)
caller_counts.columns = ["Caller Alias", "Number of Calls"]
top_callers = caller_counts.head(10)

fig_top = px.bar(
    top_callers,
    x="Caller Alias",
    y="Number of Calls",
    color="Number of Calls",
    title="Top 10 Most Frequent Callers",
    template="plotly_white",
)
st.plotly_chart(fig_top, use_container_width=True)

# ========== CALLS BY TIME ==========
st.subheader("🕒 Call Volume by Hour")

if "time" in calldata.columns:
    calldata["HOUR"] = pd.to_datetime(calldata["time"], errors='coerce').dt.hour
    hourly_counts = calldata["HOUR"].value_counts().sort_index()
    fig_hour = px.line(
        hourly_counts,
        x=hourly_counts.index,
        y=hourly_counts.values,
        labels={"x": "Hour of Day", "y": "Number of Calls"},
        title="Call Volume Throughout the Day",
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig_hour, use_container_width=True)
else:
    st.warning("🕒 'time' column not found in data.")

# ========== CALL REASONS ==========
if "REASON FOR CALL" in calldata.columns:
    st.subheader("📌 Most Common Reasons for Calling")
    reason_counts = calldata["REASON FOR CALL"].value_counts().head(10).reset_index()
    reason_counts.columns = ["Reason", "Count"]

    fig_reason = px.pie(
        reason_counts,
        values="Count",
        names="Reason",
        title="Top 10 Reasons for Calling",
        hole=0.4,
        template="plotly_white"
    )
    st.plotly_chart(fig_reason, use_container_width=True)

# ========== RAW DATA ==========
with st.expander("📄 View Raw Data"):
    st.dataframe(calldata)

st.markdown("---")
st.caption("📞 Dashboard by Ray | Data from actual customer care operations")
