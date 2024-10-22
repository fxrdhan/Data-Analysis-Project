# %% [markdown]
# <a target="_blank" href="https://colab.research.google.com/github/fxrdhan/Data-Analytics-Project/blob/main/notebook.ipynb">
#   <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
# </a>
# 

# %% [markdown]
# # Proyek Analisis Data: E-Commerce Public Dataset
# 
# - **Nama:** Firdaus Arif Ramadhani
# - **Email:** firdausarief65@gmail.com
# - **ID Dicoding:** 2VX3464E3ZYQ
# 

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis
# 

# %% [markdown]
# 1. Kategori produk apa saja yang paling laris?
# 2. Apa faktor utama yang menyebabkan pembatalan pesanan?
# 3. Bagaimana pengaruh interval pengiriman terhadap tingkat kepuasan pelanggan?
# 4. Bagaimana performa berbagai kategori produk dalam hal kepuasan pelanggan?
# 5. Bagaimana tren penjualan bulanan?
# 

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan
# 

# %%
import random
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from collections import Counter
from deep_translator import GoogleTranslator as Translator
from wordcloud import WordCloud

# %% [markdown]
# ## Data Wrangling
# 

# %% [markdown]
# ### Gathering Data
# 

# %% [markdown]
# #### Data Tabel `products_df`
# 

# %%
products_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/products_dataset.csv"
)
products_df.head()

# %% [markdown]
# **Insight:**\
# Dataset products_df berisi informasi terkait produk.\
# Informasi yang tersedia diantaranya:
# 
# 1. `product_id`: ID unik untuk setiap produk.
# 2. `product_category_name`: Panjang nama produk dalam karakter.
# 3. `product_name_lenght`: Panjang deskripsi produk.
# 4. `product_photos_qty`: Jumlah foto yang tersedia untuk produk.
# 5. `product_weight_g`: Berat produk.
# 6. `product_length_cm`, `product_height_cm`, dan `product_width_cm`: DImensi produk.
# 

# %% [markdown]
# #### Data Tabel `product_category_translation_df`
# 

# %%
product_category_translation_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/product_category_name_translation.csv"
)
product_category_translation_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `product_category_translation_df` memuat terjemahan nama kategori produk dari bahasa Portugis ke bahasa Inggris.\
# Informasi yang tertera diantaranya:
# 
# 1. `product_category_name`: Nama kategori dalam bahasa Portugis.
# 2. `product_category_name_english`: Nama kategori dalam bahasa Inggris.
# 

# %% [markdown]
# #### Data Tabel `order_reviews_df`
# 

# %%
order_reviews_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/order_reviews_dataset.csv"
)
order_reviews_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `order_reviews_df` berisi informasi mengenai ulasan pelanggan terhadap pesanan yang telah mereka terima.\
# Informasi yang tertera diantaranya:
# 
# 1. `review_id`: ID unik untuk setiap ulasan.
# 2. `order_id`: ID unik dari pesanan.
# 3. `review_score`: Skor ulasan yang diberikan oleh pelanggan, pada skala 1-5.
# 4. `review_comment_title` & `review_comment_message`: Komentar pelanggan.
# 5. `review_creation_date` $ `review_answer_timestamp`: Waktu ketika ulasan dibuat dan dijawab.
# 

# %% [markdown]
# #### Data Tabel `order_payments`
# 

# %%
order_payments_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/order_payments_dataset.csv"
)
order_payments_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `order_payments` ini berisi informasi mengenai pembayaran yang dilakukan pelanggan untuk pesanan yang mereka buat.\
# Informasi yang tertera diantaranya:
# 
# 1. `order_id`: ID unik untuk setiap pesanan.
# 2. `payment_sequential`: Urutan pembayaran untuk setiap pesanan.
# 3. `payment_type`: Jenis pembayaran yang digunakan oleh pelanggan.
# 4. `payment_installments`: Jumlah cicilan yang diambil oleh pelanggan untuk membayar pesanan.
# 5. `payment_value`: Nilai total dari setiap pembayaran.
# 

# %% [markdown]
# #### Data Tabel `order_items_df`
# 

# %%
order_items_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/order_items_dataset.csv"
)
order_items_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `order_items_df` berisi informasi mengenai item yang dipesan dalam setiap pesanan.\
# Informasi yang tertera diantaranya:
# 
# 1. `order_id`: ID unik untuk setiap pesanan.
# 2. `order_item_id`: ID untuk setiap item pesanan dalam pesanan yang sama.
# 3. `product_id`: ID produk yang dipesan.
# 4. `seller_id`: ID unik penjual.
# 5. `shipping_limit_date`: Batas waktu pengiriman item oleh penjual.
# 6. `price`: Harga jual produk yang dipesan.
# 7. `freight_value`: Biaya pengiriman item.
# 

# %% [markdown]
# #### Data Tabel `geolocation_df`
# 

# %%
geolocation_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/geolocation_dataset.csv"
)
geolocation_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `geolocation_df` berisi informasi geolokasi.\
# Informasi yang tertera diantaranya:
# 
# 1. `geolocation_zip_code_prefix`: Kode pos.
# 2. `geolocation_lat`: Koordinat geografis lintang.
# 3. `geolocation_lng`: Koordinat geografis bujur.
# 4. `geolocation_city`: Nama kota.
# 5. `geolocation_state`: Nama negara bagian.
# 

# %% [markdown]
# #### Data Tabel `customers_df`
# 

# %%
customers_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/customers_dataset.csv"
)
customers_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `customers_df` berisi informasi mengenai pelanggan yang melakukan pemesanan.\
# Informasi yang tertera diantaranya:
# 
# 1. `customer_id`: ID pelanggan untuk setiap pesanan.
# 2. `customer_unique_id`: ID unik pelanggan.
# 3. `customer_zip_code_prefix`: Kode pos pelanggan.
# 4. `customer_city`: Nama kota pelanggan.
# 5. `customer_state`: Nama negara bagian pelanggan.
# 

# %% [markdown]
# #### Data Tabel `sellers_df`
# 

# %%
sellers_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/sellers_dataset.csv"
)
sellers_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `sellers_df` berisi informasi penjual\
# Informasi yang tertera diantaranya:
# 
# 1. `seller_id`: ID penjual.
# 2. `seller_zip_code_prefix`: Kode pos penjual.
# 3. `seller_city`: Nama kota penjual.
# 4. `seller_state`: Nama negara bagian penjual.
# 

# %% [markdown]
# #### Data Tabel `orders_df`
# 

# %%
orders_df = pd.read_csv(
    "https://media.githubusercontent.com/media/fxrdhan/Data-Analytics-Project/refs/heads/main/e-commerce_public_dataset/orders_dataset.csv"
)
orders_df.head()

# %% [markdown]
# **Insight:**\
# Dataset `orders_df` berisi informasi mengenai pesanan yang dibuat oleh pelanggan.\
# Informasi yang tertera diantaranya:
# 
# 1. `order_id`: ID unik untuk setiap pesanan.
# 2. `customer_id`: ID pelanggan yang terkait dengan pesanan.
# 3. `order_status`: Status pesanan yang menunjukkan tahapan pesanan seperti delivered, shipped, canceled, dll.
# 4. `order_purchase_timestamp`: Tanggal dan waktu pesanan dibuat.
# 5. `order_approved_at`: Waktu persetujuan pesanan.
# 6. `order_delivered_carrier_date`: Tanggal pesanan dikirim ke pelanggan oleh kurir.
# 7. `order_delivered_customer_date`: Tanggal pesanan diterima oleh pelanggan.
# 8. `order_estimated_delivery_date`: Estimasi tanggal pengiriman pesanan.
# 

# %% [markdown]
# ### Assessing Data
# 

# %% [markdown]
# #### Menilai Tabel `products_df`
# 

# %%
products_df.info()

# %%
print("\nMissing values in Products dataset:")
products_df.isna().sum()

# %%
print("Duplicates in Products dataset:", products_df.duplicated().sum())

# %%
products_df["product_weight_g"].describe().round(2)

# %% [markdown]
# **Insight:**\
# Tidak ada data duplikat.\
# Terdapat beberapa kolom memiliki nilai yang hilang.\
# Rentang nilai `product_weight_g` cukup besar, mulai dari **0.00** hingga **40425** gram, yang menunjukkan adanya anomali pada nilai minimum. Nilai **0.00** pada berat produk tampak tidak logis.
# 

