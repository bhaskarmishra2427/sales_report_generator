# Sales Report Generator

A Python program that processes sales transactions one row at a time, validates records, and generates a product summary report.

## Files

- `generate_data.py` — generates `sales.csv` (Python, includes ~500 injected bad rows)
- `generate_data.c` — faster C generator for large datasets (no bad-row injection, no error handling); row count is set via `TOTAL_ROWS` in the source
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

### Generating larger datasets (C generator)

For testing at larger file sizes, use `generate_data.c` instead of the Python generator:

```bash
gcc -O2 -o generate_data generate_data.c
./generate_data
```

Edit `#define TOTAL_ROWS` in `generate_data.c` to control the output size (~70 bytes/row, so `TOTAL_ROWS=15200000` produces roughly 1GB).

## Report Columns

- `product`
- `total_revenue`
- `total_units`
- `avg_order_value`

Transactions below `$50.00` are excluded. Invalid records are skipped and logged.

## Memory Test

`main.py` reads `sales.csv` one row at a time (`csv.reader` as a lazy iterator) and aggregates into a fixed-size dict keyed by product, so peak memory should stay flat as the input file grows — only runtime should scale with row count. Measured with `/usr/bin/time -l python3 main.py` on macOS:

| Rows      | File size | Real time | Peak memory footprint |
|-----------|-----------|-----------|------------------------|
| 100,000   | ~7 MB     | 0.16s     | ~6.9 MB (7,258,400 bytes) |
| 15,200,000| ~1 GB     | 18.51s    | ~6.9 MB (7,225,632 bytes) |

Peak memory footprint is effectively identical across a ~150x increase in file size, while runtime scales roughly linearly with row count — confirming the row-by-row streaming design doesn't load the file into memory. The 1GB dataset was generated with `generate_data.c` (see above).