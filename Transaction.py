import datetime

import bitcoin

from Blockchain import *


class TxIn:
    def __init__(self, utxo):
        self.hash = utxo['hash']  # 사용할 UTXO가 포함된 트랜잭션 해쉬값
        self.idx = utxo['index']  # 트랜잭션 중 UTXO의 순서
        self.address = utxo['to']  # UTXO의 수신 주소 (공개키 해쉬)
        self.amount = utxo['amount']  # UTXO의 잔액
        self.publickey = None  # 사용자 공개키
        self.sign = None  # 서명

    def __str__(self):
        result = {
            'hash': self.hash,
            'idx': self.idx,
            'address': self.address,
            'amount': self.amount,
            'publickey': self.publickey,
            'sign': self.sign
        }
        return json.dumps(result, sort_keys=False)


class TxOut:
    def __init__(self, receiver_address, amount):
        self.to = receiver_address  # 받는 사람 주소
        self.amount = amount  # 금액

    def __str__(self):
        result = {
            'to': self.to,
            'amount': self.amount
        }
        return json.dumps(result, sort_keys=False)


class Transaction:
    def __init__(self, blockchain, amount, receiver_address, sender_address=None, sender_private_key=None):
        self.vin_size = 0
        self.vout_size = 0
        self.tx_inputs = []
        self.tx_outputs = []
        self.hash = None
        self.locktime = datetime.datetime.now()

        # 코인 베이스 트랜잭션
        if sender_address is None:
            tx_out = TxOut(receiver_address, amount)
            self.tx_outputs.append(json.loads(str(tx_out)))
            self.vout_size = 1
            self.generate_hash()
            return

        # update block transaction
        utxo_list = []
        for block in blockchain.chain:
            if 'list' in str(type(block['transactions'])):
                continue
            transactions = json.loads(block['transactions'])
            for tx in transactions:
                if 'list' in str(type(tx['tx_outputs'])):
                    tx_outs = tx['tx_outputs']
                else:
                    tx_outs = json.loads(tx['tx_outputs'])
                for i in range(len(tx_outs)):
                    output = tx_outs[i]
                    if sender_address == output['to']:
                        utxo_list.append(
                            {
                                'hash': tx['hash'],
                                'index': i,
                                'to': output['to'],
                                'amount': output['amount']
                            }
                        )

                tx_inputs = json.loads(tx['tx_inputs'])
                for i in range(len(tx_inputs)):
                    input = tx_inputs[i]
                    for utxo in utxo_list:
                        condition = input['hash'] == utxo['hash'] and input['idx'] == utxo['index'] \
                            and input['address'] == utxo['to'] and input['amount'] == utxo['amount']
                        if condition:
                            index = utxo_list.index(utxo)
                            del utxo_list[index]

        # update blockchain transaction
        for tx in blockchain.transaction_list:
            if 'list' in str(type(tx['tx_inputs'])):
                tx_inputs = tx['tx_inputs']
            else:
                tx_inputs = json.loads(tx['tx_inputs'])
            for i in range(len(tx_inputs)):
                input = tx_inputs[i]
                for utxo in utxo_list:
                    condition = input['hash'] == utxo['hash'] and input['idx'] == utxo['index'] \
                                and input['address'] == utxo['to'] and input['amount'] == utxo['amount']
                    if condition:
                        index = utxo_list.index(utxo)
                        del utxo_list[index]

        total_utxo_amount = 0
        i = 0
        for utxo in utxo_list:
            total_utxo_amount += utxo['amount']
            i += 1
            if total_utxo_amount >= amount:
                utxo_list = utxo_list[:i]
                break

        if total_utxo_amount < amount:
            raise Exception("잔액 부족")

        for utxo in utxo_list:
            self.tx_inputs.append(json.loads(str(TxIn(utxo))))

        self.vin_size = len(self.tx_inputs)
        # 전자서명
        self.sign(sender_private_key)

        if total_utxo_amount == amount:
            self.tx_outputs.append(json.loads(str(TxOut(receiver_address, amount))))
        else:
            self.tx_outputs.append(json.loads(str(TxOut(receiver_address, amount))))
            self.tx_outputs.append(json.loads(str(TxOut(sender_address, total_utxo_amount - amount))))

        self.vout_size = len(self.tx_outputs)
        self.generate_hash()

    def generate_hash(self):
        self.hash = hashlib.sha256(str(self).encode()).hexdigest()

    def sign(self, private_key):
        for i in range(len(self.tx_inputs)):
            tx_input = self.tx_inputs[i]
            tx_input['publickey'] = bitcoin.privkey_to_pubkey(private_key)
            msg = bitcoin.sha256(str(tx_input))
            tx_input['sign'] = bitcoin.ecdsa_sign(msg, private_key)

    def __str__(self):
        result = {
            'vin_size': self.vin_size,
            'vout_size': self.vout_size,
            'tx_inputs': json.dumps(self.tx_inputs, sort_keys=False),
            'tx_outputs': json.dumps(self.tx_outputs, sort_keys=False),
            'hash': self.hash,
            'locktime': str(self.locktime),
        }
        return json.dumps(result, sort_keys=False)