# %% [markdown]
# #### Menilai Tabel `product_category_translation_df`
# 

# %%
product_category_translation_df.info()

# %%
print("\nMissing values in Product Category Translation dataset:")
product_category_translation_df.isna().sum()

# %%
print(
    "Duplicates in Product Category Translation dataset:",
    product_category_translation_df.duplicated().sum(),
)

# %% [markdown]
# **Insight:**\
# Setiap kategori produk dalam bahasa Portugis dan terjemahan bahasa Inggris, sesuai dengan jumlah total entri **(71)**.\
# Tidak memiliki nilai yang hilang atau duplikat.
# 

# %% [markdown]
# #### Menilai Tabel `order_reviews_df`
# 

# %%
order_reviews_df.info()

# %%
print("\nMissing values in Order Reviews dataset:")
order_reviews_df.isna().sum()

# %%
print("Duplicates in Order Reviews dataset:", order_reviews_df.duplicated().sum())

# %% [markdown]
# **Insight:**\
# Anomali pada kolom `review_creation_date` & `review_answer_timestamp` yang bertipe data _object_ (teks).
# Terdapat banyak nilai yang hilang pada entri `review_comment_title` dan `review_comment_message`.\
# Tidak ada baris yang duplikat.\
# 

# %% [markdown]
# #### Menilai Tabel `order_payments_df`
# 

# %%
order_payments_df.info()

# %%
print("\nMissing values in Order Payments dataset:")
order_payments_df.isna().sum()

# %%
print("Duplicates in Order Payments dataset:", order_payments_df.duplicated().sum())

# %%
order_payments_df.describe()

# %% [markdown]
# **Insight:**\
# Tidak ada _missing values_.\
# Tidak ada data duplikat.\
# Pada kolom `payment_installments` dengan minimum value **0.00**, yang mungkin menunjukkan pembayaran tanpa cicilan.\
# Pada kolom `payment_value`, nilai minimum adalah **0.00**, yang mungkin barang tersebut digratiskan atau sedang promo.
# 

# %% [markdown]
# #### Menilai Tabel `order_items_df`
# 

# %%
order_items_df.info()

# %%
print("\nMissing values in Order Items dataset:")
order_items_df.isna().sum()

# %%
print("Duplicates in Order Items dataset:", order_items_df.duplicated().sum())

# %% [markdown]
# **Insight:**\
# Anomali pada kolom `shipping_limit_date` yang bertipe data _object_ (teks).\
# Tidak ada _missing values_.\
# Tidak ada baris yang duplikat.
# 

# %% [markdown]
# #### Menilai Tabel `geolocation_df`
# 

# %%
geolocation_df.info()

# %%
print("\nMissing values in Geolocation dataset:")
geolocation_df.isna().sum()

# %%
print("Duplicates in Geolocation dataset:", geolocation_df.duplicated().sum())

# %% [markdown]
# **Insight:**\
# Tidak ada _missing values_.\
# Terdapat **261831** baris duplikat, sekitar **26%** dari keseluruhan data.
# 

# %% [markdown]
# #### Menilai Tabel `customers_df`
# 

# %%
customers_df.info()

# %%
print("\nMissing values in Customers dataset:")
customers_df.isna().sum()

# %%
print("Duplicates in Customers dataset:", customers_df.duplicated().sum())

# %% [markdown]
# **Insight:**\
# Tidak ada anomali tipe data.\
# Tidak ada _missing values_.\
# Tidak ada baris yang duplikat.
# 

# %% [markdown]
# #### Menilai Tabel `sellers_df`
# 

# %%
sellers_df.info()

# %%
print("\nMissing values in Sellers dataset:")
sellers_df.isna().sum()

# %%
print("Duplicates in Sellers dataset:", sellers_df.duplicated().sum())

# %% [markdown]
# **Insight:**\
# Tidak ada anomali tipe data.\
# Tidak ada _missing values._\
# Tidak ada bairs yang duplikat.
# 

# %% [markdown]
# #### Menilai Tabel `orders_df`
# 

# %%
orders_df.info()

# %%
print("Duplicates in Orders dataset:", orders_df.duplicated().sum())

# %%
print("\nMissing values in Orders dataset:")
orders_df.isna().sum()

# %% [markdown]
# **Insight:**\
# Anomali pada kolom `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, dan `order_estimated_delivery_date` dengan tipe data _object_ (teks).\
# Tidak ada baris yang duplikat.\
# Nilai-nilai yang hilang pada dataset berkaitan dengan tahapan proses pesanan, yang bisa disebabkan oleh pesanan yang belum selesai atau pembatalan.\
# 

# %% [markdown]
# ### Cleaning Data
# 

# %% [markdown]
# #### Membersihkan Tabel `products_df`
# 

# %%
products_df.info()

# %% [markdown]
# **FIXING:** Missing Values
# 

# %%
print("\nMissing values in Products dataset:")
products_df.isna().sum()

# %%
missing_values = products_df[products_df.isna().any(axis=1)]
missing_values.head()

# %%
products_df.loc[:, "product_category_name"] = products_df[
    "product_category_name"
].fillna("unknown")

# %%
unknown_count = products_df[products_df["product_category_name"] == "unknown"].shape[0]
print(
    f"Number of rows with 'unknown' entries in 'product_category_name': {unknown_count}"
)

# %%
print("Product weight statistics:\n")
products_df["product_weight_g"].describe().round(2)

# %%
products_df.loc[
    products_df["product_weight_g"] == 0,
    ["product_id", "product_category_name", "product_weight_g"],
]

# %%
cama_mesa_banho_df = products_df[
    products_df["product_category_name"] == "cama_mesa_banho"
]

products_df.loc[
    (products_df["product_category_name"] == "cama_mesa_banho")
    & (products_df["product_weight_g"] == 0),
    "product_weight_g",
] = cama_mesa_banho_df["product_weight_g"].median()

# %%
print("Product weight statistics:\n")
products_df["product_weight_g"].describe().round(2)

# %%
products_df["product_name_lenght"] = products_df["product_name_lenght"].fillna(
    products_df["product_name_lenght"].mean().round(2)
)

products_df["product_description_lenght"] = products_df[
    "product_description_lenght"
].fillna(products_df["product_description_lenght"].mean().round(2))

products_df["product_photos_qty"] = products_df["product_photos_qty"].fillna(
    products_df["product_photos_qty"].mean().round(2)
)

# %%
print("\nMissing values in Products dataset:")
products_df.isna().sum()

# %%
missing_rows = products_df[
    products_df[
        [
            "product_weight_g",
            "product_name_lenght",
            "product_height_cm",
            "product_width_cm",
        ]
    ]
    .isna()
    .any(axis=1)
]

missing_rows

# %%
columns_to_fill = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

categories = ["bebes", "unknown"]

for category in categories:
    for column in columns_to_fill:
        products_df.loc[
            products_df["product_category_name"] == category, column
        ] = products_df[products_df["product_category_name"] == category][
            column
        ].fillna(
            products_df[products_df["product_category_name"] == category][column]
            .mean()
            .round(2)
        )

# %%
products_df.info()

# %% [markdown]
# **Insigth:**\
# _Missing values_ sebanyak **610** pada `product_category_name` berhasil diisi dengan nama kategori produk 'unknown' karena hilangnya informasi pada dataset.\
# _Missing values_ sebanyak **610** pada [`product_name_length`, `product_description_length`, `product_photos_qty`] berhasil diisi dengan nilai _mean_ dari masing-masing kolom mereka.
# 
# Nilai _NaN_ di kolom `product_weight_g`, `product_length_cm`, `product_height_cm`, dan `product_width_cm` untuk kategori 'bebes' dan 'unknown' telah diisi menggunakan rata-rata (mean) masing-masing kolom untuk setiap kategori. Pendekatan ini memastikan bahwa setiap kategori produk memiliki nilai yang lebih representatif dibanding menggunakan satu nilai median atau mean secara keseluruhan.
# 
# Rentang berat produk `product_weight_g` yang dimulai dari **0.00** hingga **40425** gram, menunjukkan adanya anomali dengan adanya berat produk sebesar **0.00** gram yang telah digantikan dengan nilai _median_.
# 

# %% [markdown]
# #### Membersihkan Tabel `order_reviews.df`
# 

# %%
order_reviews_df.info()

# %% [markdown]
# **FIXING:** Data Types
# 

# %%
order_reviews_df[["review_creation_date", "review_answer_timestamp"]].dtypes

