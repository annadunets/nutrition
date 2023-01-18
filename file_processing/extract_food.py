import re, pypdf


def extract_from_pdf(filename):
    our_goods = {}

    # creating a pdf file object 
    with open(filename, 'rb') as pdfFileObj:
        # creating a pdf reader object
        myPdfReader = pypdf.PdfReader(pdfFileObj)
    
        # extracting text from page to var
        pagesNumber = len(myPdfReader.pages)
        for i in range(pagesNumber):
            pageObj = myPdfReader.pages[i]
            for line in pageObj.extract_text().splitlines():
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