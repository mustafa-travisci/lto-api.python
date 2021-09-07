import configparser
import Account
import base58
from nacl.signing import SigningKey, VerifyKey
import os


def writeToFile(fileName: str, account: Account, secName: str):
    config = configparser.ConfigParser()
    config.read(fileName)

    if not secName:
        secName = 'Account_{0}'.format(getAccountNumber(config.sections()))
    elif secName in config.sections():
        raise Exception("Account name already taken")

    config.add_section(secName)
    config.set(secName, 'Address', account.address)
    config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
    config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
    config.set(secName, 'Seed', account.seed)
    config.write(open(fileName, 'w'))

    config.clear()
    if not os.path.exists('default.ini'):
        setDefault('config.ini', secName)
    else:
        config.read('default.ini')
        if 'Default' not in config.sections():
            setDefault('config.ini', secName)





def setDefault(fileName: str, secName: str):
    config = configparser.ConfigParser()
    config.read(fileName)
    address = config.get(secName, 'address')
    publicKey = config.get(secName, 'publickey')
    privateKey = config.get(secName, 'privatekey')
    seed = config.get(secName, 'seed')
    config.clear()
    config.read('default.ini')
    if 'Default' not in config.sections():
        config.add_section('Default')
    config.set('Default', 'Address', address)
    config.set('Default', 'PublicKey', publicKey)
    config.set('Default', 'PrivateKey', privateKey)
    config.set('Default', 'Seed', seed)
    config.write(open('default.ini', 'w'))



def listAccounts(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return (config.sections())


def removeAccount(filename, address):
    config = configparser.ConfigParser()
    config.read(filename)
    config.remove_section(findAccountSection(address, config))
    config.write(open(filename, 'w'))

    # if default account, remove it also from default file
    config.clear()
    config.read('default.ini')
    if config.sections() != []:
        if address == config.get('Default', 'address'):
            os.remove('default.ini')




# it returns the account section name from the addresses provided
def findAccountSection(address, config):
    for sec in config.sections():
        if config.get(sec, 'address') == address:
            return sec
    raise Exception("Option not found")


def getAccountNumber(secNameList):
    x = 0
    flag = True
    while flag:
        flag = False
        for name in secNameList:
            if str(x) in name:
                x += 1
                flag = True
    return x


'''config = configparser.ConfigParser()
config.read('default.ini')
if 'Default' in config.sections():
    print('ciao')
else:
    print('no')
config.set('Default', 'address', 'ciccio')
config.write(open('default.ini', 'w'))
'''


'''config = configparser.ConfigParser()
config.read('default.ini')
print(os.path.exists('default.ini'))
if 'Default' not in config.sections():
    print('Default without default Account')'''
#if not config.sections() == [] or not os.path.exists('default.ini'):
#    setDefault('config.ini', 'Default')
