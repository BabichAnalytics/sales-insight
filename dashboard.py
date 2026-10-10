"""Sales Insight: local interactive dashboard using only standard Python."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_sales(path):
    sales = []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'date', 'product', 'region', 'units', 'unit_price'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('CSV requires date, product, region, units, unit_price headers.')
        for line, row in enumerate(reader, 2):
            try:
                day = date.fromisoformat(row['date'])
                units = int(row['units'])
                price = Decimal(row['unit_price'])
                if units < 0 or not price.is_finite() or price < 0:
                    raise ValueError('Units and prices must be finite and nonnegative.')
                if not row['product'].strip() or not row['region'].strip():
                    raise ValueError('Product and region cannot be blank.')
                sales.append({'date': day.isoformat(), 'product': row['product'].strip(),
                              'region': row['region'].strip(), 'units': units,
                              'revenue': float((price * units).quantize(Decimal('0.01')))})
            except (ValueError, TypeError, InvalidOperation, AttributeError) as error:
                raise ValueError(f'Invalid CSV record {line}: {error}') from error
    return sales

def handler_for(sales):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split('?', 1)[0]
            if path in ('/', '/index.html'):
                body, mime = (ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8'
            elif path == '/api/sales':
                body, mime = json.dumps(sales, allow_nan=False).encode(), 'application/json'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(body)
    return Handler

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=ROOT / 'sample_sales.csv')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    try:
        sales = load_sales(args.csv)
        server = HTTPServer(('127.0.0.1', args.port), handler_for(sales))
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Sales Insight: http://127.0.0.1:{args.port} — Ctrl+C to stop', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
