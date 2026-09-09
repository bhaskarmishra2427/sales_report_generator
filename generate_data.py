# generate_data.py
import csv, random, uuid
from datetime import date, timedelta

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset"]
regions = ["North", "South", "East", "West"]

TOTAL_ROWS = 100_000
BAD_ROW_PROBABILITY = 500 / TOTAL_ROWS

bad_row_types = [
    "missing_product",
    "negative_quantity",
    "non_numeric_price",
    "missing_quantity",
]

with open("sales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "date", "product", "region", "quantity", "unit_price"])
    start = date(2024, 1, 1)
    for _ in range(TOTAL_ROWS):
        d = start + timedelta(days=random.randint(0, 364))
        product = random.choice(products)
        price = {"Laptop": 999.99, "Mouse": 29.99, "Keyboard": 79.99, "Monitor": 349.99, "Headset": 89.99}[product]
        quantity = random.randint(1, 5)
        # random.random() generates a float between 0.0 - 1.0
        if random.random() < BAD_ROW_PROBABILITY:
            bad_type = random.choice(bad_row_types)
            if bad_type == "missing_product":
                product = ""
            elif bad_type == "negative_quantity":
                quantity = -quantity
            elif bad_type == "non_numeric_price":
                price = "N/A"
            elif bad_type == "missing_quantity":
                quantity = ""

        writer.writerow([str(uuid.uuid4()), d, product, random.choice(regions), quantity, price])
