# 1 - imports
from daos.place_dao import DeliveryDAO
from db import Session

# 2 - extract a session
session = Session()

deliveries = session.query(DeliveryDAO).all()

print('\n### All deliveries:')
for delivery in deliveries:
    print(f'{delivery.id} was created by {delivery.customer_id}. Its current status is {delivery.status.status}')
print('')
