# mengimpor seluruh library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# create_daily_orders() digunakan untuk menyiapkan daily_orders


def create_orders_daily(df):
    create_orders_daily = df.resample(rule='M', on='order_approved_at').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    create_orders_daily.index = create_orders_daily.index.strftime(
        '%Y-%m-%d')  # mengubah format order date menjadi nama bulan
    create_orders_daily = create_orders_daily.reset_index()
    create_orders_daily.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    return create_orders_daily


# create_sum_order() untuk menyiapkan sum_orders
def create_sum_order(df):
    sum_order = df.groupby("product_category_name").product_id.sum(
    ).sort_values(ascending=False).reset_index()
    return sum_order


# create_state() digunakan untuk menyiapkan state
def create_state(df):
    state = df.groupby(by="customer_city").product_id.nunique().reset_index()
    state.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return state

# create_order_status() digunakan untuk menyiapkan order_statuse


def create_order_status(df):
    order_status = df.groupby(
        by="order_status").product_id.nunique().reset_index()
    order_status.rename(columns={
        "product_id": "customer_count"
    }, inplace=True)

    return order_status


# Menyimpan berkas data dari google colba.
all_dataset = pd.read_csv("all_dataset.csv")

# Filter untuk kolom order_approved_at dan order_status
datetime_columns = ["order_approved_at", "order_status"]
all_dataset.sort_values(by="order_approved_at", inplace=True)
all_dataset.reset_index(inplace=True)

all_dataset_index = all_dataset.set_index('order_approved_at')

for column in datetime_columns:
    all_dataset[column] = pd.to_datetime(all_dataset['order_approved_at'])

# membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar
min_date = all_dataset["order_approved_at"].min()
max_date = all_dataset["order_approved_at"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://unsplash.com/photos/IHpUgFDn7zU")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
