import json
from datetime import datetime

from constant import STATUS_CREATED
from daos.delivery_dao import DeliveryDAO
from daos.status_dao import StatusDAO
from db import Session


def create_delivery(data):
    session = Session()
    delivery = DeliveryDAO(data['customer_id'], data['provider_id'], data['package_id'], datetime.now(),
                           datetime.strptime(data['delivery_time'], '%Y-%m-%d %H:%M:%S.%f'),
                           StatusDAO(STATUS_CREATED, datetime.now()))
    session.add(delivery)
    session.commit()
    session.refresh(delivery)
    session.close()
    return json.dumps({'delivery_id': delivery.id}, sort_keys=False, indent=4), 200


def get_delivery(d_id):
    session = Session()
    # 3 - extract all movies
    delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id).first()
    session.close()
    if delivery:
        status_obj = delivery.status
        text_out = {
            "customer_id:": delivery.customer_id,
            "provider_id": delivery.provider_id,
            "package_id": delivery.package_id,
            "order_time": delivery.order_time.isoformat(),
            "delivery_time": delivery.delivery_time.isoformat(),
            "status": status_obj.status
        }
        return json.dumps(text_out, sort_keys=False, indent=4), 200
    else:
        return json.dumps({'message': f'There is no delivery with id {d_id}'}, sort_keys=False, indent=4), 200


def delete_delivery(d_id):
    session = Session()
    # 3 - extract all movies
    effected_rows = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id).delete()
    session.commit()
    session.close()
    if effected_rows == 0:
        return json.dumps({'message': f'There is no delivery with id {d_id}'}, sort_keys=False, indent=4), 200
    else:
        return json.dumps({'message': 'The delivery was removed'}, sort_keys=False, indent=4), 200
