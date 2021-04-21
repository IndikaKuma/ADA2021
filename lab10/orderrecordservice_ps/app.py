import base64
import logging
import os

from flask import Flask, request

from message_puller import MessagePuller
from pub_sub_util import create_topic, create_subscription
from resources.order import Order, Orders

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
orders = Orders()
order = Order()
project_id = os.environ['project_id']
service_uri = os.environ['service_uri']
endpoint = service_uri + "orders_ps/"
create_subscription(project=project_id, topic="inventory_status",
                    subscription="inventory_status_orderrecord_sub")
create_topic(project=project_id, topic="order_status")
MessagePuller(project=project_id, subscription="order_req_sub", orders=orders)


@app.route("/orders_ps/", methods=["POST"])
def index():
    envelope = request.get_json()

    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    print(f"Hello {pubsub_message}!")
    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"Hello {name}!")

    return "", 204


@app.route('/orders/<string:id>', methods=['GET'])
def get_order(id):
    return order.get(id)


@app.route('/orders/<string:id>', methods=['PUT'])
def update_order(id):
    return order.put(id, int(request.args.get('rating')))


@app.route('/orders/<string:id>', methods=['DELETE'])
def delete_orders(id):
    return order.delete(id)


@app.route('/orders/', methods=['POST'])
def create_order():
    return orders.post(request)


app.run(host='0.0.0.0', port=5000, debug=True)
