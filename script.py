import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# GOOGLE SHEETS AUTH
# -----------------------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Ecommerce_RealTime_Data").sheet1

# -----------------------------
# CONFIG
# -----------------------------
num_rows = random.choice([5, 10, 15, 20, 25])

departments = ["Electronics", "Fashion", "Home", "Grocery"]
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune", "Kolkata"]

# -----------------------------
# GENERATE DATA
# -----------------------------
data = []

for _ in range(num_rows):
    order_id = random.randint(100000, 999999)
    customer_id = random.randint(1000, 5000)
    product_id = random.randint(100, 999)

    order_time = datetime.now()
    delivery_delay = random.choice([0, 1, 2, 3, 5, 7])

    delivery_time = order_time + timedelta(days=delivery_delay)

    order_value = round(np.random.uniform(500, 5000), 2)
    discount = round(np.random.uniform(0, 0.3), 2)

    delivery_status = "Delayed" if delivery_delay > 3 else "On-Time"
    satisfaction_score = round(np.random.uniform(1, 5), 1)

    row = [
        order_id,
        customer_id,
        product_id,
        random.choice(departments),
        random.choice(cities),
        order_time.strftime("%Y-%m-%d %H:%M:%S"),
        delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
        order_value,
        discount,
        delivery_status,
        satisfaction_score
    ]

    data.append(row)

df = pd.DataFrame(data, columns=[
    "order_id", "customer_id", "product_id", "category", "city",
    "order_time", "delivery_time", "order_value", "discount",
    "delivery_status", "satisfaction_score"
])

# -----------------------------
# APPEND TO GOOGLE SHEET
# -----------------------------
sheet.append_rows(df.values.tolist())

print(f" Appended {num_rows} rows at {datetime.now()}")