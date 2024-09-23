import pika

from datetime import datetime

import faker

from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()

channel.exchange_declare(exchange='task_mock', 
                         exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

fake = faker.Faker('uk-UA')

def main():
    for i in range(5):
        contact = Contact(
            fullname = fake.unique.name(),
            email = fake.unique.email()
        ).save()

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    connection.close()


if __name__ == '__main__':
    main()





 