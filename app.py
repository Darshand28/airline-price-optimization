import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Airline Price Optimization Dashboard",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("✈️ Airline Price Optimization Dashboard")
st.markdown("""
Analyze airline ticket pricing using dynamic pricing algorithms,
demand forecasting, and revenue optimization analytics.
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("⚙️ Simulation Controls")

days_left = st.sidebar.slider(
    "Days Left Before Departure",
    min_value=1,
    max_value=30,
    value=15
)

tickets_left = st.sidebar.slider(
    "Available Tickets",
    min_value=20,
    max_value=300,
    value=120
)

base_demand = st.sidebar.slider(
    "Base Demand",
    min_value=50,
    max_value=300,
    value=150
)

# ---------------------------------------------------
# DYNAMIC PRICING FUNCTION
# ---------------------------------------------------
def dynamic_price(days_left, tickets_left, demand):
    scarcity_factor = max(1, 200 / tickets_left)
    urgency_factor = max(1, 30 / days_left)

    price = demand * scarcity_factor * urgency_factor * 0.6

    return round(price, 2)

# ---------------------------------------------------
# DATA SIMULATION
# ---------------------------------------------------
records = []

remaining_tickets = tickets_left

for day in range(days_left, 0, -1):

    demand_today = np.random.randint(
        base_demand - 20,
        base_demand + 20
    )

    current_price = dynamic_price(
        day,
        remaining_tickets,
        demand_today
    )

    tickets_sold = min(
        max(int((demand_today * 1.1) - current_price), 0),
        remaining_tickets
    )

    revenue = tickets_sold * current_price

    remaining_tickets -= tickets_sold

    records.append({
        "Day": day,
        "Demand": demand_today,
        "Ticket Price": current_price,
        "Tickets Sold": tickets_sold,
        "Revenue": revenue,
        "Tickets Remaining": remaining_tickets
    })

    if remaining_tickets <= 0:
        break

df = pd.DataFrame(records)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
total_revenue = df["Revenue"].sum()
avg_price = df["Ticket Price"].mean()
tickets_sold_total = df["Tickets Sold"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "🎟️ Tickets Sold",
    int(tickets_sold_total)
)

col3.metric(
    "📈 Average Price",
    f"${avg_price:.2f}"
)

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------
col4, col5 = st.columns(2)

# Price Trend
with col4:
    fig_price = px.line(
        df,
        x="Day",
        y="Ticket Price",
        markers=True,
        title="Ticket Price Trend"
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

# Revenue Chart
with col5:
    fig_revenue = px.bar(
        df,
        x="Day",
        y="Revenue",
        title="Daily Revenue"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

# ---------------------------------------------------
# DEMAND VS PRICE ANALYTICS
# ---------------------------------------------------
fig_scatter = px.scatter(
    df,
    x="Demand",
    y="Ticket Price",
    size="Revenue",
    color="Tickets Sold",
    hover_data=["Day"],
    title="Demand vs Ticket Price Analysis"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ---------------------------------------------------
# REVENUE FORECAST
# ---------------------------------------------------
st.subheader("📊 Revenue Forecast")

fig_area = px.area(
    df,
    x="Day",
    y="Revenue",
    title="Revenue Forecast Trend"
)

st.plotly_chart(
    fig_area,
    use_container_width=True
)

# ---------------------------------------------------
# INSIGHTS SECTION
# ---------------------------------------------------
st.subheader("🧠 Business Insights")

best_day = df.loc[df["Revenue"].idxmax()]

st.success(
    f"""
    Highest revenue generated on Day {int(best_day['Day'])}
    with revenue of ${best_day['Revenue']:.0f}.
    """
)

if avg_price > 150:
    st.info(
        "High dynamic pricing detected due to high demand and low ticket availability."
    )
else:
    st.warning(
        "Pricing is moderate. Increasing ticket prices during peak demand may improve revenue."
    )

if remaining_tickets < 20:
    st.error(
        "Very limited tickets remaining. Scarcity pricing can maximize profits."
    )

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("📋 Simulation Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD CSV
# ---------------------------------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name="airline_price_analytics.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "Developed using Streamlit, Plotly, Pandas, and NumPy"
)
