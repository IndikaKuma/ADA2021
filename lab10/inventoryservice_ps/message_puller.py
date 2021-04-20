import logging
import time
from threading import Thread

from google.cloud import pubsub_v1


def callback(message):
    print("Received message:", message.data)
    message.ack()


def pull_message(project, topic, subscription):
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=project,
        topic=topic
    )

    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project,
        sub=subscription
    )

    with pubsub_v1.SubscriberClient() as subscriber:
        subscriber.create_subscription(
            name=subscription_name, topic=topic_name)
        future = subscriber.subscribe(subscription_name, callback)
        try:
            future.result()
        except Exception as ex:
            logging.info(ex)
            time.sleep(30)


def create_subscription(project_id, topic_id, subscription_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        with subscriber:
            subscription = subscriber.create_subscription(subscription_path, topic_path)
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
                pull_message(self.project_id, self.topic, self.subscription_id)
            except Exception as ex:
                logging.info(ex)
                time.sleep(30)
