import tempfile
import unittest
from pathlib import Path
from dashboard import load_sales

class SalesTests(unittest.TestCase):
    def load(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'sales.csv'
            path.write_text(text)
            return load_sales(path)
    def test_revenue_and_quoted_product(self):
        rows=self.load('date,product,region,units,unit_price\n2025-01-02,"Widget, large",East,3,12.35\n')
        self.assertEqual(rows[0]['revenue'],37.05)
        self.assertEqual(rows[0]['product'],'Widget, large')
    def test_bad_headers(self):
        with self.assertRaises(ValueError): self.load('x,y\n1,2\n')
    def test_invalid_values(self):
        for values in ['2025-02-30,A,East,1,2','2025-01-01,A,East,-1,2','2025-01-01,A,East,1,NaN']:
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.load('date,product,region,units,unit_price\n'+values+'\n')
    def test_empty_dataset(self):
        self.assertEqual(self.load('date,product,region,units,unit_price\n'),[])

if __name__=='__main__': unittest.main()
