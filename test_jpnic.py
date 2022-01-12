import json
import unittest
from jpnic import base
from jpnic.jpnic import JPNIC
from tabulate import tabulate


class TestJPNIC(unittest.TestCase):
    def login(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/Documents/doornoc-cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/Documents/doornoc-cert/v4-cert.pem'
        key_path = '/Users/y-yoneda/Documents/doornoc-cert/v4-prvkey.pem'
        j = JPNIC()
        j.base_url = base_url
        j.ca_path = ca_path
        j.cert_path = cert_path
        j.key_path = key_path

        menu_url, s = j.init_access()
        r = s.get(base_url + '/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        print(r.text)

    def get_ipv4(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/Documents/doornoc-cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/Documents/doornoc-cert/v4/v4-cert.pem'
        key_path = '/Users/y-yoneda/Documents/doornoc-cert/v4/v4-prvkey.pem'
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
            'resource_admin_short': 'doornoc',
            'recep_number': '',
            'deli_number': '',
            'is_pa': 'off',  # PA
            'is_allocate': 'on',  # 割り振り
            'is_assign_infra': 'on',  # インフラ割当
            'is_assign_user': 'on',  # ユーザ割当
            'is_sub_allocate': 'on',  # SUBA
            'is_historical_pi': 'on',  # 歴史的PI
            'is_special_pi': 'on',  # 特殊用途PI
        }

        headers, table = j.get_ipv4(data_filter)
        result = tabulate(table, headers, tablefmt="grid")
        print(result)

    def get_ipv6(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/Documents/doornoc-cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/Documents/doornoc-cert/v6-cert.pem'
        key_path = '/Users/y-yoneda/Documents/doornoc-cert/v6-prvkey.pem'
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
            'resource_admin_short': 'doornoc',
            'recep_number': '',
            'deli_number': '',
            'is_allocate': 'on',  # 割振
            'is_assign_infra': 'on',  # インフラ割当
            'is_assign_user': 'on',  # ユーザ割当
            'is_sub_allocate': 'on',  # 再割当
        }

        headers, table = j.get_ipv6(data_filter)
        result = tabulate(table, headers, tablefmt="grid")
        print(result)

    def regist_assign_ipv4(self):
        base_url = 'https://iphostmaster.nic.ad.jp'
        ca_path = '/Users/y-yoneda/Documents/doornoc-cert/rootcacert_r3.cer'
        cert_path = '/Users/y-yoneda/Documents/doornoc-cert/v4-cert.pem'
        key_path = '/Users/y-yoneda/Documents/doornoc-cert/v4-prvkey.pem'
        j = JPNIC()
        j.base_url = base_url
        j.ca_path = ca_path
        j.cert_path = cert_path
        j.key_path = key_path

        json_open = open('./test-regist.json', 'r')
        data = json.load(json_open)

        recep_number = j.regist_assign_ipv4(data)
        print('受付番号: ' + recep_number)


if __name__ == "__main__":
    unittest.main()
