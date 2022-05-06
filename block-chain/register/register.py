from flask import Flask, request, jsonify, abort

app = Flask(__name__)


@app.route("/check-transaction/", methods=['POST'])
def check_transaction():
    wallet1 = request.json.get('wallet1')
    transaction = request.json.get('transaction')

    if wallet1.get('amount') >= transaction.get('amount'):
        return jsonify({"result": True})
    else:
        return jsonify({"result": False})
