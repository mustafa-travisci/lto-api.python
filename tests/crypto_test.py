from lto import crypto
import pytest

class TestCrypto:

    def testConversion(self):
        assert crypto.str2bytes('test') == b'test'
        assert crypto.bytes2str(b'test') == 'test'
        assert crypto.str2list('test') == ['t', 'e', 's', 't']


    def testsha256(self):
        assert crypto.sha256('test') == b'\x9f\x86\xd0\x81\x88L}e\x9a/\xea\xa0\xc5Z\xd0\x15\xa3\xbfO\x1b+\x0b\x82,\xd1]l\x15\xb0\xf0\n\x08'

    def testhash_chain(self):
        assert crypto.hash_chain(crypto.str2bytes('T©È T\÷?<ÑÙ½êYV¤u< '))[0:4] == 'Z*gó'

    def testGetNetwok(self):
        assert crypto.get_network('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj') == 'T'

    def testEncode(self):
        assert crypto.encode(b'hello', 'base58') == 'Cn8eVZg'
        assert crypto.encode(b'hello', 'base64') == b'aGVsbG8='
        assert crypto.encode(b'hello', 'hex') == "68656c6c6f"

        with pytest.raises(Exception):
            crypto.encode(b'hello', 'test')


    def testDecode(self):
        assert crypto.decode('Cn8eVZg', 'base58') == b'hello'
        assert crypto.decode(b'aGVsbG8=', 'base64') == b'hello'
        # assert crypto.decode('0x8004823121A', 'hex') == b'fr5A4EA4C'
        with pytest.raises(Exception):
            crypto.decode(b'hello', 'test')

    def testvalidate_address(self):
        assert crypto.validate_address('3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du') is True
        with pytest.raises(Exception):
            crypto.validate_address('1N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du')
        with pytest.raises(Exception):
            crypto.validate_address('')