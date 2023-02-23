#!/usr/bin/env python
import sys, os, pika, psycopg2, json
import config, database
from queue_listener import QueueListener
from extract_food import pdf_receipt_parser


def main():

    listener = QueueListener
    listener.listen(config.MQ_HOSTNAME, 'received_new_pdf', process_pdf)

def process_pdf(data):

    receipt_id = data['receipt_id']
    filename = config.MAINDIR + '/receipts/' + data['file_name']
    receipt_data = pdf_receipt_parser().extract_pdf(filename)
    # insert a date from the receipt to the receipts table:
    database.alter_receipts_table(receipt_id, receipt_data.date)
    # update logs table:
    message = f"The receipts table has been updated with a date {receipt_data.date} for receipt Nº{receipt_id}"
    database.insert_into_receipt_processing_logs(receipt_id, message)

    # check if products from a new receipt are already in products table, if not - insert them
    fill_products_table(receipt_id, receipt_data.receipt_lines)
    
    # send a log to logs table in DB
    message = f'All products from receipt Nº{receipt_id} have been added to DB'
    database.insert_into_receipt_processing_logs(receipt_id, message) 


def fill_products_table(receipt_id, products):
    # start loop and check if the products from the receipt are already in products table
    for product_line in products:
        
        product_id = database.select_from_products(product_line.product_name)
        if product_id == None:
            # this product will be inserted into products table
            product_id = database.insert_into_products(product_line.product_name, None, None, None)
            # send message to rabbit MQ (to product page loader)
            data = {'receipt_id': receipt_id, 'name': product_line.product_name}
            send_to_queue(data)
            # send a log to logs table in DB 
            message = product_line.product_name + ' saved to DB'
            database.insert_into_receipt_processing_logs(receipt_id, message)
        
        # now we have all the info about the products 
        # we can add their quantity into receipts_content table
        # then we gonna do some maths and be ready to return results to users
        if product_id:
            database.insert_into_table_receipts_content(
                receipt_id, product_id, product_line.quantity, product_line.units_of_measurement)

def send_to_queue(data):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.MQ_HOSTNAME))
    channel = connection.channel()
    channel.queue_declare(queue='received_new_product')
    channel.basic_publish(exchange='', routing_key='received_new_product', body=json.dumps(data))

    connection.close()
   

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)