import logging
import time
from threading import Thread

from google.cloud import pubsub_v1


def callback(message):
    print("Received message:", message.data)
    message.ack()


def pull_message(project, subscription):

    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(project, subscription)
        future = subscriber.subscribe(subscription_path, callback)
        try:
            future.result(timeout=10000)
        except Exception as ex:
            logging.info(ex)
            future.cancel()


def create_subscription(project_id, topic_id, subscription_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        with subscriber:
            subscription = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
        print(f"Subscription created: {subscription}")
    except Exception as ex:
        logging.info(ex)


class MessagePuller(Thread):
    def __init__(self, project, topic, subscription):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        self.daemon = True
        self.topic = topic
        logging.basicConfig(level=logging.INFO)
        create_subscription(project, topic, subscription)
        self.start()

    def run(self):
        while True:
            try:
                print("*** Before Pull***")
                pull_message(self.project_id, self.subscription_id)
                time.sleep(30)
            except Exception as ex:
                logging.info(ex)
                time.sleep(30)
