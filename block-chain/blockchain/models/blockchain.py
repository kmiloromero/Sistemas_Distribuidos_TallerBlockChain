
from .block import Block

class BlockChain:

    max_transactions = 3

    def __init__(self):
        self.chain = []
        block = Block(id=1)
        self.chain.append(block)

    def close_block(self, hash):
        last_block = self.chain[-1]
        last_block.hash = hash

        self.chain[-1] = last_block

        new_block = Block(
            id=len(self.chain)+1,
            hash_prev=last_block.hash
        )
        self.chain.append(new_block)


    def register_transaction(self, data):
        last_block = self.chain[-1]

        if len(last_block.data) < self.max_transactions:
            last_block.data.append(data)
            self.chain[-1] = last_block
            return True, last_block.get_data_to_str()
        else:
            return False, last_block.get_data_to_str()

    def to_json(self):
        results = []
        for block in self.chain:
            results.append(block.to_json())

        return results