# %%
order_reviews_df["review_creation_date"] = pd.to_datetime(
    order_reviews_df["review_creation_date"]
)
order_reviews_df["review_answer_timestamp"] = pd.to_datetime(
    order_reviews_df["review_answer_timestamp"]
)

order_reviews_df[["review_creation_date", "review_answer_timestamp"]].dtypes

# %% [markdown]
# **Insight:**\
# Kolom `review_creation_date` dan `review_answer_timestamp` telah dikonversi menjadi _datetime_.
# 

# %% [markdown]
# **FIXING:** Missing Values
# 

# %%
order_reviews_df.isna().sum()

# %%
order_reviews_df.loc[:, ["review_comment_title", "review_comment_message"]] = (
    order_reviews_df.loc[:, ["review_comment_title", "review_comment_message"]].fillna(
        "empty"
    )
)

empty_samples = order_reviews_df[
    (order_reviews_df["review_comment_title"] == "empty")
    | (order_reviews_df["review_comment_message"] == "empty")
]

empty_samples.sample(5)

# %%
empty_samples_title = order_reviews_df[
    order_reviews_df["review_comment_title"] == "empty"
]
empty_samples_message = order_reviews_df[
    order_reviews_df["review_comment_message"] == "empty"
]

print(
    f"'empty' values in review_comment_title or review_comment_message: {empty_samples_title.shape[0]}"
)
print(f"'empty' values in review_comment_message: {empty_samples_message.shape[0]}")

# %%
order_reviews_df.isna().sum()

# %% [markdown]
# **Insight:**\
# _Missing values_ pada kolom `review_comment_title` dan `review_comment_message` telah diisi dengan 'empty' untuk mengisi kekosongan data.
# 

# %% [markdown]
# #### Membersihkan Tabel `order_items_df`
# 

# %% [markdown]
# **FIXING:** Data Types
# 

# %%
print(f"Data type [shipping_limit_date]: {order_items_df['shipping_limit_date'].dtype}")

# %%
order_items_df["shipping_limit_date"] = pd.to_datetime(
    order_items_df["shipping_limit_date"]
)

# %%
order_items_df.info()

# %% [markdown]
# **Insight:**\
# Kolom `shipping_limit_date` telah dikonversi ke tipe data _datetime_.\
# Kolom `freight_value` tetap menyertakan nilai **0.00** karena munkin saja merepresentasikan _free shipping_.
# 

# %% [markdown]
# #### Membersihkan Tabel `geolocation_df`
# 

# %%
print("Duplicates in Geolocation dataset:", geolocation_df.duplicated().sum())

# %% [markdown]
# **FIXING:** Duplicates
# 

# %%
geolocation_df = geolocation_df.drop_duplicates()
remaining_duplicates_count = geolocation_df.duplicated().sum()

# %%
print("Remaining duplicates in Geolocation dataset:", remaining_duplicates_count)

# %%
geolocation_df.info()

# %% [markdown]
# **Insight:**\
# Sebanyak **261831** baris duplikat telah dihapus.
# 

# %% [markdown]
# #### Membersihkan Tabel `orders_df`
# 

# %% [markdown]
# **FIXING:** Data Types
# 

# %%
columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in columns:
    print(f"{col:<35} {orders_df[col].dtypes}")

# %%
for col in columns:
    orders_df[col] = pd.to_datetime(orders_df[col], errors="coerce")
    print(f"{col:<35} {orders_df[col].dtypes}")

# %% [markdown]
# **Insight:**\
# Kolom `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, dan `order_estimated_delivery_date` telah berhasil dikonversi menjadi tipe data _datetime_.
# 

# %% [markdown]
# **FIXING:** Missing Values
# 

# %%
print("\nMissing values in Orders dataset:")
orders_df.isna().sum()

# %%
missing_approved_at = orders_df[orders_df["order_approved_at"].isna()]

missing_approved_delivered = missing_approved_at[
    missing_approved_at["order_status"] == "delivered"
]

print("\nSample rows with missing 'order_approved_at' and status 'delivered':")
missing_approved_delivered.sample(3)

# %%
orders_df["approval_time_diff"] = (
    orders_df["order_approved_at"] - orders_df["order_purchase_timestamp"]
).dt.total_seconds() / 3600
orders_df["approval_time_diff"] = orders_df["approval_time_diff"].round(2)

average_approval_time = orders_df["approval_time_diff"].mean()

orders_df["order_approved_at"] = orders_df["order_approved_at"].fillna(
    orders_df["order_purchase_timestamp"]
    + pd.to_timedelta(average_approval_time, unit="h")
)

orders_df["order_approved_at"] = orders_df["order_approved_at"].dt.round("s")

orders_df.sample(3)

# %%
print(
    "NaN values in 'approval_time_diff':", orders_df["approval_time_diff"].isna().sum()
)

# %%
average_approval_time = orders_df["approval_time_diff"].mean()
orders_df["approval_time_diff"] = orders_df["approval_time_diff"].fillna(
    average_approval_time
)
orders_df["approval_time_diff"] = orders_df["approval_time_diff"].round(2)

# %%
print(
    "NaN values in 'approval_time_diff':", orders_df["approval_time_diff"].isna().sum()
)

# %%
# orders_df = orders_df.dropna(subset=["order_delivered_carrier_date"])
# orders_df = orders_df.dropna(subset=["order_delivered_customer_date"])

# %%
print("\nMissing values in Orders dataset:")
orders_df.isna().sum()

# %%
orders_df.info()

# %% [markdown]
# **Insight:**\
# Terdapat beberapa `order_status` 'delivered' yang mempunyai nilai kosong pada `order_approved_at`.\
# Kolom `order_approved_at` yang memiliki nilai kosong telah diisi dengan menghitung rata-rata waktu persetujuan dari pesanan yang sudah memiliki nilai di `order_approved_at` (selisih waktu antara `order_purchase_timestamp` dan `order_approved_at`).\
# 
# _NaT_ pada kolom `order_delivered_carrier_date` dan `order_delivered_customer_date` tetap, karena disesuaikan dengan keadaan aktual dimana pesanan belum memasuki status pengiriman.
# 

# %% [markdown]
# ## Exploratory Data Analysis (EDA)
# 

# %% [markdown]
# ### Eksplorasi Data `orders_df`
# 

# %%
orders_df.head(3)

# %%
orders_df.info()

print(f"\n(rows, collumns): \t\t{orders_df.shape}")
print(f"nunique of order_id: \t\t{orders_df['order_id'].nunique()}")
print(f"nunique of customer_id: \t{orders_df['customer_id'].nunique()}")
print(f"nunique of order_status: \t{orders_df['order_status'].nunique()}")

# %%
status_counts = orders_df["order_status"].value_counts()
total_orders = status_counts.sum()

status_percentages = (status_counts / total_orders) * 100

pd.DataFrame(
    {
        "Count": status_counts.values,
        "Percentage": status_percentages.round(2).map("{:.2f}%".format),
    }
)

# %%
stats = orders_df["approval_time_diff"].describe().round(2)

pd.DataFrame({"Statistic": stats.index, "Value": stats.values})

# %%
delivered_status_df = orders_df[orders_df["order_status"] == "delivered"].sort_values(
    "approval_time_diff", ascending=False
)

delivered_status_df[["order_id", "order_status", "approval_time_diff"]]

# %%
canceled_status_df = orders_df[orders_df["order_status"] == "canceled"].sort_values(
    "approval_time_diff", ascending=False
)

canceled_status_df[["order_id", "order_status", "approval_time_diff"]]

# %% [markdown]
# **Insight:**
# 
# - Sebanyak 97% pesanan memiliki status "delivered", menunjukkan bahwa sistem pengiriman berjalan dengan baik dan memiliki tingkat keberhasilan yang tinggi.
# - Persentase pembatalan hanya sebesar 0,63%, yang menunjukkan bahwa jumlah pesanan yang dibatalkan sangat rendah dibandingkan total pesanan.
# - Rata-rata waktu persetujuan adalah 10,42 jam, dengan variasi yang cukup besar.
# 

# %% [markdown]
# ### Eksplorasi Data `order_reviews_df`
# 

# %%
order_reviews_df.sample(5).T

# %%
order_reviews_df.describe(include="all").T

# %%
review_counts = order_reviews_df["review_score"].value_counts().sort_index()
total_reviews = review_counts.sum()

pd.DataFrame(
    {
        "Score Count": review_counts.values,
        "Percentage": (review_counts / total_reviews * 100)
        .round(2)
        .map("{:.2f}%".format),
    }
)

