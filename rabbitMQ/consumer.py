import os
import sys

import pika

from models import Contact

def send_email(name):
    print(f'Email to {name} is sent!')

def main():
    credentials = pika.PlainCredentials('guest', 'guest')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    consumer = 'Worker1'
    def callback(ch, method, properties, body):
        pk = body.decode()
        contact = Contact.objects(id=pk, sent=False).first()
        if contact:
            contact.update(set__sent=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        send_email(contact.fullname)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', 
                          on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
