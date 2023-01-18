#!/usr/bin/env python
import sys, os, pika, psycopg2
from os.path import dirname, abspath

from queue_listener import QueueListener
import database, extract_food
#from pathlib import Path



def main():

    listener = QueueListener
    listener.listen('some-rabbit', 'received_new_pdf', process_pdf)

def process_pdf(data):
    
    database.insert_into_db(data['name'])
   # filename = str(Path.cwd()) + '/receipts/' + data['name']
    filename = str(dirname(dirname(abspath(__file__)))) + '/receipts/' + data['name']
    print(filename)
    extract_food.extract_from_pdf(filename)
    

   

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)