# %% [markdown]
# **Insight:**\
# Berdasarkan distribusi Review Score pada e-commerce, mayoritas ulasan menunjukkan kepuasan tinggi dengan skor **5** yang memiliki kontribusi sebesar **57.78%** dari total ulasan. Diikuti oleh skor **4** yang memberikan kontribusi sebesar **19.29%**.
# 

# %% [markdown]
# ### Merge Data `orders_df` dan `order_reviews_df`
# 

# %%
order_orders_reviews_df = pd.merge(
    orders_df,
    order_reviews_df,
    on="order_id",
    how="inner",
)

order_orders_reviews_df["review_score"] = order_orders_reviews_df[
    "review_score"
].astype("Int64")

# %%
order_orders_reviews_df.sample(5).T

# %%
canceled_status_df = order_orders_reviews_df[
    (order_orders_reviews_df["order_status"] == "canceled")
]
canceled_status_df.head().T

# %%
canceled_reviews_df = order_orders_reviews_df[
    (order_orders_reviews_df["order_status"] == "canceled")
    & (order_orders_reviews_df["review_comment_message"] != "empty")
]

colls_df = canceled_reviews_df[
    [
        "order_id",
        "order_status",
        "customer_id",
        "review_id",
        "review_score",
        "review_comment_message",
    ]
].sample(5)

colls_df.T

# %%
canceled_reviews_translated_df = canceled_reviews_df.copy()

canceled_reviews_translated_df[
    "review_comment_message"
] = canceled_reviews_translated_df["review_comment_message"].apply(
    lambda x: (Translator(source="pt", target="en").translate(x) if pd.notna(x) else "")
)

translated_df = canceled_reviews_translated_df[
    [
        "order_id",
        "order_status",
        "customer_id",
        "review_id",
        "review_score",
        "review_comment_message",
    ]
]

pd.set_option("display.max_colwidth", None)

translated_df.head().T

# %% [markdown]
# ### Eksplorasi Data `order_items_df`
# 

# %%
print(order_items_df.info())

print(f"\nnunique of order_id: \t\t{order_items_df['order_id'].nunique()}")
print(f"nunique of product_id: \t\t{order_items_df['product_id'].nunique()}")
print(f"nunique of seller_id: \t\t{order_items_df['seller_id'].nunique()}")

# %%
merged_items_reviews_df = pd.merge(
    order_reviews_df, order_items_df, on="order_id", how="left"
)

selected_colls = merged_items_reviews_df[
    [
        "order_id",
        "review_id",
        "review_score",
        "order_item_id",
        "seller_id",
        "product_id",
    ]
]

multi_item_orders = selected_colls.groupby("order_id").filter(
    lambda x: x["product_id"].nunique() > 1
)

multi_item_orders.head(6)

# %% [markdown]
# **Insight:**
# 
# 1. `multi_item_order`:
#    - `order_id` <span style="color:orange">b18dcdf73be66366873cd26c5724d1dc</span> memiliki beberapa item yang berbeda (`order_item_id` 1, 2, 3, dan 4). Semua item ini terkait dengan satu ulasan (berdasarkan `review_id`), dan pelanggan memberikan skor **1** untuk keseluruhan pesanan.
#    - `order_id` <span style="color:orange">d7bd0e4afdf94846eb73642b4e3e75c3</span> juga memuat lebih dari satu item, dan pelanggan memberikan skor **3**.
# 2. Ini memberikan gambaran jelas bahwa dalam beberapa kasus, satu `order_id` memang dapat berisi beberapa produk (berdasarkan `product_id`). Namun, ulasan diberikan satu kali untuk pesanan tersebut (berdasarkan `order_id` dan `review_id`), meskipun pesanan tersebut terdiri dari beberapa produk (berdasarkan `order_item_id`).
# 

# %% [markdown]
# ### Eksplorasi Data `products_df`
# 

# %%
products_df.info()

print(f"\n(rows, collumns): \t\t\t{products_df.shape}")
print(f"nunique of product_id: \t\t\t{products_df['product_id'].nunique()}")
print(
    f"nunique of product_category_name: \t{products_df['product_category_name'].nunique()}"
)

# %%
products_df[["product_id", "product_category_name"]].head()

# %% [markdown]
# **Menerjemahkan `product_category_name`**
# 

# %%
category_translation = product_category_translation_df.set_index(
    "product_category_name"
)["product_category_name_english"]

products_df["product_category_name"] = (
    products_df["product_category_name"]
    .map(category_translation)
    .fillna(products_df["product_category_name"])
)

products_df[["product_id", "product_category_name"]].head()

# %%
products_df

# %%
category_counts = products_df["product_category_name"].value_counts()
total_categories = len(category_counts)

percentages = (category_counts.head() / category_counts.head().sum() * 100).map(
    "{:.2f}%".format
)

pd.DataFrame(
    {"Product Count": category_counts.head().values, "Percentage": percentages}
)

# %%
category_counts = products_df["product_category_name"].value_counts()
total_categories = len(category_counts)

rarest_categories = category_counts.tail().sort_values()

percentages = (rarest_categories / category_counts.sum() * 100).map("{:.3f}%".format)

pd.DataFrame(
    {
        "Product Count": rarest_categories.values,
        "Percentage": percentages,
    }
)

# %%
unknown_type = products_df[products_df["product_category_name"] == "unknown"]
print(f"Number of products with 'unknown' category: {unknown_type.shape[0]} \n")

unknown_type[["product_id", "product_category_name"]].head()

# %%
products_df.describe().round(2)

# %% [markdown]
# **Insight:**
# 
# 1. Banyak jenis produk berdasarkan kategori produk:
#    - Kategori produk yang memiliki **varian produk terbanyak** adalah `bed_bath_table`.
#    - Kategori produk yang memiliki **varian produk paling sedikit** adalah `cds_dvds_musicals`.
# 2. `product_name_lenght`
#    - Panjang nama produk bervariasi antara **5** hingga **76** karakter dengan rata-rata panjang sebesar **48.48** karakter.
#    - Hal ini menunjukkan bahwa rata-rata nama produk relatif singkat dan deskriptif.
# 3. `product_description_lenght`
#    - Panjang deskripsi produk berkisar dari **4** hingga **3992** karakter, dengan rata-rata deskripsi sebesar **771.5** karakter.
#    - Ini menunjukkan bahwa sebagian besar produk memiliki deskripsi yang cukup detail, namun ada beberapa produk dengan deskripsi yang sangat singkat.
# 4. `product_photos_qty`
#    - Setiap produk memiliki antara **1** hingga **20** foto, dengan rata-rata jumlah foto sebesar **2.19**.
#    - Ini menunjukkan bahwa sebagian besar produk didokumentasikan dengan baik menggunakan setidaknya satu foto, namun ada juga yang memiliki lebih banyak foto untuk mendukung promosi produk.
# 

# %% [markdown]
# ### Merge Data `order_items_df` dan `products_df`
# 

# %%
order_items_products_df = pd.merge(
    order_items_df, products_df, on="product_id", how="inner"
)

order_items_products_df.info()

# %%
order_items_products_df.head()

# %% [markdown]
# ### Merge Data `order_items_products_df` dan `orders_order_reviews_df`
# 

# %%
oor_oip_df = pd.merge(
    order_items_products_df,
    order_orders_reviews_df,
    on="order_id",
    how="left",
)

oor_oip_df.info()

# %% [markdown]
# ### Eksplorasi Data `order_payments_df`
# 

# %%
order_payments_df.info()

print(f"\n(rows, collumns): \t\t\t{order_payments_df.shape}")
print(f"nunique of order_id: \t\t\t{order_payments_df['order_id'].nunique()}")
print(f"nunique of payment_type: \t\t{order_payments_df['payment_type'].nunique()}")

# %%
duplicated_order_id = order_payments_df[
    order_payments_df.duplicated("order_id", keep=False)
]
duplicated_order_id.sort_values(by="order_id", ascending=False).head(4)

# %%
order_payments_df.describe().round(2)

# %%
order_payments_summary = (
    order_payments_df.groupby("order_id")
    .agg({"payment_type": lambda x: ", ".join(x), "payment_value": "sum"})
    .reset_index()
    .sort_values(by="payment_value", ascending=False)
)

order_payments_summary

