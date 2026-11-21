from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Olist E-Commerce Dashboard", layout="wide")

BLUE = "#2a6f97"
RED = "#c1666b"
ORANGE = "#e9a03b"


@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "main_data.csv",
                     parse_dates=["order_purchase_timestamp"])

    df = df.dropna(subset=["is_late"])
    df["is_late"] = df["is_late"].astype(bool)
    return df


def make_rfm(df):
    rfm = df.groupby("customer_unique_id").agg(
        last_order=("order_purchase_timestamp", "max"),
        frequency=("order_id", "nunique"),
        monetary=("price", "sum"),
    ).reset_index()
    recent = rfm["last_order"].max() + pd.Timedelta(days=1)
    rfm["recency"] = (recent - rfm["last_order"]).dt.days

    rfm["r_score"] = pd.qcut(rfm["recency"].rank(
        method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(
        method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    # mayoritas pelanggan hanya belanja 1x, jadi frequency dibagi 2 kelompok
    rfm["f_score"] = np.where(rfm["frequency"] >= 2, 2, 1)

    def segment(row):
        if row["f_score"] == 2 and row["r_score"] >= 3:
            return "Loyal"
        if row["r_score"] >= 3 and row["m_score"] >= 3:
            return "Big Spender Baru"
        if row["r_score"] <= 2 and row["m_score"] >= 3:
            return "At Risk (Spender Besar)"
        if row["r_score"] <= 2:
            return "Lost / Dormant"
        return "Regular"

    rfm["segment"] = rfm.apply(segment, axis=1)
    return rfm


data = load_data()

# sidebar
st.sidebar.header("Filter")
min_d = data["order_purchase_timestamp"].min().date()
max_d = data["order_purchase_timestamp"].max().date()
date_range = st.sidebar.date_input("Rentang tanggal order", value=(
    min_d, max_d), min_value=min_d, max_value=max_d)

if len(date_range) == 2:
    start, end = date_range
    data = data[
        (data["order_purchase_timestamp"].dt.date >= start)
        & (data["order_purchase_timestamp"].dt.date <= end)
    ]

st.title("Olist E-Commerce Dashboard")
st.caption("Hanya order berstatus delivered")

# ringkasan
orders = data.drop_duplicates("order_id")
c1, c2, c3 = st.columns(3)
c1.metric("Total Order", f"{orders['order_id'].nunique():,}")
c2.metric("Total Revenue", f"R$ {data['price'].sum():,.0f}")
c3.metric("Pelanggan Unik", f"{data['customer_unique_id'].nunique():,}")

# pertanyaan1
st.header("1. Revenue per Kategori Produk")
rev = (
    data.groupby("product_category_name_english")["price"].sum()
    .sort_values(ascending=False).reset_index()
)
top5, bottom5 = rev.head(5), rev.tail(5)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=top5, x="price",
                y="product_category_name_english", ax=ax, color=BLUE)
    ax.set_title("5 Kategori Revenue Tertinggi")
    ax.set_xlabel("Revenue (R$)")
    ax.set_ylabel("")
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=bottom5, x="price",
                y="product_category_name_english", ax=ax, color=RED)
    ax.set_title("5 Kategori Revenue Terendah")
    ax.set_xlabel("Revenue (R$)")
    ax.set_ylabel("")
    st.pyplot(fig)

top_share = top5["price"].sum() / rev["price"].sum() * 100
st.info(
    f"5 kategori teratas menyumbang **{top_share:.1f}%** dari total revenue pada periode terpilih.")

# pertanyaan2
st.header("2. Keterlambatan Pengiriman vs Review Score")
# satu baris per order
ord_df = orders.dropna(subset=["review_score", "delivery_time"])

if len(ord_df) > 0 and ord_df["is_late"].nunique() == 2:
    rating = ord_df.groupby("is_late")["review_score"].mean()
    corr = ord_df["delivery_time"].corr(ord_df["review_score"])

    m1, m2, m3 = st.columns(3)
    m1.metric("Rating tepat waktu", f"{rating[False]:.2f}")
    m2.metric("Rating terlambat", f"{rating[True]:.2f}")
    m3.metric("Korelasi delivery_time vs rating", f"{corr:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=["Tepat waktu", "Terlambat"], y=[rating[False], rating[True]],
                    ax=ax, hue=["Tepat waktu", "Terlambat"],
                    palette=[BLUE, RED], legend=False)
        ax.set_ylim(0, 5)
        ax.set_ylabel("Rata-rata review score")
        ax.set_title("Rating: Tepat Waktu vs Terlambat")
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        bins = pd.cut(ord_df["delivery_time"], [-1, 7, 14, 21, 30, 200],
                      labels=["<=7 hari", "8-14 hari", "15-21 hari",
                              "22-30 hari", ">30 hari"])
        by_bin = ord_df.groupby(bins, observed=True)[
            "review_score"].mean().reset_index()
        sns.barplot(data=by_bin, x="delivery_time",
                    y="review_score", ax=ax, color=BLUE)
        ax.set_ylim(0, 5)
        ax.set_xlabel("Durasi pengiriman")
        ax.set_ylabel("Rata-rata review score")
        ax.set_title("Rating per Durasi Pengiriman")
        st.pyplot(fig)
else:
    st.warning(
        "Data pada rentang ini belum cukup untuk membandingkan order terlambat dan tepat waktu.")

# pertanyaan3
st.header("3. Segmentasi Pelanggan (RFM)")
rfm = make_rfm(data)
seg = rfm.groupby("segment").agg(
    jumlah=("customer_unique_id", "count"),
    total_spent=("monetary", "sum"),
    avg_recency=("recency", "mean"),
).sort_values("total_spent", ascending=False).reset_index()

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=seg, x="jumlah", y="segment", ax=ax, color=BLUE)
    ax.set_title("Jumlah Pelanggan per Segmen")
    ax.set_ylabel("")
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=seg, x="total_spent", y="segment", ax=ax, color=ORANGE)
    ax.set_title("Total Spending per Segmen (R$)")
    ax.set_ylabel("")
    st.pyplot(fig)

st.dataframe(seg, use_container_width=True)

# analisis lanjutan: geospatial per state
st.header("4. Analisis Lanjutan: Persentase Order Terlambat per State")
if "customer_state" in data.columns:
    state = orders.dropna(subset=["is_late"]).groupby("customer_state").agg(
        jumlah_order=("order_id", "count"),
        persen_terlambat=("is_late", lambda x: x.astype(float).mean() * 100),
    ).reset_index()
    # hanya state dengan jumlah order memadai (>= 500) agar persentasenya stabil
    state = state[state["jumlah_order"] >= 500].sort_values(
        "persen_terlambat", ascending=False)
    top_state = state.head(10)

    overall_late = orders["is_late"].astype(float).mean() * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top_state, x="persen_terlambat",
                y="customer_state", ax=ax, color=RED)
    ax.axvline(overall_late, color="gray", linestyle="--",
               label=f"Rata-rata seluruh order ({overall_late:.1f}%)")
    ax.set_title("10 State dengan Persentase Order Terlambat Tertinggi")
    ax.set_xlabel("Persentase Order Terlambat (%)")
    ax.set_ylabel("State")
    ax.legend()
    st.pyplot(fig)
    st.caption(
        "Hanya state dengan minimal 500 order yang ditampilkan agar persentase keterlambatan stabil.")
else:
    st.info("Kolom customer_state tidak tersedia pada data.")
