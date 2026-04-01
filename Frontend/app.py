import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

# Page Config
st.set_page_config(
    page_title="Smart Money Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------------------
# Custom Styling
# ---------------------------

st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#00E5FF;
}

.metric-card{
    background:linear-gradient(135deg,#2b5876,#4e4376);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">💰 Smart Money Tracker Dashboard</p>', unsafe_allow_html=True)

# ---------------------------
# Sidebar Navigation
# ---------------------------

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Transaction", "Budget Manager", "Insights"]
)

# ---------------------------
# Dashboard
# ---------------------------

if menu == "Dashboard":

    st.subheader("📊 Financial Overview")

    response = requests.get(f"{API_URL}/transactions")

    if response.status_code == 200:

        transactions = response.json()

        if len(transactions) == 0:
            st.info("No transactions yet.")
        else:

            df = pd.DataFrame(transactions)

            income = df[df["type"] == "income"]["amount"].sum()
            expense = df[df["type"] == "expense"]["amount"].sum()
            balance = income - expense

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Income", f"₹{income}")
            col2.metric("💸 Expense", f"₹{expense}")
            col3.metric("🏦 Balance", f"₹{balance}")

            st.divider()

            st.subheader("Transaction History")
            st.dataframe(df, use_container_width=True)

            st.divider()

            expense_df = df[df["type"] == "expense"]

            if not expense_df.empty:

                col1, col2 = st.columns(2)

                with col1:
                    pie = px.pie(
                        expense_df,
                        values="amount",
                        names="category",
                        title="Expenses by Category",
                        color_discrete_sequence=px.colors.sequential.Teal
                    )
                    st.plotly_chart(pie, use_container_width=True)

                with col2:
                    bar = px.bar(
                        expense_df,
                        x="category",
                        y="amount",
                        color="category",
                        title="Spending by Category"
                    )
                    st.plotly_chart(bar, use_container_width=True)

# ---------------------------
# Add Transaction
# ---------------------------

elif menu == "Add Transaction":

    st.subheader("➕ Add Transaction")

    col1, col2 = st.columns(2)

    amount = col1.number_input("Amount", min_value=0.0)

    t_type = col2.selectbox(
        "Transaction Type",
        ["income", "expense"]
    )

    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]
    )

    description = st.text_input("Description")

    date = st.date_input("Date")

    if st.button("Submit Transaction"):

        payload = {
            "amount": amount,
            "type": t_type,
            "category": category,
            "description": description,
            "date": str(date)
        }

        r = requests.post(
            f"{API_URL}/add-transaction",
            json=payload
        )

        if r.status_code == 200:
            st.success("Transaction added successfully!")

# ---------------------------
# Budget Manager
# ---------------------------

elif menu == "Budget Manager":

    st.subheader("💳 Set Monthly Budget")

    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Shopping", "Bills", "Entertainment"]
    )

    limit = st.number_input("Monthly Limit", min_value=0.0)

    month = st.text_input("Month (Example: 2026-03)")

    if st.button("Save Budget"):

        payload = {
            "category": category,
            "monthly_limit": limit,
            "month": month
        }

        r = requests.post(
            f"{API_URL}/set-budget",
            json=payload
        )

        if r.status_code == 200:
            st.success("Budget saved!")

# ---------------------------
# Insights
# ---------------------------

elif menu == "Insights":

    st.subheader("🧠 Smart Spending Insights")

    r = requests.get(f"{API_URL}/spending-insights")

    if r.status_code == 200:

        insights = r.json()["suggestions"]

        if len(insights) == 0:
            st.success("No warnings. You're managing money well!")

        for i in insights:
            st.warning(i)