# %% [markdown]
# **Insight:**
# 
# 1. Nunique of `order_id`:
#    - Dataset ini mencakup **103886** entri, dengan **99440** pesanan unik.
#    - Ini menunjukkan bahwa beberapa pesanan memiliki lebih dari satu pembayaran, juga menunjukkan pesanan dibayar dengan beberapa metode atau cicilan.
# 2. Berdasarkan nilai quartil `payment_installments`, sebagian besar pelanggan melakukan pembayaran dalam **1** hingga **4** cicilan
# 3. Nilai pembayaran tertinggi berdasarkan `order_id` adalah pembayaran dengan `credit_card` yaitu senilai **13.664,08**.
# 

# %% [markdown]
# ### Eksplorasi Data `all_df`
# 

# %%
all_df = pd.merge(oor_oip_df, order_payments_summary, on="order_id", how="left")
all_df.head()

# %%
all_df.info()

# %%
all_df.describe().round(2).T

# %%
price_sorted_df = (
    all_df[
        [
            "order_id",
            "order_item_id",
            "product_id",
            "product_category_name",
            "price",
        ]
    ]
    .sort_values(by=["price", "order_item_id"], ascending=False)
    .head()
)
price_sorted_df

# %%
payment_val_sorted_df = (
    all_df.loc[all_df.groupby("order_id")["order_item_id"].idxmax()][
        [
            "order_id",
            "order_item_id",
            "product_id",
            "product_category_name",
            "price",
            "freight_value",
            "payment_value",
        ]
    ]
    .sort_values(by=["payment_value", "order_item_id"], ascending=False)
    .head()
)
payment_val_sorted_df

# %%
category_revenue_df = (
    all_df.groupby("product_category_name")
    .agg(
        total_payment_value=("payment_value", "sum"),
        order_count=("order_id", "nunique"),
        order_item_count=("order_item_id", "count"),
    )
    .reset_index()
)

category_revenue_sorted = category_revenue_df.sort_values(
    by="total_payment_value", ascending=False
)

category_revenue_sorted

# %%
all_df["payment_type"] = (
    all_df["payment_type"]
    .fillna("")
    .apply(lambda x: x.split(", ")[0] if "," in x else x)
)

payment_counts = all_df["payment_type"].value_counts()
total_payments = payment_counts.sum()
payment_percentages = (payment_counts / total_payments) * 100

clean_payment_df = pd.DataFrame(
    {
        "Count": payment_counts.values,
        "Percentage": payment_percentages.map("{:.1f}%".format),
    },
    index=payment_counts.index,
)

clean_payment_df

# %%
all_df.to_csv("e-commerce_public_dataset/all_df_cleaned.csv", index=False)

# %% [markdown]
# **Insight:**\
# Nilai harga produk (`price`) tertinggi adalah produk dari kategori `housewares` yakni sebesar **6735.0**.\
# Sementara itu, nilai pembayaran (`payment_value`) tertinggi berasal dari produk dengan kategori `fixed_telephony` sebesar **13664.08**.
# 
# Berdasarkan kategori produk, kategori dengan revenue tertinggi adalah `bed_bath_table` dengan total revenue sebesar **1725465.67**
# 
# Metode pembayaran `credit_card` menjadi yang paling dominan digunakan oleh pembeli, mencakup **75.6%** dari seluruh transaksi.\
# Sedangkan, transaksi dengan `debit_card` menjadi meotode pembayaran yang paling jarang digunakan, hanya **1.5%** dari seluruh transaksi.
# 

# %% [markdown]
# ## Visualization & Explanatory Analysis
# 

# %% [markdown]
# ### Kategori produk apa saja yang paling laris?
# 

# %%
total_orders = len(order_items_products_df["order_id"].unique())

category_orders = (
    order_items_products_df.groupby("product_category_name")
    .agg({"order_id": "nunique"})
    .reset_index()
)

category_orders.columns = ["product_name", "num_orders"]

category_orders["percentage"] = (
    category_orders["num_orders"] / total_orders * 100
).round(2)

category_orders_sorted = category_orders.sort_values("percentage", ascending=False)

top_5_categories = category_orders_sorted.head()

print("Top 5 selling product categories:")
print(top_5_categories.to_string(index=False))

plt.figure(figsize=(10, 6))
bars = plt.bar(top_5_categories["product_name"], top_5_categories["percentage"])

for bar in bars[1:]:
    bar.set_color("lightgray")

plt.title("Top 5 Selling Product Categories", fontsize=14, pad=20)
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Percentage (%)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

