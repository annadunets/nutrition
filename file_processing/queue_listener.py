import pika, json

class QueueListener:
    def listen(hostname, queue_name, process_pdf):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        def callback(ch, method, properties, body):
            process_pdf(json.loads(body))
            

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
