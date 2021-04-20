import logging
import time

from google.cloud import pubsub_v1
import logging
import time

from google.cloud import pubsub_v1


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


def callback(message):
    print(f"Received {message}.")
    message.ack()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    create_subscription("ada2020-305519", "order_status_user", "order_status_user_sub")
    pull_message("ada2020-305519","order_status_user", "order_status_user_sub")