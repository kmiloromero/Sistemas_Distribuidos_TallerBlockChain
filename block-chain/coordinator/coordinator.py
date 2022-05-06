import requests
from flask import Flask, request, jsonify, abort

app = Flask(__name__)


REGISTER_URL = 'http://register:5000'
WALLETS_URL = 'http://wallets:5000'
BLOCKCHAIN_URL = 'http://blockchain:5000'
OPEN_CLOSER_URL = 'http://open_closer:5000'


@app.route("/transaction/create/", methods=['POST'])
def create_transaction():
    """
        transaction
        {
            "dir1": str,
            "dir2": str,
            "amount": int
        }
    """
    transaction = request.json

    wallet1 = requests.get(
        f"{WALLETS_URL}/wallet/", json={"dir": transaction.get('dir1')},
        headers={"Content-Type": "application/json"}
    ).json()

    if not wallet1:
        return jsonify({"result": "error, wallet1 dir not exist"})

    wallet2 = requests.get(
        f"{WALLETS_URL}/wallet/", json={"dir": transaction.get('dir2')},
        headers={"Content-Type": "application/json"}
    ).json()

    if not wallet2:
        if type(transaction.get('dir2')) is str:
            response = requests.post(
                f"{WALLETS_URL}/wallet/create",
                json={"dir": transaction.get('dir2'), "amount": 0},
                headers={"Content-Type": "application/json"}
            )

            wallet2 = response.json()
        else:
            return jsonify({"result": "error, wallet2 dir not is str"})

    transaction_data = {
        "wallet1": wallet1,
        "wallet2": wallet2,
        "transaction": transaction
    }

    check_transaction = requests.post(
        f"{REGISTER_URL}/check-transaction/",
        headers={"Content-Type": "application/json"},
        json=transaction_data,
    ).json().get('result')

    if check_transaction:

        check_block = False

        while not check_block:
            response_json = requests.post(
                f"{BLOCKCHAIN_URL}/register-transaction/",
                headers={"Content-Type": "application/json"},
                json=transaction,
            ).json()

            result = response_json.get('result')
            data = response_json.get('data')

            if result:
                check_block = True

                new_wallet1_amount = wallet1.get('amount') - transaction.get('amount')
                new_wallet2_amount = wallet2.get('amount') + transaction.get('amount')

                requests.post(
                    f"{WALLETS_URL}/wallet/update-amount/",
                    headers={"Content-Type": "application/json"},
                    json = {"dir": wallet1.get('dir'), "amount": new_wallet1_amount}
                )
                requests.post(
                    f"{WALLETS_URL}/wallet/update-amount/",
                    headers={"Content-Type": "application/json"},
                    json = {"dir": wallet2.get('dir'), "amount": new_wallet2_amount}
                )

            else:
                hash = requests.post(
                    f"{OPEN_CLOSER_URL}/generate-hash/",
                    headers={"Content-Type": "application/json"},
                    json={"data": data},
                ).json().get('hash')

                requests.post(
                    f"{BLOCKCHAIN_URL}/close-block/",
                    headers={"Content-Type": "application/json"},
                    json={"hash": hash},
                ).json()
    else:
        return jsonify({"result": "error, the transaction have invalid types"})
    return jsonify(
        {
            "result": "the transaction has been registered succesfully",
            "transaction": transaction
        }
    )


@app.route("/blockchain/", methods=['GET'])
def get_blockchain_details():
    return jsonify(requests.get(f"{BLOCKCHAIN_URL}/chain/").json())