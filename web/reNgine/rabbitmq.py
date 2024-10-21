import pika


class RabbitMQ:

    def __init__(self, config):
        self.BROKER_HOST = config["BROKER_HOST"]
        self.BROKER_PORT = config["BROKER_PORT"]
        self.BROKER_USER = config["BROKER_USER"]
        self.BROKER_PASS = config["BROKER_PASS"]
        self.QUEUE = config["QUEUE"]
        self.MANAGER_PORT = config["MANAGER_PORT"]
        self.connection = None
        self.channel = None
        self.priority_queue = {"x-max-priority": 10}

    def create_connection(self):
        try:
            credentials = pika.PlainCredentials(
                self.BROKER_USER,
                self.BROKER_PASS,
            )

            parameters = pika.ConnectionParameters(
                self.BROKER_HOST,
                int(self.BROKER_PORT),
                "/",
                credentials=credentials,
                heartbeat=30,
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.QUEUE, durable=True, arguments=self.priority_queue)
            print("👉👉👉👉👉 connected to rabbitmq", self.QUEUE)
        except Exception as e:
            print(e)
            self.connection = None
            self.channel = None
            print("Cannot connect to rabbitmq")

    def get_connection(self):
        return self.connection

    def get_channel(self):
        return self.channel

    def push(self, data):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.QUEUE,
            body=data,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def consume(self, callback, queue=None):
        if queue is None:
            queue = self.QUEUE

        self.channel.basic_consume(
            queue=queue,
            on_message_callback=callback,
            auto_ack=True,
        )
        self.channel.start_consuming()
