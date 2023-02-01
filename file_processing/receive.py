#!/usr/bin/env python
import sys, os, pika, psycopg2, json
import config, database
from queue_listener import QueueListener
from extract_food import pdf_receipt_parser


def main():

    listener = QueueListener
    listener.listen(config.MQ_HOSTNAME, 'received_new_pdf', process_pdf)

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
            product_id = database.insert_into_products(product_line.product_name, None, None, None)
            # send message to rabbit MQ (to product page loader)
            send_to_queue(product_line.product_name)
        
        # now we have all the info about the products 
        # we can add their quantity into receipts_content table
        # then we gonna do some maths and be ready to return results to users
        if product_id:
            database.insert_into_table_receipts_content(
                receipt_id, product_id, product_line.quantity, product_line.units_of_measurement)



def send_to_queue(product_name):
    print(f"{product_name} is send to the queue")

    data = {'name': product_name}

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