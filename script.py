# %% [markdown]
# # Proyek Analisis Data: E-Commerce Public Dataset
# 
# - **Nama:** Firdaus Arif Ramadhani
# - **Email:** firdausarief65@gmail.com
# - **ID Dicoding:** FIRDAUS ARIF RAMADHANI
# 

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis
# 

# %% [markdown]
# -
# 

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan
# 

# %%
import random
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from deep_translator import GoogleTranslator as Translator  # type: ignore

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
products_df = pd.read_csv("e-commerce_public_dataset/products_dataset.csv")
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
    "e-commerce_public_dataset/product_category_name_translation.csv"
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
order_reviews_df = pd.read_csv("e-commerce_public_dataset/order_reviews_dataset.csv")
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
order_payments_df = pd.read_csv("e-commerce_public_dataset/order_payments_dataset.csv")
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
order_items_df = pd.read_csv("e-commerce_public_dataset/order_items_dataset.csv")
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
geolocation_df = pd.read_csv("e-commerce_public_dataset/geolocation_dataset.csv")
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
customers_df = pd.read_csv("e-commerce_public_dataset/customers_dataset.csv")
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
sellers_df = pd.read_csv("e-commerce_public_dataset/sellers_dataset.csv")
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
orders_df = pd.read_csv("e-commerce_public_dataset/orders_dataset.csv")
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
# Fill missing values in 'product_category_name' with 'unknown'
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
# Product weight with value 0
products_df.loc[
    products_df["product_weight_g"] == 0,
    ["product_id", "product_category_name", "product_weight_g"],
]

# %%
cama_mesa_banho_df = products_df[
    products_df["product_category_name"] == "cama_mesa_banho"
]

# Replace the value 0 in the 'product_weight_g' column for the cama_mesa_banho cateogry
products_df.loc[
    (products_df["product_category_name"] == "cama_mesa_banho")
    & (products_df["product_weight_g"] == 0),
    "product_weight_g",
] = cama_mesa_banho_df["product_weight_g"].median()

# %%
print("Product weight statistics:\n")
products_df["product_weight_g"].describe().round(2)

# %%
# Fill missing values with their mean values
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

# Specify the category for which you want to fill the NaN value
categories = ["bebes", "unknown"]

# Process for each category
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
# Fill the NaN values in review_comment_title and review_comment_message with 'empty'
order_reviews_df.loc[:, ["review_comment_title", "review_comment_message"]] = (
    order_reviews_df.loc[:, ["review_comment_title", "review_comment_message"]].fillna(
        "empty"
    )
)

# Display sample data that contains 'empty'
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
# Drop duplicates
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

print(f"{'Column Name':<35} | {'Data Type':<15}")
print("-" * 55)

for col in columns:
    print(f"{col:<35} | {orders_df[col].dtypes}")

# %%
print(f"{'Column Name':<35} | {'Data Type':<15}")
print("-" * 55)

for col in columns:
    orders_df[col] = pd.to_datetime(orders_df[col], errors="coerce")
    print(f"{col:<35} | {orders_df[col].dtypes}")

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
# Calculate the time difference between 'order_purchase_timestamp' and 'order_approved_at' in hours
orders_df["approval_time_diff"] = (
    orders_df["order_approved_at"] - orders_df["order_purchase_timestamp"]
).dt.total_seconds() / 3600
orders_df["approval_time_diff"] = orders_df["approval_time_diff"].round(2)

# Calculate the average approval time
average_approval_time = orders_df["approval_time_diff"].mean()

# Fill missing values in 'order_approved_at' by adding the average approval time to 'order_purchase_timestamp'
orders_df["order_approved_at"] = orders_df["order_approved_at"].fillna(
    orders_df["order_purchase_timestamp"]
    + pd.to_timedelta(average_approval_time, unit="h")
)

# Round 'order_approved_at' to the nearest second
orders_df["order_approved_at"] = orders_df["order_approved_at"].dt.round("s")

orders_df.sample(3)

