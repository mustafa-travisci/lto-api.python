from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Sponsor import Sponsor
import copy
from unittest import mock
from time import time

class TestSponsor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Sponsor('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.txFee == 500000000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'


    def testSignWith(self):
        transaction = Sponsor('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def testToJson(self):
        transaction = Sponsor('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        transaction.timestamp = 1610142631066
        transaction.signWith(self.account)
        expected = {
            "type": 18,
            "version": 1,
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1610142631066,
            "proofs": ['zqoN7PBwnRvYP72csdoszjz11u6HR2ogoomrgF8d7Aky8CR6eqM1PUM36EFnvbrKmpoLccDKmKTw4fX34xSPEvH']
        }
        assert transaction.toJson() == expected

    @mock.patch('PyCLTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Sponsor('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction = Sponsor('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction

    def testFromData(self):
        data = {
            "type": 18,
            "version": 1,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "id": "8S2vD5dGCPhwS8jLzNQpSRYDBGXv6GKq6qT5yXUBWPgb",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610410901000,
            "fee": 500000000,
            "proofs": [
                "QKef6R8LrMBupBF9Ry8zjFTu3mexC55J6XNofDDQEcJnZJsRjZPnAk6Yn2eiHkqqd2uSjB2r58fC8QVLaVegQEz"
            ],
            "height": 1225821
        }
        transaction = Sponsor(data['recipient']).fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)
