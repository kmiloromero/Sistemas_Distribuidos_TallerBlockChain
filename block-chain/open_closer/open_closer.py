import hashlib

from flask import Flask, request, jsonify, abort


app = Flask(__name__)


@app.route("/generate-hash/", methods=['POST'])
def generate_hash():
    data = request.json.get('data')
    nonce = 0
    while True:
        var = data + str(nonce)
        hash = hashlib.sha256(var.encode('utf-8')).hexdigest()
        if hash[0:4] == '0000':
            break
        nonce += 1
    return jsonify({"hash": hash})
