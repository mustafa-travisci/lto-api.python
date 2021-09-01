from __future__ import absolute_import, division, print_function, unicode_literals

from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.PublicNode import PublicNode
from PyCLTO.Account import Account
from PyCLTO.coin import pyLTOCoin
from PyCLTO.Transactions import Transfer
from PyCLTO.Transactions.Anchor import Anchor
from PyCLTO.Transactions.Lease import Lease
from PyCLTO.Transactions.Association import Association
from PyCLTO.Transactions.CancelLease import CancelLease
from PyCLTO.Transactions.CancelSponsor import CancelSponsor
from PyCLTO.Transactions.MassTransferLto import MassTransferLTO
from PyCLTO.Transactions.RevokeAssociation import RevokeAssociation
from PyCLTO.Transactions.SetScript import SetScript
from PyCLTO.Transactions.Sponsor import Sponsor



class PyCLTO:

    def __init__(self, chainId='T'):
        self.accountFactory = AccountFactory(chainId)

        if chainId == 'T':
            self.NODE = PublicNode('https://testnet.lto.network')
            self.CHAIN = 'testnet'
            self.CHAIN_ID = 'T'
        elif chainId == 'L':
            self.NODE = PublicNode('https://nodes.lto.network')
            self.CHAIN = 'mainnet'
            self.CHAIN_ID = 'L'
        else:
            self.NODE = ''

        # is this necessary ?
        self.LTO = pyLTOCoin(self)

    def Account(self, address='', publicKey='', privateKey='', seed='', nonce=0):

        if seed:
            account = self.accountFactory.createFromSeed(seed, nonce)
        elif privateKey:
            account = self.accountFactory.createFromPrivateKey(privateKey)
        elif publicKey:
            account = self.accountFactory.createFromPublicKey(publicKey)
        else:
            account = self.accountFactory.create()

        # We don't have a case for someone who just passes the address
        if not self.accountFactory.assertAccount(account, address, publicKey, privateKey, seed):
            raise Exception("Account info are inconsistent")
        return account

    def getChainId(self):
        return self.accountFactory.chainId

    def fromData(self, data):

        if data['type'] == 4:
            return Transfer(recipient=data['recipient'], amount=data['amount']).fromData(data)
        elif data['type'] == 8:
            return Lease(amount=1, recipient='').fromData(data)
        elif data['type'] == 11:
            return MassTransferLTO(transfers='').fromData(data)
        elif data['type'] == 15:
            return Anchor(anchor='').fromData(data)
        elif data['type'] == 16:
            return Association(party='', associationType='').fromData(data)
        elif data['type'] == 17:
            return RevokeAssociation(party='', associationType='').fromData(data)
        elif data['type'] == 18:
            return Sponsor(data['recipient']).fromData(data)
        elif data['type'] == 19:
            return CancelSponsor(data['recipient']).fromData(data)
        elif data['type'] == 13:
            return SetScript(data['script']).fromData(data)
        elif data['type'] == 9:
            return CancelLease(leaseId='').fromData(data)
        else:
            raise Exception('Incorrect transaction Type')
