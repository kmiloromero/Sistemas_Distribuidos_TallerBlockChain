import os
import json


class WalletCollection:

    wallets = []

    def __init__(self):
        path = os.path.dirname(__file__)
        self.filename = f'{path}/wallets.json'
        self.load_wallets()

    def to_dict(self, wallet):
        return {"dir": wallet.get('dir'),
                "amount": wallet.get('amount')}

    def load_wallets(self):
        with open(self.filename, "r") as wallets_file:
            self.wallets = json.loads(wallets_file.read())

    def get_by_dir(self, dir):
        for idx, wallet in enumerate(self.wallets, start=0):
            if wallet.get('dir') == dir:
                return wallet
        return None

    def remove_by_dir(self, dir):
        for idx, wallet in enumerate(self.wallets, start=0):
            if wallet.get('dir') == dir:
                self.wallets.pop(idx)
                return True
        return False

    def add_wallet(self, wallet):
        self.wallets.append(wallet)

    def save(self):
        with open(self.filename, "w") as wallets_file:
            wallets_file.write(json.dumps(self.wallets))

    def set_amount(self, dir, amount):
        wallet = self.get_by_dir(dir)
        wallet['amount'] = amount
        self.remove_by_dir(wallet.get('dir'))
        self.add_wallet(wallet)
        self.save()
        return True, wallet

    # def set_amount(self, dir1, dir2, amount):
    #     try:
    #         wallet1 = self.get_by_dir(dir1)
    #         wallet2 = self.get_by_dir(dir2)
    #         wallet1['amount'] = (int(wallet1['amount']) - amount)
    #
    #         self.remove_by_dir(wallet1.get('dir'))
    #         self.add_wallet(wallet1)
    #
    #         if wallet2:
    #             wallet2['amount'] = (int(wallet2['amount']) + amount)
    #
    #             self.remove_by_dir(wallet2.get(dir))
    #             self.add_wallet(wallet2)
    #         else:
    #             wallet2 = self.__create_wallet(dir2, amount)
    #             self.add_wallet(wallet2)
    #
    #         self.save()
    #     except Exception as e:
    #         print(e)
    #         return False
    #
    #     return True
