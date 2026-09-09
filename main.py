import csv, logging

row_count = 0
skipped_count = 0

# Dictionary to catalog products
# name: total_revenue, units_sold, num_orders, avg_order_value
products = {
    "Laptop": [0.00, 0, 0, 0.00],
    "Mouse": [0.00, 0, 0, 0.00],
    "Keyboard": [0.00, 0, 0, 0.00],
    "Monitor": [0.00, 0, 0, 0.00],
    "Headset": [0.00, 0, 0, 0.00],
}

logging.basicConfig(filename="errors.log",
                level=logging.INFO,
                format='%(message)s',
                filemode='w')

# handle_bad_data (input: transaction_id, reason)
def handle_bad_data(transaction_id: str, reason: str):
    logging.info(f"SKIPPED [transaction_id={transaction_id}] reason={reason}")

with open('sales.csv', mode='r', newline='', encoding='utf-8') as file:
    
    # Python's csv.reader reads CSV files line by line (lazily) 
    # as an iterator rather than loading the entire file into memory 
    # at once.
    
    csv_reader = csv.reader(file)
    
    # Skip/extract the header row if your file has one
    header = next(csv_reader)
    
    for row in csv_reader:
        #separate the values
        transaction_id = row[0]
        date = row[1]
        product = row[2]
        region = row[3]
        quantity_str = row[4]
        unit_price_str = row[5]

        #task 1
        row_count += 1

        #task 4 (checked on the raw strings, before conversion)
        if product == "":
            handle_bad_data(transaction_id, "missing product name")
            skipped_count += 1
            continue

        if quantity_str == "":
            handle_bad_data(transaction_id, "missing quantity")
            skipped_count += 1
            continue

        try:
            quantity = int(quantity_str)
        except ValueError:
            handle_bad_data(transaction_id, f"non-numeric quantity ({quantity_str})")
            skipped_count += 1
            continue
        
        if quantity < 0:
            handle_bad_data(transaction_id, f"negative quantity ({quantity})")
            skipped_count += 1
            continue

        try:
            unit_price = float(unit_price_str)
        except ValueError:
            handle_bad_data(transaction_id, f"non-numeric unit_price ({unit_price_str})")
            skipped_count += 1
            continue

        #task 2
        total_price = quantity * unit_price
        if total_price < 50.00:
            continue
        else:
            products[product][0] += total_price     # Total revenue
            products[product][1] += quantity        # Total units sold
            products[product][2] += 1               # Number of orders

# Calculate Average Order Value
for product in products:
    if products[product][2] != 0:
        products[product][3] = products[product][0] / products[product][2]

#task 3
# Convert products dictionary to CSV
# Format rows (excluding Orders at index 2)

# Round total_revenue and avg_order_value to 2 decimal places
for product in products:
    products[product][0] = round(products[product][0], 2)
    products[product][3] = round(products[product][3], 2)

# Sort data in descending order based on total revenue
sorted_products = dict(sorted(products.items(), key=lambda item: item[1][0], reverse=True))

csv_filename = "report.csv"

with open(csv_filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write headers
    writer.writerow(["product", "total_revenue", "total_units", "avg_order_value"])

    # Write data rows
    for product_name, metrics in sorted_products.items():
        # Exclude num_orders
        filtered_metrics = [metrics[0], metrics[1], metrics[3]]
        writer.writerow([product_name] + filtered_metrics)

print("Total rows: ", row_count)
print("Skipped rows: ", skipped_count)


