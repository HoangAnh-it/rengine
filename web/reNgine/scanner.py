from rabbitmq import RabbitMQ
import environ

env = environ.FileAwareEnv()

RABBITMQ_CONFIG = {
    "BROKER_HOST": env("BROKER_HOST"),
    "BROKER_PORT": env("BROKER_PORT"),
    "BROKER_USER": env("BROKER_USER"),
    "BROKER_PASS": env("BROKER_PASS"),
    "MANAGER_PORT": env("MANAGER_PORT"),
    "QUEUE": env("BROKER_QUEUE"),
}

rabbitmq = RabbitMQ(RABBITMQ_CONFIG)
rabbitmq.create_connection()


def scanner(ch, method, pro, body):
    print(body)


try:
    rabbitmq.consume(scanner, "scanner")
except Exception as e:
    print(e)
