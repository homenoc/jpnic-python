import unittest
from jpnic import base


class TestJPNIC(unittest.TestCase):
    def test_jpnic(self):
        ca_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-cert.pem'
        key_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-prvkey.pem'

        base.init_access(ca_path, cert_path, key_path, "再申請")


if __name__ == "__main__":
    unittest.main()
