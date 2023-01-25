import re, pypdf


class receipt_line:
    def __init__(self, product_name, quantity, units_of_measurement):
        self.product_name = product_name
        self.quantity = quantity
        self.units_of_measurement = units_of_measurement


class pdf_receipt_parser:
    
    def extract_pdf(self, filename):
        our_goods = []

        # creating a pdf file object 
        with open(filename, 'rb') as pdfFileObj:
            # creating a pdf reader object
            myPdfReader = pypdf.PdfReader(pdfFileObj)
    
            # extracting text from page to var
            pagesNumber = len(myPdfReader.pages)
            for i in range(pagesNumber):
                pageObj = myPdfReader.pages[i]
                for line in pageObj.extract_text().splitlines():
                    pattern = "[0-9]\.[0-9]{1,3}kg"
                    x = re.search(pattern, line)
            
                    if x:
                        our_goods.append(self.line_parser(line))

        return our_goods
    
    def line_parser(self, line) -> receipt_line:
        quantity_pattern = "[0-9]\.[0-9]{1,3}kg"
        quantity = re.findall(quantity_pattern, line)
        name_pattern = "\s[a-zA-Z\s]+"
        name = re.findall(name_pattern, line)

        amount_pattern = "[0-9]\.[0-9]{1,3}"
        amount = re.findall(amount_pattern, quantity[0])
        units_of_measurement_pattern = "[0-9]\.[0-9]{1,3}kg"
        units_of_measurement = re.findall(units_of_measurement_pattern, quantity[0])

        return receipt_line(name[0], amount[0], units_of_measurement[0])