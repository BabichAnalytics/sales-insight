# Sales Insight

A local, interactive sales performance dashboard built with Python and browser JavaScript. Uses the Python standard library: no packages or account required.

## Run

Install Python 3.10 or newer, download this repository, open a terminal in its folder, and run:

```bash
python dashboard.py
```

Open **http://127.0.0.1:8000** in your browser. Keep the terminal open; press Ctrl+C to stop.

If your computer uses `python3`, substitute that command. For a busy port: `python dashboard.py --port 8001`.

## Features

- Revenue, units, sales records, and revenue per record
- Region, product, and date filters
- Monthly revenue, top products, and regional comparison charts
- Download filtered data as CSV
- Clear empty-data and invalid-date messages

## Your own data

```bash
python dashboard.py --csv your_sales.csv
```

Required columns: `date,product,region,units,unit_price`. Dates use YYYY-MM-DD. Units must be nonnegative integers; unit prices must be finite, nonnegative USD amounts. Revenue is units times price, rounded to cents. Each record is a sales line, not necessarily a unique order. Taxes, returns, and discounts are not modeled. Input stays on your computer; the server binds to localhost only.

## Sample data and tests

`sample_sales.csv` contains 720 fictional records spanning January–December 2025. It contains no customer information or real business data.

```bash
python -m unittest -v
```

Built as a portfolio example; not an accounting system. Very large CSVs are loaded into memory and may require a database-backed design.