# %%
# Check nan value in 'approval_time_diff' column
print(
    "NaN values in 'approval_time_diff':", orders_df["approval_time_diff"].isna().sum()
)

# %%
# Fill missing values in 'approval_time_diff' with the calculated average
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
print("\nMissing values in Orders dataset:")
orders_df.isna().sum()

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

# %% [markdown]
# **Memahami Distribusi `approval_time_diff`**
# 

# %%
stats = orders_df["approval_time_diff"].describe().round(2)

pd.DataFrame({"Statistic": stats.index, "Value": stats.values})

# %%
delivered_status_df = orders_df[orders_df["order_status"] == "delivered"].sort_values(
    "approval_time_diff", ascending=False
)

delivered_status_df[["order_id", "order_status", "approval_time_diff"]]

# %%
bins = [
    -float("inf"),  # Less than or equal to 0
    0,  # 0 hours
    24,  # 1 day
    48,  # 2 days
    72,  # 3 days
    96,  # 4 days
    168,  # 7 days
    336,  # 14 days
    504,  # 21 days
    720,  # 30 days
    float("inf"),  # More than 30 days
]

labels = [
    "diff <= 0",
    "0 < diff <= 24",
    "24 < diff <= 48",
    "48 < diff <= 72",
    "72 < diff <= 96",
    "96 < diff <= 168",  # 4 < diff <= 7 days
    "168 < diff <= 336",  # 7 < diff <= 14 days
    "336 < diff <= 504",  # 14 < diff <= 21 days
    "504 < diff <= 720",  # 21 < diff <= 30 days
    "diff > 720",  # > 30 days
]

output_df = (
    delivered_status_df["approval_time_diff"]
    .pipe(pd.cut, bins=bins, labels=labels, right=True)
    .value_counts()
    .reindex(labels, fill_value=0)
    .to_frame(name="Count")
    .assign(
        Percentage=lambda df: (df["Count"] / df["Count"].sum() * 100)
        .round(3)
        .map("{:.3f}%".format)
    )
    .reset_index()
    .rename(columns={"index": "Time Range (hours)"})
)

print("\nDistribution of Delivered Orders by Approval Time")
print("-" * 70)
print(output_df.to_string(index=False))
print("-" * 70)
print(f"Total delivered orders: {output_df['Count'].sum()}")

# %%
canceled_status_df = orders_df[orders_df["order_status"] == "canceled"].sort_values(
    "approval_time_diff", ascending=False
)

canceled_status_df[["order_id", "order_status", "approval_time_diff"]]

# %%
output_df = (
    canceled_status_df["approval_time_diff"]
    .pipe(pd.cut, bins=bins, labels=labels, right=True)
    .value_counts()
    .reindex(labels, fill_value=0)
    .to_frame(name="Count")
    .assign(
        Percentage=lambda df: (df["Count"] / df["Count"].sum() * 100)
        .round(2)
        .map("{:.2f}%".format)
    )
    .reset_index()
    .rename(columns={"index": "Time Range"})
)

print("\nDistribution of Canceled Orders by Approval Time")
print("-" * 60)
print(output_df.to_string(index=False))
print("-" * 60)
print(f"Total canceled orders: {output_df['Count'].sum()}")

# %% [markdown]
# **Insight:**
# 
# 1. Rata-rata lama persetujuan pesanan adalah sekitar **10** jam.
# 1. **Pesanan yang dibatalkan cenderung disetujui lebih cepat**
#    - Berdasarkan `approval_time_diff`:
#      - `canceled`: **84.00%** disetujui dalam 24 jam pertama
#      - `delivered`: **81.25%** disetujui dalam 24 jam pertama
#    - Terindikasi bahwa **kecepatan persetujuan bukan faktor utama pembatalan pesanan oleh pelanggan.**
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
# ### Eksplorasi Data `orders_df` dan `order_reviews_df`
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
# Creates a dataframe that contains the canceled status
canceled_status_df = order_orders_reviews_df[
    (order_orders_reviews_df["order_status"] == "canceled")
]
canceled_status_df.head().T

