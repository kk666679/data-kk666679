import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import requests

st.set_page_config(page_title="HRMS Malaysia Dashboard", layout="wide")

st.title("🇲🇾 HRMS Malaysia - Executive Dashboard")

# Sidebar
st.sidebar.header("Dashboard Controls")
date_range = st.sidebar.date_input("Select Date Range", [datetime.now() - timedelta(30), datetime.now()])

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Employees", "1,247", "+12")

with col2:
    st.metric("Monthly Payroll", "RM 2.8M", "+5.2%")

with col3:
    st.metric("EPF Contributions", "RM 312K", "+3.1%")

with col4:
    st.metric("HRDF Claims", "RM 45K", "+15%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Sentiment Analysis")
    sentiment_data = pd.DataFrame({
        'Department': ['IT', 'HR', 'Finance', 'Operations'],
        'Positive': [85, 92, 78, 88],
        'Neutral': [10, 5, 15, 8],
        'Negative': [5, 3, 7, 4]
    })
    
    fig = px.bar(sentiment_data, x='Department', y=['Positive', 'Neutral', 'Negative'],
                 title="Employee Sentiment by Department")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Attrition Risk Prediction")
    risk_data = pd.DataFrame({
        'Risk Level': ['Low', 'Medium', 'High'],
        'Employees': [1050, 150, 47]
    })
    
    fig = px.pie(risk_data, values='Employees', names='Risk Level',
                 title="Employee Attrition Risk Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Recent activities
st.subheader("Recent HR Activities")
activities = pd.DataFrame({
    'Time': ['10:30 AM', '11:15 AM', '2:45 PM', '4:20 PM'],
    'Activity': ['New Employee Onboarded', 'Leave Request Approved', 'Payroll Calculated', 'Training Completed'],
    'Employee': ['Ahmad Rahman', 'Siti Nurhaliza', 'Batch Process', 'Lim Wei Ming'],
    'Status': ['✅ Completed', '✅ Approved', '✅ Success', '✅ Certified']
})

st.dataframe(activities, use_container_width=True)

# AI Insights
st.subheader("🤖 AI-Powered Insights")
st.info("💡 **Recommendation**: IT Department shows highest engagement. Consider implementing similar practices in Finance.")
st.warning("⚠️ **Alert**: 47 employees identified as high attrition risk. Schedule retention meetings.")
st.success("✅ **Achievement**: HRDF claims increased by 15% this month, maximizing training ROI.")