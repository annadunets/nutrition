#!/usr/bin/env python
import sys, os, pika, psycopg2
from queue_listener import QueueListener
import database

def main():

    listener = QueueListener
    listener.listen('some-rabbit', 'received_new_pdf', process_pdf)

def process_pdf(data):
    database.insert_into_db(data['name'])
    print(" [x] Received %r" % data['name'])
   

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)