# %%
# Creates a dataframe that only contains the canceled status with review message
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

# Translate the entire review column to English
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

# %%
# Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


translated_df.loc[:, "cleaned_review"] = (
    translated_df["review_comment_message"].fillna("").apply(preprocess_text)
)

# Frequency analysis of words in canceled reviews
word_freq = Counter(" ".join(translated_df["cleaned_review"]).split())

# print("Top 20 Frequent Words in Canceled Reviews:")
# print(word_freq.most_common(20))


# Manual categorization based on English keywords
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


# Categorize each review in `translated_df`
translated_df.loc[:, "Category"] = translated_df["cleaned_review"].apply(
    categorize_review
)

# Calculate the number of reviews per category and sort by count
category_counts = Counter(translated_df["Category"])
sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

# Calculate total number of reviews for percentage calculation
total_reviews = sum(category_counts.values())

print("\nCanceled Review Category Counts")
print("-" * 55)
print(f"{'Category':<25} | {'Count':>10} | {'Percentage':>12}")
print("-" * 55)
for category, count in sorted_categories:
    percentage = (count / total_reviews) * 100
    print(f"{category:<25} | {count:>10} | {percentage:>11.2f}%")
print("-" * 55)
print(f"Total Reviews: {total_reviews}")

# # Random review samples per category (show 5 random examples per category)
# print("\nRandom Samples of Reviews per Category (Sorted by Frequency):")
# for category, count in sorted_categories:
#     print(f"\nCategory: {category} (Total: {count})")
#     category_reviews = translated_df[translated_df["Category"] == category][
#         "review_comment_message"
#     ].tolist()
#     examples = random.sample(category_reviews, min(10, len(category_reviews)))

#     for i, example in enumerate(examples, 1):
#         print(f"{i}. {example}")

# # Keyword analysis per category
# print("\nTop 10 words per category (Sorted by Category Frequency):")
# for category, _ in sorted_categories:
#     category_text = " ".join(translated_df[translated_df["Category"] == category]["cleaned_review"])
#     category_word_freq = Counter(category_text.split())
#     print(f"\n{category}:")
#     print(category_word_freq.most_common(10))

# %% [markdown]
# **Insight:**\
# Alasan utama pembatalan pesanan dapat terlihat di sini, di mana sekitar **72% pembatalan terjadi karena masalah pengiriman**.\
# Di sisi lain, pembatalan yang diikuti dengan ulasan positif dan menunjukkan kepuasan pelanggan terhadap produk kemungkinan disebabkan oleh kesalahan manusia (human error) atau kesalahan sistem (system error).
# 

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
# ### Eksplorasi Data `order_items_products_df` dan `orders_order_reviews_df`
# 

# %%
oor_oip_df = pd.merge(
    order_items_products_df,
    order_orders_reviews_df,
    on="order_id",
    how="left",
)

oor_oip_df.info()

# %%
category_reviews_df = (
    oor_oip_df.groupby("product_category_name")
    .agg({"review_id": "count", "review_score": "mean"})
    .rename(columns={"review_id": "Review Count", "review_score": "Average Rating"})
    .sort_values("Review Count", ascending=False)
)

total_reviews = category_reviews_df["Review Count"].sum()
category_reviews_df["Percentage"] = (
    category_reviews_df["Review Count"] / total_reviews * 100
).map("{:.2f}%".format)
category_reviews_df["Average Rating"] = category_reviews_df["Average Rating"].round(2)

category_reviews_df

