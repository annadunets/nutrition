# importing required modules 
import PyPDF2
import re

file = 'sainsburys.pdf'
our_goods = {}

# creating a pdf file object 
with open(file, 'rb') as pdfFileObj:
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    # extracting text from page to var
    pagesNumber = pdfReader.numPages
    # creating a page object
    for i in range(pagesNumber):
        pageObj = pdfReader.getPage(i)
        for line in pageObj.extractText().splitlines():
            pattern = "[0-9]\.[0-9]{1,3}kg"
            x = re.search(pattern, line)
            
            if x:
                quantity_pattern = "[0-9]\.[0-9]{1,3}kg"
                quantity = re.findall(quantity_pattern, line)
                name_pattern = "\s[a-zA-Z\s]+"
                name = re.findall(name_pattern, line)
                our_goods[name[0]] = quantity[0]


for key, value in our_goods.items():
    print(key)
    print(value)
