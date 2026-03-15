import streamlit as st

st.set_page_config(
    page_title="Hospitality Analytics Dashboard",
    page_icon="🏨",
    layout="wide",
)

st.title("Hospitality Analytics Dashboard")
st.caption("Databricks lakehouse project with hotel booking metrics and AI-generated insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Bookings", "—")

with col2:
    st.metric("Cancellation Rate", "—")

with col3:
    st.metric("Average ADR", "—")

with col4:
    st.metric("Realized Booking Value", "—")

st.subheader("AI Insight Summary")
st.info("AI-generated insights will appear here.")

st.subheader("Trends")
st.write("Charts will go here.")

st.subheader("Exploration")
st.write("Filters and deeper analysis will go here.")