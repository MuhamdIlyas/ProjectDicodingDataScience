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
    sum_order = df.groupby("product_category_name").product_id.nunique(
    ).sort_values(ascending=False).reset_index()
    return sum_order


# create_state() digunakan untuk menyiapkan state
def create_state(df):
    state = df.groupby(
        by="customer_city").product_id.nunique().reset_index()

    return state

# create_order_status() digunakan untuk menyiapkan order_statuse


def create_order_status(df):
    order_status = df.groupby(
        by="order_status").product_id.nunique().reset_index()

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
    st.title("Toko Kita")
    st.image("https://raw.githubusercontent.com/MuhamdIlyas/ProjectDicodingDataScience/a773b6e2b6b6b1a890c7ccf635de83fc9b487de2/erica-zhou-IHpUgFDn7zU-unsplash.jpg",
             width=None, use_column_width=None)
    # https://unsplash.com/photos/IHpUgFDn7zU

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# start_date dan end_date di atas akan digunakan untuk memfilter all_dataset. Data yang telah difilter ini selanjutnya akan disimpan dalam main_dataset
main_dataset = all_dataset[(all_dataset["order_approved_at"] >= str(start_date)) &
                           (all_dataset["order_approved_at"] <= str(end_date))]

daily_order = create_orders_daily(main_dataset)
sum_order = create_sum_order(main_dataset)
state = create_state(main_dataset)
order_status = create_order_status(main_dataset)
# rfm_df = create_rfm_df(main_dataset)

# Menambahkan Header
st.header('Toko Kita Dashboard :sparkles:')

# menampilkan informasi total order dan revenue dalam bentuk metric() yang ditampilkan menggunakan layout columns()
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_order.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(
        daily_order.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

# Perfoma penjualan
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_order["order_approved_at"].values,
    daily_order["order_count"].values,
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

st.pyplot(fig)

# Menampilkan 5 produk paling laris dan paling sedikit terjual melalui sebuah visualisasi data
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_id", y="product_category_name",
            data=sum_order.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None, fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="product_id", y="product_category_name", data=sum_order.sort_values(
    by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None, fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# # Menampilkan Kota Bagian (state) apa saja dengan customer terbanyak yang dimiliki perusahaan
# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3",
#           "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# sns.barplot(
#     x="customer_city",
#     y="product_id",
#     data=state.sort_values(by="customer_city", ascending=False),
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Number of Customer by States", loc="center", fontsize=30)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
# st.pyplot(fig)

# # Menampilkan proses transaksi yang paling diminati
# fig, ax = plt.subplots(figsize=(20, 10))
# colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3",
#           "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# sns.barplot(
#     x="order_status",
#     y="product_id",
#     data=order_status.sort_values(by="order_status", ascending=False),
#     palette=colors,
#     ax=ax
# )
# ax.set_title("Most Popular Transaction Processes", loc="center", fontsize=50)
# ax.set_ylabel(None)
# ax.set_xlabel(None)
# ax.tick_params(axis='x', labelsize=35)
# ax.tick_params(axis='y', labelsize=30)
# st.pyplot(fig)
