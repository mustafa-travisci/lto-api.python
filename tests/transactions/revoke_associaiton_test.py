from lto.transactions.revoke_association import RevokeAssociation
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto
import pytest

class TestRevokeAssociation:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.association_type == 1
        assert transaction.tx_fee == 100000000


    def test_sign_with(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.anchor == '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
            "type": 17,
            "version": 1,
            "sender": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "hash": 'Hjh8aEYykDxvjksNKKM2SSun3nAmXvjg5cT8zqXubqrZPburn9qYebuJ5cFb',
            "associationType": 1,
            "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "fee": 100000000,
            'senderKeyType': 'ed25519',
            "timestamp": 1609773456000,
            "proofs": ['G7JKv9F6jPmSA6netZeSW5BKpmssmD6qLudRh1zt4Ce6T6cW8JBjqEmktyfaA7a6tLTrgdTPrDUwQdX8wMU1eah']
        }

    expected_v3 = {
                "type": 17,
                "version": 3,
                "sender": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                "senderKeyType": "ed25519",
                "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
                "associationType": 1,
                "hash": 'Hjh8aEYykDxvjksNKKM2SSun3nAmXvjg5cT8zqXubqrZPburn9qYebuJ5cFb',
                "timestamp": 1609773456000,
                "fee": 100000000,
                "proofs": ['5CMh979q6R5L5wbxVSdRBQHMNYCD2FTsPocnEmMkuGJnjuvi81nKG9ftpE6dx8KdPfHszv3hPyz4wKqizRwEKiZa']
            }



    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        transaction.timestamp = 1609773456000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        broadcastedTransaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction


    def test_from_data(self):
        data = {
            "type": 16,
            "version": 1,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "associationType": 1,
            "hash": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "fee": 100000000,
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = RevokeAssociation(recipient='', association_type='').from_data(data)
        crypto.compare_data_transaction(data, transaction)
