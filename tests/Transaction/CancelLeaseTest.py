from PyCLTO.Transactions.CancelLease import CancelLease
from PyCLTO.AccountFactory import AccountFactory
from time import time
from unittest import mock

class TestCancelLease:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        assert transaction.leaseId == 'B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo'
        assert transaction.txFee == 500000000


    def testSignWith(self):
        transaction = CancelLease('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def expectedV1(self):
        return {
            "type": 9,
            "version": 1,
            'txId': 'B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "proofs": ['373CZ9HNU8Hr3CGVxVPuDxAvAxVp2FsDHUYetEAShbPgeewQPdRsk38TXPkvrMJNWhYWGD7AH4HvwtUoaH8oGDrd']
        }

    def expectedV3(self):
        return {
            "type": 9,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "proofs": ['3yTbYErRRXZUp1S4TPpXS4sNNuCFi7goyP5ZMJq64sExhAbBbhqfAb6zrZea1UNGsjfTbsjmMjGfyDVaAqRai7US'],
            "leaseId": "B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo"
        }

    def testToJson(self):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)

        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('PyCLTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        broadcastedTransaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction


    def testFromData(self):
        data = {
            "type": 9,
            "version": 3,
            "id": "BLMA4vkfe2S5UFHnoPyTh8SJmpTA1deh5SnWk1bdfjhq",
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": 'ed25519',
            "senderPublicKey": "4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz",
            "timestamp": 1519862400,
            "fee": 500000000,
            "leaseId": "B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo",
            "proofs": [
                "2AKUBja93hF8AC2ee21m9AtedomXZNQG5J3FZMU85avjKF9B8CL45RWyXkXEeYb13r1AhpSzRvcudye39xggtDHv"
            ]
        }
        transaction = CancelLease(leaseId='').fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)



