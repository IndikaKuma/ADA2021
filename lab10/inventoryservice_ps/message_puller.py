import json
import logging
import time
from threading import Thread

from google.cloud import pubsub_v1

from pub_sub_util import publish_message


def pull_message(project, subscription, product):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback(message):
        logging.info(f"Received {message.data}.")
        data = json.loads(message.data.decode("utf-8"))
        quantity = product.get_quantity(data["product_type"])
        if quantity > data["quantity"]:
            data = {
                "message": "The requested quantity can be satisfied"
            }
            data = json.dumps(data).encode("utf-8")
            publish_message(project=project, topic="inventory_status", message=data, event="StockAvailable")
            logging.info("StockAvailable")
        else:
            data = {
                "message": "The requested quantity cannot be satisfied"
            }
            data = json.dumps(data).encode("utf-8")
            publish_message(project=project, topic="inventory_status", message=data, event="StockUnavailable")
            logging.info("StockUnavailable")
        message.ack()
        logging.info(f"Done processing the message {data}.")

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, await_callbacks_on_shutdown=True,
    )
    logging.info(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=60)
        except TimeoutError:
            streaming_pull_future.cancel()
            logging.info("Streaming pull future canceled.")


class MessagePuller(Thread):
    def __init__(self, project, subscription, product):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        self.daemon = True
        self.product = product
        self.start()

    def run(self):
        while True:
            try:
                print("Pulling Messages")
                pull_message(self.project_id, self.subscription_id, self.product)
                time.sleep(30)
            except Exception as ex:
                logging.info(f"Listening for messages on {self.subscription_id} threw an exception: {ex}.")
                time.sleep(30)
