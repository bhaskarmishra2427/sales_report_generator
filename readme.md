# Sales Report Generator

A Python program that processes sales transactions one row at a time, validates records, and generates a product summary report.

## Files

- `generate_data.py` — generates `sales.csv`
- `sales.csv` — source transaction data
- `main.py` — validates and processes sales data
- `report.csv` — generated product summary
- `errors.log` — skipped records and validation errors

## Run

```bash
python3 generate_data.py
python3 main.py
```

The program prints the total and skipped row counts, then creates `report.csv` and `errors.log`.

## Report Columns

- `product`
- `total_revenue`
- `total_units`
- `avg_order_value`

Transactions below `$50.00` are excluded. Invalid records are skipped and logged.