from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load products from the local JSON file.
def load_products_from_json():
    json_file_path = os.path.join(os.path.dirname(__file__), 'products.json')
    with open(json_file_path, 'r') as f:
        return json.load(f)

@app.route('/products', methods=['GET'])
def get_products():
    products = load_products_from_json()
    return jsonify(products)

@app.route('/ucp/products', methods=['GET'])
def get_ucp_products():
    # For this POC, we'll serve the same products from the JSON file.
    products = load_products_from_json()
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
