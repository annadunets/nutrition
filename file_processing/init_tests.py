import unittest
from extract_food import pdf_receipt_parser, receipt_line

class TestLineParser(unittest.TestCase):

    def test_line_with_food(self):
        actual = pdf_receipt_parser().line_parser("1.168kgSainsbury's Butternut Squash Loose £1.46")
        self.assertEqual(actual.product_name, "Butternut Squash Loose")
        self.assertEqual(actual.quantity, "1.168")
        self.assertEqual(actual.units_of_measurement, "kg")


if __name__ == '__main__':
    unittest.main()