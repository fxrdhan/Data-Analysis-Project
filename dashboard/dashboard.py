import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set_style("darkgrid", {"axes.facecolor": ".2", "grid.color": ".6"})
plt.style.use("dark_background")


def create_daily_orders_df(df):
    # Aggregate daily orders and revenue
    daily_orders_df = df.resample(rule="D", on="order_purchase_timestamp").agg(
        {"order_id": "nunique", "price": "sum"}
    )
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(
        columns={"order_id": "order_count", "price": "revenue"}, inplace=True
    )
    return daily_orders_df


def create_sum_order_items_df(df):
    # Calculate total orders per product category
    sum_order_items_df = (
        df.groupby("product_category_name")
        .order_item_id.count()
        .sort_values(ascending=False)
        .reset_index()
    )
    return sum_order_items_df


def create_rfm_df(df):
    # Calculate RFM metrics per customer
    rfm_df = df.groupby(by="customer_id", as_index=False).agg(
        {"order_purchase_timestamp": "max", "order_id": "nunique", "price": "sum"}
    )
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(
        lambda x: (recent_date - x).days
    )
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df


def create_daily_orders_status_df(df):
    # Create pivot table of daily order status counts
    daily_status_df = (
        df.groupby(["order_purchase_timestamp", "order_status"]).size().reset_index(name="count")
    )
    daily_status_pivot = daily_status_df.pivot(
        index="order_purchase_timestamp", columns="order_status", values="count"
    ).fillna(0)
    return daily_status_pivot


# Load and prepare data
all_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analysis-Project/refs/heads/main/e-commerce_public_dataset/all_df_cleaned.csv"
)

datetime_columns = ["order_purchase_timestamp", "shipping_limit_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# Streamlit configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Custom CSS for dark theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: transparent;
        color: white;
    }
    [data-testid="stMetricValue"] {
        background-color: transparent !important;
        color: white !important;
        padding: 10px !important;
        border-radius: 5px !important;
    }
    [data-testid="stMetricLabel"] {
        background-color: transparent !important;
        color: #B0B0B0 !important;
        padding: 10px !important;
        border-radius: 5px !important;
    }
    [data-testid="metric-container"] {
        background-color: transparent !important;
        border-radius: 5px !important;
        padding: 10px !important;
        border: 1px solid #2D2D2D !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar configuration
with st.sidebar:
    st.image(
        "https://github.com/fxrdhan/Data-Analysis-Project/blob/main/dashboard/pngwing.com.png?raw=true",
        width=200,
    )
    start_date, end_date = st.date_input(
        label="Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Filter data based on date range
main_df = all_df[
    (all_df["order_purchase_timestamp"] >= str(start_date)) & (all_df["order_purchase_timestamp"] <= str(end_date))
]

# Prepare dataframes
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
rfm_df = create_rfm_df(main_df)

# Dashboard header
st.header("E-commerce Dashboard :sparkles:")
st.subheader("Daily Orders")

# Key metrics
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
with col2:
    total_revenue = format_currency(
        daily_orders_df.revenue.sum(), "USD", locale="en_US"
    )
    st.metric("Total Revenue", value=total_revenue)

# Daily orders trend plot
fig, ax = plt.subplots(figsize=(16, 8), facecolor="#0E1117")
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.set_facecolor("#0E1117")
ax.tick_params(axis="y", labelsize=20, colors="white")
ax.tick_params(axis="x", labelsize=15, colors="white")
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")
ax.grid(True, alpha=0.2)
st.pyplot(fig)

# Order status analysis
st.subheader("Daily Orders Status")
daily_status_df = create_daily_orders_status_df(main_df)

# Status colors for consistency
status_colors = {
    "delivered": "#00CED1",
    "shipped": "#FFD700",
    "canceled": "#FF6B6B",
    "approved": "#98FB98",
    "invoiced": "#DDA0DD",
    "processing": "#87CEEB",
    "unavailable": "#D3D3D3",
}

# Order status stacked area chart
fig, ax = plt.subplots(figsize=(16, 8), facecolor="#0E1117")
ax.set_facecolor("#0E1117")

daily_status_df.plot(
    kind="area",
    stacked=True,
    ax=ax,
    color=[
        status_colors.get(status.lower(), "#333333")
        for status in daily_status_df.columns
    ],
    alpha=0.7,
)

ax.set_title("Daily Orders by Status", pad=20, color="white", fontsize=20)
ax.set_xlabel("Date", color="white", fontsize=12)
ax.set_ylabel("Number of Orders", color="white", fontsize=12)
ax.tick_params(axis="x", colors="white", labelsize=10)
ax.tick_params(axis="y", colors="white", labelsize=10)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["left"].set_color("white")
ax.spines["right"].set_color("white")
ax.grid(True, alpha=0.2)
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", frameon=False, labelcolor="white")

plt.tight_layout()
st.pyplot(fig)

# Order status summary
st.subheader("Order Status Summary")
status_summary = main_df["order_status"].value_counts()
total_orders = status_summary.sum()
cols = st.columns(len(status_summary))

for i, (status, count) in enumerate(status_summary.items()):
    percentage = (count / total_orders) * 100
    with cols[i]:
        st.metric(
            label=status.replace("_", " ").title(),
            value=f"{count:,}",
            delta=f"{percentage:.1f}%",
        )

# Product performance analysis
st.subheader("Best & Worst Performing Product Categories")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15), facecolor="#0E1117")
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Best performing products
sns.barplot(
    x="order_item_id",
    y="product_category_name",
    data=sum_order_items_df.head(5),
    palette=colors,
    hue="product_category_name",
    ax=ax[0],
)
ax[0].set_facecolor("#0E1117")
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30, color="white")
ax[0].tick_params(axis="y", labelsize=35, colors="white")
ax[0].tick_params(axis="x", labelsize=30, colors="white")
ax[0].spines["bottom"].set_color("white")
ax[0].spines["top"].set_color("white")
ax[0].spines["left"].set_color("white")
ax[0].spines["right"].set_color("white")

