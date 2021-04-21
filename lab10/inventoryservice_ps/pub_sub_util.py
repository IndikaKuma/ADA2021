import logging

from google.cloud import pubsub_v1


def create_push_subscription(project, topic, subscription, endpoint):
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project, topic)
    subscription_path = subscriber.subscription_path(project, subscription)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
            }
        )

    logging.info(f"Push subscription created: {subscription}.")
    logging.info(f"Endpoint for subscription is: {endpoint}")


def create_topic(project, topic):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project, topic)
        topic = publisher.create_topic(request={"name": topic_path})
        print("Created topic: {}".format(topic.name))
    except Exception as ex:
        logging.info(ex)


def publish_message(project, topic, message, event_type):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    # event_type is a custom message attribute or meta-data. We can use our own meta-data.
    future = publisher.publish(topic_path, message, event_type=event_type)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
    print(f"Published event {event_type} to {topic_path}.")


def create_subscription(project, topic, subscription):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project, topic)
        subscription_path = subscriber.subscription_path(project, subscription)
        with subscriber:
            subscription_en = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
        logging.info(f"Subscription created: {subscription_en}")
    except Exception as ex:
        logging.info(f"Error creating subscription {subscription} , the exception: {ex}.")