# %% [markdown]
# Dalam menentukan **Best Seller** berdasarkan 5 produk terlaris, kita bisa menerapkan pendekatan _Bayesian Average Rating_. Metode ini memanfaatkan rumus Bayes untuk mengkalkulasi peringkat yang lebih berimbang. Penghitungannya mempertimbangkan beberapa faktor: banyaknya ulasan per produk, nilai rata-rata tiap produk, serta rata-rata penilaian secara menyeluruh.\
# Keunggulan metode ini terletak pada kemampuannya memberikan penilaian yang lebih tepat, terutama untuk produk-produk dengan jumlah ulasan yang relatif sedikit. Dengan demikian, kita bisa mendapatkan gambaran yang lebih akurat tentang kualitas dan popularitas produk, tanpa terlalu dipengaruhi oleh perbedaan jumlah ulasan antar produk.
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
# Calculate the overall average rating (C)
C = category_reviews_df["Average Rating"].mean()

# Determine the minimum reviews threshold (m)
m = category_reviews_df["Review Count"].quantile(
    0.75
)  # Using the 75th percentile as the threshold

# Calculate the Bayesian value for each product
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
        # "product_category_name": top_5_products,
        # "Review Count": category_reviews_df.loc[top_5_products, "Review Count"],
        # "Average Rating": category_reviews_df.loc[top_5_products, "Average Rating"],
        # "Percentage": category_reviews_df.loc[top_5_products, "Percentage"],
        "Bayesian Average Rating": bayesian_ratings,
    }
).sort_values(by="Bayesian Average Rating", ascending=False)

# %% [markdown]
# **Insight:**\
# Kategori produk dengan **ulasan terbanyak** yakni `bed_bath_table` dengan **11.137** ulasan **(mendapat 9,91% dari total ulasan)**. Meskipun memiliki jumlah ulasan tertinggi, rata-rata ratingnya hanya **3,9**.\
# Kategori produk dengan **ulasan terendah** yakni `security_and_services` yang hanya mendapat **2** ulasan dengan rata-rata rating **2,5**.
# 
# Kategori produk `health_beauty` memiliki _Bayesian Average Rating_ tertinggi, yaitu **4,12**. Hal ini menunjukkan bahwa produk di kategori ini paling memuaskan dibandingkan kategori lainnya, meskipun jumlah ulasannya tidak paling tinggi.
# 

# %% [markdown]
# ### Eksplorasi Data `order_payments_df`
# 

# %%
order_payments_df.info()

print(f"\n(rows, collumns): \t\t\t{order_payments_df.shape}")
print(f"nunique of order_id: \t\t\t{order_payments_df['order_id'].nunique()}")
print(f"nunique of payment_type: \t\t{order_payments_df['payment_type'].nunique()}")

# %%
# Duplicate rows based on order_id
duplicated_order_id = order_payments_df[
    order_payments_df.duplicated("order_id", keep=False)
]
duplicated_order_id.sort_values(by="order_id", ascending=False).head(4)

# %%
order_payments_df.describe().round(2)

# %%
# Summarize order_payments_df into one row per order_id
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
all_df.describe().round(2).T

# %%
# Sorting by price
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
# Sorting by payment_value
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
# Group by product_category_name and calculate total payment_value
category_revenue_df = (
    all_df.groupby("product_category_name")
    .agg(
        total_payment_value=("payment_value", "sum"),
        order_count=("order_id", "nunique"),  # Count of unique orders in each category
        order_item_count=("order_item_id", "count"),  # Total number of items sold
    )
    .reset_index()
)

# Sort by total_payment_value in descending order
category_revenue_sorted = category_revenue_df.sort_values(
    by="total_payment_value", ascending=False
)

category_revenue_sorted

# %%
# Fixing duplicate values by taking a unique value
all_df["payment_type"] = (
    all_df["payment_type"]
    .fillna("")
    .apply(lambda x: x.split(", ")[0] if "," in x else x)
)

# Recalculate the counts and percentages of payment types
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
# ### Pertanyaan 1:
# 

# %%


# %% [markdown]
# ### Pertanyaan 2:
# 

# %%


# %% [markdown]
# **Insight:**
# 
# - xxx
# - xxx
# 

# %% [markdown]
# ## Analisis Lanjutan (Opsional)
# 

# %%


# %% [markdown]
# ## Conclusion
# 

# %% [markdown]
# - Conclution pertanyaan 1
# - Conclution pertanyaan 2
# 