for i, v in enumerate(top_5_categories["percentage"]):
    plt.text(i, v, f"{v}%", ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.show()

# %% [markdown]
# **Insight:**
# 
# - Kategori **bed_bath_table** memimpin penjualan dengan **9,54%** dari total pesanan.
# - **Lima kategori teratas menyumbang hampir 40%** dari total pesanan.
# - **Perbedaan persentase** antara kategori teratas dan terbawah dalam daftar ini **sekitar 3%**.
# 

# %% [markdown]
# ### Apa faktor utama yang menyebabkan pembatalan pesanan?
# 

# %%
status_df = all_df["order_status"].value_counts().reset_index()
status_df.columns = ["Order Status", "Count"]

colors = [
    "#6EACC9",
    "#4986A7",
    "#105D8A",
    "#0F4C75",
    "#1B4965",
    "#2B5F82",
    "#133E62",
    "#083358",
    "#0A2647",
    "#001B48",
]

plt.figure(figsize=(10, 8))
plt.pie(status_df["Count"], labels=None, colors=colors, startangle=90)
plt.title("Order Status Distribution", fontsize=14, pad=20, weight="bold")

legend = plt.legend(
    status_df.index,
    title="Order Statuses",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)
legend.get_frame().set_alpha(0)

plt.axis("equal")

plt.tight_layout()
plt.show()

print(status_df)

# %%
translations = {
    "portateis_cozinha_e_preparadores_de_alimentos": "kitchen_appliances",
}

canceled_by_category = (
    all_df[all_df["order_status"] == "canceled"].groupby("product_category_name").size()
)
total_by_category = all_df.groupby("product_category_name").size()
cancellation_rate = (
    (canceled_by_category / total_by_category * 100)
    .sort_values(ascending=False)
    .head(5)
)

cancellation_rate.index = cancellation_rate.index.map(lambda x: translations.get(x, x))

plt.figure(figsize=(10, 6))
bars = cancellation_rate.plot(kind="bar", width=0.8, color="lightgray")
ax = plt.gca()

plt.title(
    "Top 5 Product Categories with Highest Cancellation Rates", fontsize=14, pad=20
)
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Cancellation Rate (%)", fontsize=12)
plt.xticks(rotation=45, ha="right")

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.gca().set_axisbelow(True)

highest_bar = bars.patches[0]
highest_bar.set_color("#1f77b4")

for i, v in enumerate(cancellation_rate):
    ax.text(i, v, f"{v:.2f}%", ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.show()

# %%
canceled_payment_methods = all_df[all_df["order_status"] == "canceled"][
    "payment_type"
].value_counts()

plt.figure(figsize=(12, 8))


colors = [
    "#6EACC9",
    "#4986A7",
    "#105D8A",
    "#0F4C75",
]

patches, texts, autotexts = plt.pie(
    canceled_payment_methods,
    labels=[""] * len(canceled_payment_methods),
    colors=colors,
    autopct="%1.1f%%",
    pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor="white", linewidth=1),
)

plt.setp(autotexts, size=9, weight="bold", color="white")

legend = plt.legend(
    patches,
    canceled_payment_methods.index,
    title="Payment Methods",
    loc="center left",
    bbox_to_anchor=(0.45, 0.5),
    fontsize=10,
)
legend.get_frame().set_alpha(0.0)
legend.get_frame().set_facecolor("none")

plt.title(
    "Distribution of Payment Methods\nfor Canceled Orders",
    pad=5,
    size=14,
    weight="bold",
)

plt.axis("equal")

plt.tight_layout()

plt.show()

# %%
translated_df_copy = translated_df.copy()


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


translated_df_copy.loc[:, "cleaned_review"] = (
    translated_df_copy.loc[:, "review_comment_message"]
    .fillna("")
    .apply(preprocess_text)
)

word_freq = Counter(" ".join(translated_df_copy["cleaned_review"]).split())


def categorize_review(text):
    categories = {
        "Shipping Issue": [
            "ship",
            "delay",
            "send",
            "courier",
            "package",
            "deliver",
            "arrive",
            "receive",
            "expedition",
            "transport",
            "wait",
            "late",
            "come",
            "came",
            "slow",
        ],
        "Product Quality Issue": [
            "quality",
            "broken",
            "damaged",
            "defect",
            "different",
            "not working",
            "fake",
            "destroyed",
            "not functioning",
            "poor",
            "does not match",
            "like",
        ],
        "Customer Service Issue": [
            "service",
            "trust",
            "reliable",
            "invoice",
            "call",
            "error",
            "solve",
            "contact",
            "seller",
            "response",
            "customer",
            "ignore",
            "answer",
            "help",
            "support",
            "notified",
        ],
        "Stock Issue": [
            "stock",
            "unavailable",
            "empty",
            "not available",
        ],
        "App/Website Issue": [
            "app",
            "website",
            "error",
            "bug",
            "crash",
            "glitch",
        ],
        "Return/Refund Issue": [
            "return",
            "refund",
            "exchange",
            "replace",
            "money back",
            "send back",
            "exchange",
            "compensation",
        ],
        "Seller Cancellation": [
            "cancel",
            "void",
        ],
        "Positive Comment": [
            "good",
            "satisfied",
            "happy",
            "great",
            "awesome",
            "excellent",
            "ok",
            "nice",
            "wonderful",
            "amazing",
            "love",
            "easy",
            "delight",
        ],
    }

    for category, keywords in categories.items():
        if any(word in text for word in keywords):
            return category
    return "Other"


translated_df_copy.loc[:, "Category"] = translated_df_copy.loc[
    :, "cleaned_review"
].apply(categorize_review)

category_counts = Counter(translated_df_copy["Category"])
sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

total_reviews = sum(category_counts.values())

for category, count in sorted_categories:
    percentage = (count / total_reviews) * 100

# %%
df = pd.DataFrame(sorted_categories, columns=["Category", "Count"])
df["Percentage"] = df["Count"] / total_reviews * 100

plt.figure(figsize=(12, 8))

colors = [
    "#6EACC9",
    "#4986A7",
    "#105D8A",
    "#0F4C75",
    "#1B4965",
    "#2B5F82",
    "#133E62",
    "#083358",
    "#0A2647",
    "#001B48",
]

patches, texts, autotexts = plt.pie(
    df["Percentage"],
    labels=[""] * len(df),
    colors=colors,
    autopct=lambda pct: f"{pct:.1f}%" if pct > 1 else "",
    startangle=90,
    pctdistance=0.9,
    wedgeprops={"linewidth": 0.7, "edgecolor": "white"},
)

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(8)
    autotext.set_weight("bold")

legend = plt.legend(
    patches,
    df["Category"],
    title="Review Categories",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=9,
)
legend.get_frame().set_alpha(0.0)
legend.get_frame().set_facecolor("none")

plt.title(
    "Distribution of Canceled Order\nReview Categories", pad=20, size=14, weight="bold"
)

plt.tight_layout()

plt.show()

# %%
def create_wordcloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()


shipping_keywords = " ".join(
    [
        # "ship",
        "delay",
        "send",
        "courier",
        "package",
        "deliver",
        "arrive",
        "receive",
        "expedition",
        "transport",
        "wait",
        "late",
        "come",
        "came",
        "slow",
    ]
)

create_wordcloud(shipping_keywords, "Shipping Issue Keywords")

# %% [markdown]
# **Insight:**
# 
# - Kategori produk teknologi tinggi seperti "PC Gamer" memimpin dalam tingkat pembatalan, mencapai **11.11%**, diikuti oleh "alat masak" dan "peralatan audio/video".
# - Produk-produk dengan **spesifikasi teknis yang kompleks** atau **harga tinggi** cenderung lebih rentan terhadap pembatalan.
# - Dari sisi pembayaran, "kartu kredit" mendominasi metode yang digunakan dalam pesanan yang dibatalkan, mencakup **77.7%** dari total. Hal ini bisa saja mencerminkan **kemudahan pembatalan** dan **kecenderungan pembelian impulsif** dengan kartu kredit.
# - Faktor yang paling signifikan dalam pembatalan pesanan adalah **masalah pengiriman**, yang menyumbang **72.17%** dari alasan pembatalan berdasarkan ulasan pelanggan. Diikuti oleh **masalah layanan pelanggan (8.62%)** dan **kualitas produk (3.45%)**.
# - Kata paling sering yang muncul dalam masalah pengiriman adalah **"delay"**, yang menunjukkan bahwa masalah pengiriman disebabkan oleh **keterlambatan**.
# 

# %% [markdown]
# ### Bagaimana pengaruh interval pengiriman terhadap tingkat kepuasan pelanggan?
# 

# %%
prepared_df = order_orders_reviews_df.copy()

prepared_df["delivery_time"] = (
    pd.to_datetime(prepared_df["order_delivered_customer_date"])
    - pd.to_datetime(prepared_df["order_purchase_timestamp"])
).dt.total_seconds() / (24 * 3600)

prepared_df = prepared_df[prepared_df["delivery_time"] >= 0]

prepared_df["delivery_interval"] = pd.cut(
    prepared_df["delivery_time"],
    bins=[0, 1, 2, 3, 5, 7, 10, 15, 30, 60, np.inf],
    labels=[
        "0-1",
        "1-2",
        "2-3",
        "3-5",
        "5-7",
        "7-10",
        "10-15",
        "15-30",
        "30-60",
        "60+",
    ],
)

# %%
plt.figure(figsize=(12, 6))

data_matrix = prepared_df.pivot_table(
    index="delivery_interval",
    columns="review_score",
    aggfunc="size",
    fill_value=0,
    observed=False,
)
sns.heatmap(
    data_matrix,
    cmap=sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True),
    annot=True,
    fmt="d",
    cbar_kws={"label": "Count"},
)

plt.title("Review Score Distribution by Delivery Time Interval", fontsize=14, pad=20)
plt.xlabel("Review Score", fontsize=12)
plt.ylabel("Delivery Time Interval (days)", fontsize=12, labelpad=10)

plt.tight_layout()
plt.show()

# %%
category_order = sorted(prepared_df["delivery_interval"].unique())

if not isinstance(prepared_df["delivery_interval"].dtype, pd.CategoricalDtype):
    prepared_df["delivery_interval"] = pd.Categorical(
        prepared_df["delivery_interval"], categories=category_order, ordered=True
    )

