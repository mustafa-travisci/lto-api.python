import base58
import struct
import PyCLTO
from PyCLTO import crypto
from PyCLTO.Transaction import Transaction


class Transfer(Transaction):
    TYPE = 4
    DEFAULT_TX_FEE = 100000000
    defaultVersion = 3

    def __init__(self, recipient, amount, attachment=''):
        super().__init__()
        self.recipient = recipient
        PyCLTO.crypto.validateAddress(recipient)
        self.amount = amount
        self.attachment = attachment
        self.version = self.defaultVersion

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        self.txFee = self.DEFAULT_TX_FEE

    def __toBinaryV2(self):
        return (b'\4' +
                b'\2' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.txFee) +
                base58.b58decode(self.recipient) +
                struct.pack(">H", len(self.attachment)) +
                PyCLTO.crypto.str2bytes(self.attachment))

    def __toBinaryV3(self):
        return (b'\4' +
                b'\3' +
                crypto.str2bytes(self.chainId) +
                struct.pack(">Q", self.timestamp) +
                b'\1' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">Q", self.txFee) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def toBinary(self):
        if self.version == 2:
            return self.__toBinaryV2()
        elif self.version == 3:
            return self.__toBinaryV3()
        else:
            raise Exception('Incorrect Version')

    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": "ed25519",
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "amount": self.amount,
            "recipient": self.recipient,
            "attachment": base58.b58encode(PyCLTO.crypto.str2bytes(self.attachment)),
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = Transfer(data['recipient'], data['amount'], data['attachment'])
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        # it is not possible to obtain the senderAddress without the chainId + publicKey
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.amount = data['amount']
        tx.recipient = data['recipient']
        tx.attachment = data['attachment'] if 'attachment' in data else ''
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''

        if 'sponsorPublicKey' in data:
            tx.sponsor = data['sponsor']
            tx.sponsorPublicKey = data['sponsorPublicKey']

        return tx