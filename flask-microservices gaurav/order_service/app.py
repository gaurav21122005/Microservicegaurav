from flask import Flask, jsonify
import requests

app = Flask(__name__)

orders = [
    {"id": 1, "user_id": 1, "item": "Boxing Gloves"},
    {"id": 2, "user_id": 2, "item": "Sneakers"}
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order:
        # Call user_service to get user info
        user_service_url = f"http://user_service:5001/users/{order['user_id']}"
        user = requests.get(user_service_url).json()
        order["user"] = user
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
