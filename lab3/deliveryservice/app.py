from flask import Flask, request

from db import Base, engine
from resources.delivery import create_delivery, get_delivery, delete_delivery
from resources.status import update_status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/deliveries', methods=['POST'])
def create_delivery_api():
    req_data = request.get_json()
    return create_delivery(req_data)


@app.route('/deliveries/<d_id>', methods=['GET'])
def get_delivery_api(d_id):
    return get_delivery(d_id)


@app.route('/deliveries/<d_id>/status', methods=['PUT'])
def update_delivery_status_api(d_id):
    status = request.args.get('status')
    return update_status(d_id, status)


@app.route('/deliveries/<d_id>', methods=['DELETE'])
def delete_delivery_api(d_id):
    return delete_delivery(d_id)


app.run(host='0.0.0.0', port=5000)
