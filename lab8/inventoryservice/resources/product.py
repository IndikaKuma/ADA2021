from flask import jsonify

inventories = [
    {
        "name": "Laptop",
        "quantity": 1000
    },
    {
        "name": "Phone",
        "quantity": 5000
    }
]


class Product:
    def get(self, pname):
        for record in inventories:
            if pname == record["name"]:
                return jsonify(record), 200
        return jsonify({"message": "No product for " + pname}), 404

    def put(self, pname, value):
        for record in inventories:
            if pname == record["name"]:
                record["quantity"] = record["quantity"] - value
                return jsonify(record), 200
        return jsonify({"message": "No product for " + pname}), 404
