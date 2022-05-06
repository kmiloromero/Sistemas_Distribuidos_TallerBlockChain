from flask import Flask, request, jsonify, abort
from collection.wallet import WalletCollection

app = Flask(__name__)


@app.route("/wallet/", methods=['GET'])
def get_wallet():
    content = request.json
    collection = WalletCollection()
    wallet = collection.get_by_dir(content.get('dir'))
    if wallet:
        return jsonify(wallet)
    else:
        return jsonify({})


@app.route("/wallet/create/", methods=['POST'])
def create_wallet():
    wallet = request.json
    collection = WalletCollection()
    collection.add_wallet(wallet)
    collection.save()
    if wallet:
        return jsonify(wallet)
    else:
        return jsonify({})


@app.route("/wallet/update-amount/", methods=['POST'])
def update_amount():
    content = request.json
    collection = WalletCollection()
    response, wallet = collection.set_amount(
        content.get('dir'), content.get('amount')
    )
    if response:
        return jsonify(wallet)
    else:
        return abort(400)