# Worst performing products
sns.barplot(
    x="order_item_id",
    y="product_category_name",
    data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5),
    palette=colors,
    hue="product_category_name",
    ax=ax[1],
)
ax[1].set_facecolor("#0E1117")
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30, color="white")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis="y", labelsize=35, colors="white")
ax[1].tick_params(axis="x", labelsize=30, colors="white")
ax[1].spines["bottom"].set_color("white")
ax[1].spines["top"].set_color("white")
ax[1].spines["left"].set_color("white")
ax[1].spines["right"].set_color("white")

plt.tight_layout()
st.pyplot(fig)

# RFM analysis
st.subheader("Best Customer Based on RFM Parameters")

# RFM metrics
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "USD", locale="en_US")
    st.metric("Average Monetary", value=avg_monetary)

# RFM visualization
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15), facecolor="#0E1117")
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

# Recency plot
sns.barplot(
    y="recency",
    x="customer_id",
    data=rfm_df.sort_values(by="recency", ascending=True).head(5),
    palette=colors,
    hue="customer_id",
    ax=ax[0],
)
ax[0].set_facecolor("#0E1117")
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=30, color="white")
ax[0].set_title("By Recency (days)", loc="center", fontsize=50, color="white")
ax[0].tick_params(axis="y", labelsize=10, colors="white")
ax[0].tick_params(axis="x", labelsize=15, colors="white")
ax[0].spines["bottom"].set_color("white")
ax[0].spines["top"].set_color("white")
ax[0].spines["left"].set_color("white")
ax[0].spines["right"].set_color("white")

# Frequency plot
sns.barplot(
    y="frequency",
    x="customer_id",
    data=rfm_df.sort_values(by="frequency", ascending=False).head(5),
    palette=colors,
    hue="customer_id",
    ax=ax[1],
)
ax[1].set_facecolor("#0E1117")
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=30, color="white")
ax[1].set_title("By Frequency", loc="center", fontsize=50, color="white")
ax[1].tick_params(axis="y", labelsize=10, colors="white")
ax[1].tick_params(axis="x", labelsize=15, colors="white")
ax[1].spines["bottom"].set_color("white")
ax[1].spines["top"].set_color("white")
ax[1].spines["left"].set_color("white")
ax[1].spines["right"].set_color("white")

# Monetary plot
sns.barplot(
    y="monetary",
    x="customer_id",
    data=rfm_df.sort_values(by="monetary", ascending=False).head(5),
    palette=colors,
    hue="customer_id",
    ax=ax[2],
)
ax[2].set_facecolor("#0E1117")
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=30, color="white")
ax[2].set_title("By Monetary", loc="center", fontsize=50, color="white")
ax[2].tick_params(axis="y", labelsize=10, colors="white")
ax[2].tick_params(axis="x", labelsize=15, colors="white")
ax[2].spines["bottom"].set_color("white")
ax[2].spines["top"].set_color("white")
ax[2].spines["left"].set_color("white")
ax[2].spines["right"].set_color("white")

plt.tight_layout()
st.pyplot(fig)

st.caption("Copyright © E-commerce Dashboard 20XX")
