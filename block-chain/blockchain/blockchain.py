import hashlib

from flask import Flask, request, jsonify, abort

from models.blockchain import BlockChain

app = Flask(__name__)

chain = BlockChain()

@app.route("/register-transaction/", methods=['POST'])
def register_transaction():
    transaction = request.json

    data = f"{transaction.get('dir1')}," \
           f"{transaction.get('dir2')}," \
           f"{transaction.get('amount')}"

    result, data = chain.register_transaction(data)

    return jsonify({"result": result, "data": data})

@app.route("/close-block/", methods=['POST'])
def close_block():
    hash = request.json.get('hash')
    chain.close_block(hash)

    return jsonify({"result": True})

@app.route("/chain/", methods=['GET'])
def get_chain():
    return jsonify({"result": chain.to_json()})