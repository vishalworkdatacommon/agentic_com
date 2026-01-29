from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    with open('mcp_server/products.json', 'r') as f:
        products = json.load(f)
    return jsonify(products)

@app.route('/ucp/products', methods=['GET'])
def get_ucp_products():
    # For this POC, we'll serve the same products.json, but in a real scenario,
    # this endpoint would apply UCP-specific transformations or filters.
    with open('mcp_server/products.json', 'r') as f:
        products = json.load(f)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
