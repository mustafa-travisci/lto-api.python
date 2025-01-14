from lto.transactions.lease import Lease
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto
import pytest
from freezegun import freeze_time

class TestLease:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = Lease('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.amount == 10000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
        assert transaction.tx_fee == 100000000


    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Lease('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v2 = {
            "type": 8,
            "version": 2,
            'senderKeyType': 'ed25519',
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1326499200000,
            'height': '',
            'id': '',
            "proofs": ['2rgvnVB6s5yvrUX85S2MkjH19G6p9QpmGAXVKjzkFFbaFE89m4gYa8tZs1ATEEiKQybvgL8wCviY4nHx1bqSw87k']
        }

    expected_v3 = {
            "type": 8,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1326499200000,
            'height': '',
            'id': '',
            "proofs": ['4kuKVaN2HjoYacitKePaThXg4e5vTZBawvateHPfgaEQzueUkJQwZY7F9zP5uogxAb6Pv6bjh92DX9LEnrRW1PV7']
        }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(2, expected_v2), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = Lease('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000)
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected


    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Lease('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000)
        broadcastedTransaction = transaction
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "id": "895ryYABK7KQWLvSbw8o8YSjTTXHCqRJw1yzC63j4Fgk",
            "type" : 8,
            "version": 3,
            "sender" : "3HgqG68qfeVz5dqbyvqnxQceFaH49xmGvUS",
            "amount" : 1,
            "senderKeyType": 'ed25519',
            "senderPublicKey" : "DddGQs63eWAA1G1ZJnJDVSrCpMS97NH4odnggwUV42kE",
            "fee" : 500000000,
            "timestamp" : 1495625418143,
            "proofs" : "2SUmFj4zo7NfZK7Xoqvqh7m7bhzFR8rT7eLtqe9Rrp18ugFH9SSvoTx1BtekWhU7PN1uLrnQCpJdS8JhmcBAjmb9",
            "recipient": "3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb"
        }
        transaction = Lease(amount=1, recipient='3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb').from_data(data)
        crypto.compare_data_transaction(data, transaction)


