class Block:

    def __init__(self, id, hash_prev=None):
        self.id = id
        self.nonce = 0
        self.data = []
        self.hash_prev = hash_prev
        self.hash = None


    def get_data_to_str(self):
        result = ''
        for tx in self.data:
            result += tx
        return result

    def to_json(self):
        return {
            "id": self.id,
            "nonce": self.nonce,
            "data": self.data,
            "hash_prev": self.hash_prev,
            "hash": self.hash
        }