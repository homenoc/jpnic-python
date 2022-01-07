from bs4 import BeautifulSoup
from jpnic import base


class JPNIC:
    def __init__(self):
        self.base_url = ''
        self.ca_path = ''
        self.cert_path = ''
        self.key_path = ''

    def get_ipv4(self, data_filter):
        menu_name = '登録情報検索(IPv4)'
        try:
            menu_url, s = base.init_access(self.base_url, self.ca_path, self.cert_path, self.key_path, menu_name)
        except Exception as e:
            raise e
        r = s.get(self.base_url + '/jpnic/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        submit_url = soup.find('form')['action']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']

        json = {
            'org.apache.struts.taglib.html.TOKEN': base.get_random(32),
            'destdisp': dest_disp,
            'ipaddr': data_filter['ip_address'],  # IPアドレス
            'sizeS': data_filter['size_start'],  # サイズ (開始)
            'sizeE': data_filter['size_end'],  # サイズ (終了)
            'netwrkName': data_filter['network_name'],  # ネットワーク名
            'regDateS': data_filter['reg_start'],  # 割振・割当年月日(開始)
            'regDateE': data_filter['reg_end'],  # 割振・割当年月日(終了)
            'rtnDateS': data_filter['return_start'],  # 返却年月日(開始)
            'rtnDateE': data_filter['return_end'],  # 返却年月日(終了)
            'organizationName': data_filter['org_name'],  # 組織名
            'resceAdmSnm': data_filter['resource_admin_short'],  # 資源管理者略称
            'recepNo': data_filter['recep_number'],  # 受付番号
            'deliNo': data_filter['deli_number'],  # 審議番号
            'ipaddrKindPa': data_filter['is_pa'],  # PA
            'regKindAllo': data_filter['is_allocate'],  # 割り振り
            'regKindEvent': data_filter['is_assign_infra'],  # インフラ割当
            'regKindUser': data_filter['is_assign_user'],  # ユーザ割当
            'regKindSubA': data_filter['is_sub_allocate'],  # SUBA
            'ipaddrKindPiHistorical': data_filter['is_historical_pi'],  # 歴史的PI
            'ipaddrKindPiSpecial': data_filter['is_special_pi'],  # 特殊用途PI
            'action': '%81%40%8C%9F%8D%F5%81%40',
        }

        print(self.base_url + '/' + submit_url)
        r = s.post(
            self.base_url + submit_url,
            data=json,
        )
        # auto encode
        r.encoding = r.apparent_encoding
        # print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.findAll('td', attrs={'class': 'dataRow_mnt04'}))
        count = 0
        all_count = 0
        headers = []
        tables = []
        tmp_row = []

        for i in soup.findAll('td', attrs={'class': 'dataRow_mnt04'}):
            if count == 11:
                count = 0
                if all_count > 0:
                    tables.append(tmp_row)
                    tmp_row = []
                all_count += 1

            if all_count == 0:
                headers.append(i.text.strip())
            else:
                tmp_row.append(i.text.strip())

            count += 1

        return headers, tables

    def get_ipv6(self, data_filter):
        menu_name = '登録情報検索(IPv6)'
        try:
            menu_url, s = base.init_access(self.base_url, self.ca_path, self.cert_path, self.key_path, menu_name)
        except Exception as e:
            raise e
        r = s.get(self.base_url + '/jpnic/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        submit_url = soup.find('form')['action']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']

        json = {
            'org.apache.struts.taglib.html.TOKEN': base.get_random(32),
            'destdisp': dest_disp,
            'ipaddr': data_filter['ip_address'],  # IPアドレス
            'sizeS': data_filter['size_start'],  # サイズ (開始)
            'sizeE': data_filter['size_end'],  # サイズ (終了)
            'netwrkName': data_filter['network_name'],  # ネットワーク名
            'regDateS': data_filter['reg_start'],  # 割振・割当年月日(開始)
            'regDateE': data_filter['reg_end'],  # 割振・割当年月日(終了)
            'rtnDateS': data_filter['return_start'],  # 返却年月日(開始)
            'rtnDateE': data_filter['return_end'],  # 返却年月日(終了)
            'organizationName': data_filter['org_name'],  # 組織名
            'resceAdmSnm': data_filter['resource_admin_short'],  # 資源管理者略称
            'recepNo': data_filter['recep_number'],  # 受付番号
            'deliNo': data_filter['deli_number'],  # 審議番号
            'regKindAllo': data_filter['is_allocate'],  # 割り振り
            'regKindEvent': data_filter['is_assign_infra'],  # インフラ割当
            'regKindUser': data_filter['is_assign_user'],  # ユーザ割当
            'regKindSubA': data_filter['is_sub_allocate'],  # SUBA
            'action': '%81%40%8C%9F%8D%F5%81%40',
        }

        print(self.base_url + '/' + submit_url)
        r = s.post(
            self.base_url + submit_url,
            data=json,
        )
        # auto encode
        r.encoding = r.apparent_encoding
        # print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.findAll('td', attrs={'class': 'dataRow_mnt04'}))
        count, all_count = 0, 0
        all_count = 0
        headers = []
        tables = []
        tmp_row = []

        for i in soup.findAll('td', attrs={'class': 'dataRow_mnt04'}):
            if count == 9:
                count = 0
                if all_count > 0:
                    tables.append(tmp_row)
                    tmp_row = []
                all_count += 1

            if all_count == 0:
                headers.append(i.text.strip())
            else:
                tmp_row.append(i.text.strip())

            count += 1

        return headers, tables
