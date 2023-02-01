#!/usr/bin/env python
import sys, os, pika, psycopg2
import config, database, extract_page
from queue_listener import QueueListener


def main():

    listener = QueueListener
    listener.listen(config.MQ_HOSTNAME, 'received_new_product', process_received_data)


def process_received_data(data):

    try:
        nutrition_arr = extract_page.load_page(data['name'])
    except Exception as error:
        print(error)
        return

    fat = 0 if '<' in nutrition_arr[0] else float(nutrition_arr[0])
    carbohydrate = 0 if '<' in nutrition_arr[1] else float(nutrition_arr[1])
    protein = 0 if '<' in nutrition_arr[2] else float(nutrition_arr[2])
    database.alter_products_info(data['name'], fat, carbohydrate, protein)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)