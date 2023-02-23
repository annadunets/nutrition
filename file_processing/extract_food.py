import re, pypdf
from typing import List


class receipt_line:
    def __init__(self, product_name, quantity, units_of_measurement):
        self.product_name = product_name
        self.quantity = quantity
        self.units_of_measurement = units_of_measurement

class receipt_details:
    def __init__(self, date: str, receipt_lines: List[receipt_line]):
        self.date = date
        self.receipt_lines = receipt_lines

class pdf_receipt_parser:
    
    def extract_pdf(self, filename) -> receipt_details:
        # this is a list of objects each with properties: product_name, quantity, UOM
        our_goods = []
        date = ''

        # creating a pdf file object 
        with open(filename, 'rb') as pdfFileObj:
            # creating a pdf reader object
            myPdfReader = pypdf.PdfReader(pdfFileObj)
    
            # extracting text from page to var
            pagesNumber = len(myPdfReader.pages)
            for i in range(pagesNumber):
                pageObj = myPdfReader.pages[i]
                # зліплювати строчки з тими в яких немає ціни. Повернути масив строчок
                # і далі іти по ньому
                for line in pageObj.extract_text().splitlines():
                    product_pattern_kg = "[0-9]\.[0-9]{1,3}kg"
                    product_kg = re.search(product_pattern_kg, line)
                    #product_pattern_g = "[0-9]{1,3}g"
                    #product_g = re.search(product_pattern_g, line)
            
                    #if product_kg or product_g:
                    if product_kg:
                        our_goods.append(self.line_parser(line))

                    date_pattern = "Slot time: [a-z]* (.+?),.*"
                    date_search = re.search(date_pattern, line, flags=re.IGNORECASE)
                    if date_search:
                        date = date_search.group(1)

        return receipt_details(date, our_goods)
    
    def line_parser(self, line) -> receipt_line:
        quantity_pattern = "[0-9]\.[0-9]{1,3}kg"
        quantity = re.findall(quantity_pattern, line)

        amount_pattern = "[0-9]\.[0-9]{1,3}"
        amount = re.findall(amount_pattern, quantity[0])
        #amount_pattern = "([0-9]+[.]*[0-9]*)[k]*g"
        #amount_search = re.search(amount_pattern, line)
        #amount = amount_search.group(1)

        name_pattern = "\s[a-zA-Z\s]+"
        name = re.findall(name_pattern, line)

        units_of_measurement_pattern = "[0-9]\.[0-9]{1,3}kg"
        units_of_measurement = re.findall(units_of_measurement_pattern, quantity[0])

        return receipt_line(name[0], amount[0], units_of_measurement[0])