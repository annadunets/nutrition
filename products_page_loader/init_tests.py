import unittest
from extract_page import text_parser

class TestLineParser(unittest.TestCase):

    def test_line_with_food(self):

        text1 = """
            Fat 0.6g - -
            Saturates 0.2g - -
            Carbohydrate 3.1g - -
            Sugars 1.8g - -
            Fibre 2.5g - -
            Protein 4.3g - -
            Salt 0.02g - -"""
        actual1 = text_parser(text1)
        expected1 = {'Fat': 0.6, 'Carbohydrate': 3.1, 'Protein': 4.3}
        self.assertEqual(actual1, expected1)

        text2 = """
            Fat <0.5g <0.5g -
            Saturates <0.1g <0.1g -
            Carbohydrate 15.9g 27.8g 11%
            Sugars 0.8g 1.4g 2%
            Starch 15.1g 26.4g -
            Fibre 1.6g 2.8g -
            Protein 1.8g 3.2g 6%
            Salt <0.01g <0.01g -"""

        actual2 = text_parser(text2)
        expected2 = {'Fat': 0.5, 'Carbohydrate': 15.9, 'Protein': 1.8}
        self.assertEqual(actual2, expected2)



if __name__ == '__main__':
    unittest.main()