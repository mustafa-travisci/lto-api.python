import requests



class PublicNode(object):
    def __init__(self, url):
        self.url = url

        ''' is the offline important? it should be imported from the init.py'''
        self.OFFLINE = False  # this comes from the __init__


    def wrapper(self, api, postData='', host='', headers=''):
        # global OFFLINE
        if self.OFFLINE:
            offlineTx = {}
            offlineTx['api-type'] = 'POST' if postData else 'GET'
            offlineTx['api-endpoint'] = api
            offlineTx['api-data'] = postData
            return offlineTx
        if not host:
            host = self.url
        if postData:
            req = requests.post('%s%s' % (host, api), data=postData,
                                headers={'content-type': 'application/json'}).json()
        else:
            req = requests.get('%s%s' % (host, api), headers=headers).json()
        return req

    def height(self):
        return self.wrapper('/blocks/height')['height']

    def lastblock(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        return self.wrapper('/transactions/info/%s' % id)

    def balanceOriginal(self, address, confirmations=0):
        try:
            return self.wrapper(
                '/addresses/balance/%s%s' % (address, '' if confirmations == 0 else '/%d' % confirmations))[
                'balance']
        except:
            return -1

    def balance(self, address):
        try:
            return self.wrapper('/addresses/balance/%s' % str(address))
        except:
            return -1

    def transactions(self, limit=100, after=''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            self.address, limit, "" if after == "" else "?after={}".format(after)))

# url = 'https://testnet.lto.network'
# node = PublicNode(url)
# node.tx('T')
