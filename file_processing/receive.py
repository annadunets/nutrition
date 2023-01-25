#!/usr/bin/env python
import sys, os, pika, psycopg2
from queue_listener import QueueListener
import config, database
from extract_food import pdf_receipt_parser


def main():

    listener = QueueListener
    listener.listen('some-rabbit', 'received_new_pdf', process_pdf)

def process_pdf(data):
    
    # this shuld return the new receipt id
    receipt_id = database.insert_into_receipts(data['name'])
    filename = config.MAINDIR + '/receipts/' + data['name']
    receipt_data = pdf_receipt_parser().extract_pdf(filename)
    # start loop and check if the produnct from the receipt are already in products table

    for product_line in receipt_data:
        product_id = database.select_from_products(product_line.product_name)
        if product_id == None:
            # this product will be inserted into products table
            products_info_extraction()
            product_id = database.insert_into_products(product_line.product_name, None, None, None)
        
        # now we have all the info about the products 
        # we can add their quantity into receipts_content table
        # then we gonna do some maths and be ready to return results to users
        if product_id:
            database.insert_into_table_receipts_content(
                receipt_id, product_id, product_line.quantity, product_line.units_of_measurement)

    print(receipt_data)


def products_info_extraction():
    pass
   

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)