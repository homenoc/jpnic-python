import unittest
from jpnic import base
from jpnic.jpnic import JPNIC
from tabulate import tabulate


class TestJPNIC(unittest.TestCase):
    def login(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-cert.pem'
        key_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-prvkey.pem'

        menu_url, s = base.init_access(base_url, ca_path, cert_path, key_path, "再申請")
        r = s.get(base_url + '/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        print(r.text)

    def get_ipv4(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-cert.pem'
        key_path = '/Users/y-yoneda/github/homenoc/jpnic-python/cert/v4-prvkey.pem'
        j = JPNIC()
        j.base_url = base_url
        j.ca_path = ca_path
        j.cert_path = cert_path
        j.key_path = key_path

        data_filter = {
            'ip_address': '',
            'size_start': '',
            'size_end': '',
            'network_name': '',
            'reg_start': '',
            'reg_end': '',
            'return_start': '',
            'return_end': '',
            'org_name': '',
            'resource_admin_short': 'SAKURA',
            'recep_number': '',
            'deli_number': '',
            'is_pa': 'on',  # PA
            'is_assign': 'on',  # 割り振り
            'is_allocate_infra': 'on',  # インフラ割当
            'is_allocate_user': 'on',  # ユーザ割当
            'is_suba': 'on',  # SUBA
            'is_historical_pi': 'on',  # 歴史的PI
            'is_special_pi': 'on',  # 特殊用途PI
        }

        headers, table = j.get_ipv4(data_filter)
        result = tabulate(table, headers, tablefmt="grid")
        print(result)


if __name__ == "__main__":
    unittest.main()
