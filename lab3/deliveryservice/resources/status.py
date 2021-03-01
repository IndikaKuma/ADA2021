import json

from daos.delivery_dao import DeliveryDAO
from db import Session


def update_status(d_id, status):
    session = Session()
    # 3 - extract all movies
    delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id)[0]
    delivery.status.status = status
    session.commit()
    return json.dumps({'message': 'The delivery status was updated'}, sort_keys=False, indent=4), 200
