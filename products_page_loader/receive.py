#!/usr/bin/env python
import sys, os, pika, psycopg2
import config
from queue_listener import QueueListener


def main():

    listener = QueueListener
    listener.listen(config.MQ_HOSTNAME, 'received_new_product', extract_page)

def extract_page(data):
    print(data)
   

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)