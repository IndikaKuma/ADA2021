import logging
import time
from threading import Thread

from google.cloud import pubsub_v1


def pull_message(project, subscription, timeout=30):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback(message):
        print(f"Received {message.data}.")
        message.ack()
        print(f"Done processing the message {message.data}.")

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, await_callbacks_on_shutdown=True,
    )
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            print("Streaming pull future canceled.")


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
        logging.info("create_subscription")
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
                pull_message(self.project_id, self.subscription_id)
                time.sleep(30)
            except Exception as ex:
                logging.info(ex)
                time.sleep(30)