avg_scores = (
    prepared_df.groupby("delivery_interval", observed=False)["review_score"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.plot(avg_scores["delivery_interval"], avg_scores["review_score"], marker="o")
plt.title("Average Review Score Trend by Delivery Time Interval", fontsize=14, pad=20)
plt.xlabel("Delivery Time Interval (days)", fontsize=12)
plt.ylabel("Average Review Score", fontsize=12)
plt.ylim(1, 5)

plt.grid(
    visible=True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.5
)
plt.yticks([1, 2, 3, 4, 5])
plt.minorticks_on()

for i, row in avg_scores.iterrows():
    plt.text(
        row["delivery_interval"],
        row["review_score"] + 0.05,
        f"{row['review_score']:.2f}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

plt.tight_layout()

plt.show()

# %% [markdown]
# **Insight:**
# 
# - **Kecepatan pengiriman** memiliki **dampak signifikan** terhadap **kepuasan pelanggan**.
#   - **Pengiriman yang lebih cepat** cenderung menghasilkan **ulasan yang lebih positif**.
#   - **Skor ulasan rata-rata tertinggi (4,50)** dicapai untuk **pengiriman yang diselesaikan dalam 1-2 hari**.
# - Terdapat **penurunan bertahap** dalam **skor ulasan seiring** bertambahnya **waktu pengiriman**.
#   - Penurunan drastis terlihat untuk pengiriman yang memakan waktu lebih dari 15 hari.
# - **Pengiriman yang sangat lama (30-60 dan 60+ hari)** menerima **skor ulasan terendah**.
#   - Skor rata-rata hanya **2,26** untuk pengiriman **30-60 hari**.
#   - Skor rata-rata bahkan lebih rendah, yaitu **2,14**, untuk pengiriman yang memakan waktu **lebih dari 60 hari**.
# 

# %% [markdown]
# ### Bagaimana performa berbagai kategori produk dalam hal kepuasan pelanggan?
# 

# %%
category_reviews_df = (
    all_df.groupby("product_category_name")
    .agg(
        {
            "order_id": "nunique",
            "review_id": "count",
            "review_score": "mean",
        }
    )
    .rename(
        columns={
            "order_id": "Order Count",
            "review_id": "Review Count",
            "review_score": "Average Rating",
        }
    )
    .sort_values("Review Count", ascending=False)
)

total_reviews = category_reviews_df["Review Count"].sum()
category_reviews_df["Percentage"] = (
    category_reviews_df["Review Count"] / total_reviews * 100
).map("{:.2f}%".format)
category_reviews_df["Average Rating"] = category_reviews_df["Average Rating"].round(2)

category_reviews_df

# %% [markdown]
# Dalam menentukan **Best Seller** berdasarkan 5 produk terlaris dapat menggunakan pendekatan **_Bayesian Average Rating_**. Metode ini memanfaatkan rumus Bayes untuk mengkalkulasi peringkat yang lebih berimbang. Penghitungannya mempertimbangkan beberapa faktor daiantaranya banyaknya ulasan per produk, nilai rata-rata tiap produk, serta rata-rata penilaian secara menyeluruh.\
# Metode ini memberikan penilaian yang lebih tepat, terutama untuk produk-produk dengan jumlah ulasan yang relatif sedikit. Dengan demikian, mendapatkan gambaran yang lebih akurat tentang kualitas dan popularitas produk, tanpa terlalu dipengaruhi oleh perbedaan jumlah ulasan antar produk.
# 
# $$
# \text{Bayesian Average Rating} = \frac{v \cdot R + m \cdot C}{v + m}
# $$
# 
# Dimana:\
# **_v_** = Jumlah ulasan untuk produk tersebut\
# **_R_** = Peringkat rata-rata produk\
# **_C_** = Peringkat rata-rata keseluruhan di semua produk\
# **_m_** = Jumlah minimum ulasan yang diperlukan agar produk dapat dipertimbangkan
# 

# %%
C = category_reviews_df["Average Rating"].mean()
m = category_reviews_df["Review Count"].quantile(0.75)

top_5_products = category_reviews_df.head(5).index.tolist()
bayesian_ratings = (
    (
        category_reviews_df.loc[top_5_products, "Review Count"]
        * category_reviews_df.loc[top_5_products, "Average Rating"]
        + m * C
    )
    / (category_reviews_df.loc[top_5_products, "Review Count"] + m)
).round(2)

pd.DataFrame(
    {
        "Order Count": category_reviews_df.loc[top_5_products, "Order Count"],
        "Review Count": category_reviews_df.loc[top_5_products, "Review Count"],
        "Average Rating": category_reviews_df.loc[top_5_products, "Average Rating"],
        "Bayesian Average Rating": bayesian_ratings,
    }
).sort_values(by="Bayesian Average Rating", ascending=False)

# %%
plt.figure(figsize=(12, 6))

colors = ["#CCCCCC"] * len(bayesian_ratings)
colors[0] = sns.color_palette()[0]

sns.barplot(
    x="Bayesian Average Rating",
    y="product_category_name",
    data=bayesian_ratings,
    palette=colors,
    hue="product_category_name",
)

plt.title(
    "Top 5 Best Seller Product Categories\nby Bayesian Average Rating",
    fontsize=16,
    pad=20,
)
plt.xlabel("Bayesian Average Rating", fontsize=12)
plt.ylabel("Product Category", fontsize=12)

for i, v in enumerate(bayesian_ratings["Bayesian Average Rating"]):
    plt.text(v, i, f" {v:.2f}", va="center", fontsize=10)

plt.tight_layout()
plt.show()

# %% [markdown]
# **Insight:**
# 
# - Kategori **health_beauty** memiliki performa terbaik dengan Bayesian Average Rating **4.12**, diikuti oleh **sports_leisure** dengan **4.10**.
# - Perbedaan rating antar kategori teratas relatif kecil (range 0.2), menunjukkan **konsistensi kualitas** di berbagai kategori produk populer.
# 

# %% [markdown]
# ### Bagaimana tren penjualan bulanan?
# 

# %%
all_df["order_date"] = pd.to_datetime(all_df["order_purchase_timestamp"])

all_df["year_month"] = all_df["order_date"].dt.to_period("M")

start_date = pd.Period("2016-10")
end_date = pd.Period("2018-08")
df_filtered = all_df[
    (all_df["year_month"] >= start_date) & (all_df["year_month"] <= end_date)
]

monthly_data = (
    df_filtered.groupby("year_month")
    .agg({"price": "sum", "order_id": "count"})
    .reset_index()
)

monthly_data["year_month"] = monthly_data["year_month"].astype(str)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

sns.lineplot(x="year_month", y="price", data=monthly_data, ax=ax1, marker="o")
ax1.set_title("Revenue Trend", fontsize=16, pad=20)
ax1.set_xlabel("Year-Month", fontsize=12, labelpad=10)
ax1.set_ylabel("Revenue", fontsize=12)
ax1.tick_params(axis="x", rotation=45)
ax1.grid(True, linestyle="--", alpha=0.7)

sns.lineplot(x="year_month", y="order_id", data=monthly_data, ax=ax2, marker="o")
ax2.set_title("Order Trend", fontsize=16, pad=20)
ax2.set_xlabel("Year-Month", fontsize=12, labelpad=10)
ax2.set_ylabel("Number of Orders", fontsize=12)
ax2.tick_params(axis="x", rotation=45)
ax2.grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()

plt.show()

top_months_revenue = monthly_data.nlargest(3, "price")
print("\nTop 3 months by revenue:")
print(top_months_revenue[["year_month", "price"]])

top_months_orders = monthly_data.nlargest(3, "order_id")
print("\nTop 3 months by number of orders:")
print(top_months_orders[["year_month", "order_id"]])

# %% [markdown]
# **Insight:**
# 
# - Terlihat **lonjakan tajam** pada bulan **November 2017** untuk kedua metrik. Ini menjadi bulan dengan performa tertinggi, baik dari segi **revenue (1,008,127.73)** maupun **jumlah pesanan (8,647)**.
# - **Lonjakan di bulan November 2017** sangat mungkin berkaitan dengan **event Black Friday**. Di Brasil, Black Friday biasanya **jatuh pada akhir November**, sama seperti di AS.
# - Setelah lonjakan November 2017, bisnis tampaknya mampu mempertahankan level penjualan yang lebih tinggi di bulan-bulan berikutnya dibandingkan periode sebelum November 2017.
# 

# %% [markdown]
# ## RFM Analysis
# 

# %%
end_date = pd.to_datetime(all_df["order_purchase_timestamp"]).max()

rfm = all_df.groupby("customer_id").agg(
    {
        "order_purchase_timestamp": lambda x: (end_date - pd.to_datetime(x.max())).days,
        "order_id": "count",
        "price": "sum",
    }
)

rfm.columns = ["Recency", "Frequency", "Monetary"]


def create_quartiles(series, labels):
    try:
        return pd.qcut(series, q=4, labels=labels, duplicates="drop")
    except ValueError:
        median = series.median()
        return pd.cut(
            series, bins=[-np.inf, median, np.inf], labels=[labels[0], labels[-1]]
        )


r_labels = range(4, 0, -1)
f_labels = range(1, 5)
m_labels = range(1, 5)

rfm["R"] = create_quartiles(rfm["Recency"], r_labels)
rfm["F"] = create_quartiles(rfm["Frequency"], f_labels)
rfm["M"] = create_quartiles(rfm["Monetary"], m_labels)

rfm["RFM_Score"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)

rfm_result = rfm

rfm_result.head(10)

# %%
rfm_result.describe()

# %%
rfm_result["RFM_Score"].value_counts()

# %%
def truncate_id(cust_id, max_length=10):
    return (
        str(cust_id)[:max_length] + "..."
        if len(str(cust_id)) > max_length
        else str(cust_id)
    )


recency_df = rfm_result.sort_values("Recency", ascending=False).head()
frequency_df = rfm_result.sort_values("Frequency", ascending=False).head()
monetary_df = rfm_result.sort_values("Monetary", ascending=False).head()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("Best Customers Based on RFM Parameters (customer_id)", fontsize=16)


def plot_bar(ax, df, column, title, ylabel):
    colors = ["#CCCCCC"] * len(df)
    colors[0] = sns.color_palette()[0]

    ax.bar(range(len(df)), df[column], color=colors)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([truncate_id(id) for id in df.index], rotation=45, ha="right")

    for i, v in enumerate(df[column]):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom")


plot_bar(ax1, recency_df, "Recency", "By Recency (days)", "Days since last purchase")
plot_bar(ax2, frequency_df, "Frequency", "By Frequency", "Number of Orders")
plot_bar(ax3, monetary_df, "Monetary", "By Monetary", "Total Spend")

plt.tight_layout()
plt.subplots_adjust(top=0.88, bottom=0.2)
plt.show()

# %% [markdown]
# #### Segmentasi pelanggan
# 

# %%
def rfm_segment(score):
    score = int(score)
    r, f, m = score // 100, (score % 100) // 10, score % 10

    if r >= 4 and f >= 1 and m >= 4:
        return "Top customers"
    elif r >= 3 and f >= 1 and m >= 3:
        return "High value customer"
    elif r >= 2 and f >= 1 and m >= 2:
        return "Medium value customer"
    elif r >= 2 and f >= 1 and m >= 1:
        return "Low value customers"
    else:
        return "Lost customers"


rfm_result["customer_segment"] = rfm_result["RFM_Score"].apply(rfm_segment)

print(rfm_result[["RFM_Score", "customer_segment"]].head(20))

# %%
customer_segment_df = rfm_result["customer_segment"].value_counts().reset_index()
customer_segment_df.columns = ["customer_segment", "customer_count"]
print(customer_segment_df)

# %%
customer_segment_df["customer_segment"] = pd.Categorical(
    customer_segment_df["customer_segment"],
    [
        "Lost customers",
        "Low value customers",
        "Medium value customer",
        "High value customer",
        "Top customers",
    ],
)

customer_segment_df = customer_segment_df.sort_values("customer_segment")

# %%
max_segment = customer_segment_df.loc[
    customer_segment_df["customer_count"].idxmax(), "customer_segment"
]

colors = [
    "#CCCCCC" if segment != max_segment else sns.color_palette()[0]
    for segment in customer_segment_df["customer_segment"]
]

plt.figure(figsize=(12, 6))
bar_plot = sns.barplot(
    x="customer_count",
    y="customer_segment",
    data=customer_segment_df,
    palette=colors,
    hue="customer_segment",
)

plt.title("Number of Customers for Each Segment", loc="center", fontsize=16, pad=20)
plt.ylabel("Customer Segment", fontsize=12)
plt.xlabel("Number of Customers", fontsize=12)
plt.tick_params(axis="both", which="major", labelsize=10)

for i, v in enumerate(customer_segment_df["customer_count"]):
    plt.text(v + 0.5, i, str(v), va="center")

plt.tight_layout()
plt.show()

# %%
total_customers = customer_segment_df["customer_count"].sum()
customer_segment_df["percentage"] = (
    customer_segment_df["customer_count"] / total_customers * 100
)

plt.figure(figsize=(12, 8))

sea_colors = [
    "#6EACC9",
    "#4986A7",
    "#105D8A",
    "#0F4C75",
    "#1B4965",
]

patches, texts, autotexts = plt.pie(
    customer_segment_df["percentage"],
    labels=[""] * len(customer_segment_df),
    colors=sea_colors[: len(customer_segment_df)],
    autopct="%1.1f%%",
    pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor="white", linewidth=0.7),
)

plt.setp(autotexts, size=9, weight="bold", color="white")

legend = plt.legend(
    patches,
    customer_segment_df["customer_segment"],
    title="Customer Segments",
    loc="center left",
    bbox_to_anchor=(0.35, 0.5),
    fontsize=10,
)
legend.get_frame().set_alpha(0.0)
legend.get_frame().set_facecolor("none")

plt.title("Distribution of Customer Segments", pad=5, size=14, weight="bold")

plt.tight_layout()

plt.show()

# %% [markdown]
# **Insight:**
# 
# - Recency:
#   - 5 pelanggan teratas memiliki rentang recency antara 699-728 hari sejak pembelian terakhir.
#   - Perbedaan recency antar pelanggan top 5 relatif kecil, hanya berkisar 29 hari.
#   - **Menunjukkan bahwa pelanggan-pelanggan ini belum melakukan pembelian dalam waktu yang cukup lama (sekitar 2 tahun).**
# - Frequency:
#   - **Pelanggan teratas melakukan 22 kali pembelian.**
#   - Frekuensi pembelian menurun secara bertahap dari 22 ke 15 untuk 5 pelanggan teratas.
#   - Perbedaan frekuensi pembelian cukup signifikan antara pelanggan teratas (22) dan kelima (15).
# - Monetary:
# 
#   - **Pelanggan teratas memiliki total belanja sebesar 13,440** (dalam satuan mata uang).
#   - **Terdapat penurunan yang cukup drastis antara pelanggan teratas (13,440) dengan pelanggan kedua (7,160)**.
#   - Nilai belanja menurun secara bertahap dari pelanggan kedua hingga kelima.
# 
# - Customer Segmentation:
#   - **Medium value customer** merupakan **segmen pelanggan terbesar** dengan **30,681 pelanggan (31.3% dari total pelanggan)**. Ini menunjukkan bahwa sebagian besar pelanggan memiliki nilai transaksi yang moderat.
#   - **Lost customers** adalah **segmen terbesar kedua** dengan **24,296 pelanggan (24.8%)**. Ini mengindikasikan bahwa hampir seperempat pelanggan telah berhenti melakukan transaksi.
#   - **Low value customers** terdiri dari **18,225 pelanggan (18.6%)**. Pelanggan ini berpotensi untuk ditingkatkan nilainya melalui program retensi atau promosi yang tepat.
#   - **Top customers** hanya mencakup **6.2% dari total pelanggan** dengan 6,090 pelanggan. Segmen ini sangat penting karena kontribusinya yang tinggi terhadap pendapatan, meskipun jumlahnya relatif kecil.
# 

# %% [markdown]
# ## Conclusion
# 

# %% [markdown]
# 1. Kategori produk apa saja yang paling laris?\
#    Kategori bed_bath_table menjadi yang paling laris, diikuti oleh produk-produk kesehatan dan kecantikan. Ini menunjukkan bahwa konsumen cenderung lebih banyak membeli produk-produk untuk kebutuhan rumah tangga dan perawatan diri.
# 
# 2. Apa faktor utama yang menyebabkan pembatalan pesanan?\
#    Faktor utama yang menyebabkan pembatalan pesanan adalah masalah pengiriman, yang mencakup 72.17% dari total alasan pembatalan. Keterlambatan pengiriman merupakan penyebab terbesar, dengan kata "delay" muncul paling sering dalam ulasan pelanggan. Selain itu, produk dengan spesifikasi teknis yang kompleks dan harga tinggi seperti "PC Gamer" juga lebih rentan dibatalkan, serta metode pembayaran dengan kartu kredit lebih sering digunakan dalam pesanan yang dibatalkan (77.7%), yang mungkin terkait dengan kemudahan pembatalan dan perilaku pembelian impulsif.
# 
# 3. Bagaimana pengaruh interval pengiriman terhadap tingkat kepuasan pelanggan?\
#    Kecepatan pengiriman memiliki dampak yang signifikan terhadap kepuasan pelanggan. Pengiriman cepat (1-2 hari) menghasilkan ulasan dengan skor rata-rata tertinggi 4.50, sementara pengiriman yang memakan waktu lebih lama menyebabkan penurunan skor secara bertahap. Pengiriman 30-60 hari hanya mendapat skor rata-rata 2.26, sedangkan pengiriman lebih dari 60 hari memperoleh skor lebih rendah lagi, yaitu 2.14. Ini menunjukkan bahwa pengiriman lambat memiliki korelasi kuat dengan ulasan negatif.
# 
# 4. Bagaimana performa berbagai kategori produk dalam hal kepuasan pelanggan?\
#    Kategori health_beauty mencatat performa terbaik dalam hal kepuasan pelanggan dengan Bayesian Average Rating 4.12, diikuti oleh sports_leisure dengan 4.10. Perbedaan antar kategori teratas cukup kecil, mencerminkan konsistensi kualitas di berbagai kategori produk populer.
# 
# 5. Bagaimana tren penjualan bulanan?\
#    Terdapat lonjakan signifikan dalam penjualan pada November 2017, baik dari sisi pendapatan (1,008,127.73 dalam mata uang Brazil) maupun jumlah pesanan (8,647), yang kemungkinan besar dipicu oleh event Black Friday. Setelah itu, level penjualan cenderung stabil dan lebih tinggi dibandingkan periode sebelum November 2017, menunjukkan dampak positif dari momentum Black Friday terhadap tren penjualan bisnis.
# 


