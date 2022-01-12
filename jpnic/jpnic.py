import ssl
import urllib.parse

from bs4 import BeautifulSoup
import requests

from jpnic import base
from jpnic.base import json_to_req_format, get_value, get_random
from jpnic.exception import InvalidSearchMenuException, InvalidGetDataException, InvalidPostException


class JPNIC:
    def __init__(self):
        self.base_url = ''
        self.ca_path = ''
        self.cert_path = ''
        self.key_path = ''

    def init_access(self, function_name):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        try:
            context.load_verify_locations(self.ca_path)
        except Exception as e:
            print('ca: ', e)
            raise e
        try:
            context.load_cert_chain(self.cert_path, self.key_path)
        except Exception as e:
            raise e

        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        content_type = "application/x-www-form-urlencoded"

        headers = {
            'User-Agent': user_agent,
            'Content-Type': content_type,
            'Host': 'iphostmaster.nic.ad.jp',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
        }

        # cookie
        random_str = get_random(32)
        jar = requests.cookies.RequestsCookieJar()
        jar.set('JSESSIONID', random_str)

        s = requests.Session()
        s.verify = self.ca_path
        s.cert = (self.cert_path, self.key_path)
        s.cookies = jar
        s.headers = headers

        r = s.get(self.base_url + '/jpnic/certmemberlogin.do')
        # auto encode
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # メンテナンスには未対応
        if soup.find('meta')['http-equiv'] != 'Refresh':
            raise InvalidGetDataException("meta")
        login_url = soup.find('meta')['content'].partition('=')[2]

        r = s.get(self.base_url + '/jpnic/' + login_url)
        # auto encode
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.findAll('a'))
        find_menu = soup.find('a', text=function_name)
        if find_menu is None:
            raise InvalidSearchMenuException(function_name)
        menu_url = find_menu['href']
        # return find_menu['href'], s, {'cert': cert, 'cookies': cookies, 'headers': headers}
        return menu_url, s

    def get_ipv4(self, data_filter):
        menu_name = '登録情報検索(IPv4)'
        try:
            menu_url, s = self.init_access(menu_name)
        except Exception as e:
            raise e
        # print(s.headers)
        r = s.get(self.base_url + '/jpnic/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        submit_url = soup.find('form')['action']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']

        json_data = {
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
            'action': '　検索　',
        }

        req_sjis = urllib.parse.urlencode(json_data, encoding='shift-jis')
        r = s.post(
            self.base_url + submit_url,
            data=req_sjis,
        )
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.text)
        # print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.findAll('td', attrs={'class': 'dataRow_mnt04'}))
        count = 0
        all_count = 0
        headers = []
        tables = []
        tmp_row = []

        for i in soup.findAll('td', attrs={'class': 'dataRow_mnt04'}):
            if all_count == 0:
                headers.append(i.text.strip())
            else:
                tmp_row.append(i.text.strip())
            count += 1

            if count == 11:
                count = 0
                if all_count > 0:
                    tables.append(tmp_row)
                    tmp_row = []
                all_count += 1

        return headers, tables

    def get_ipv6(self, data_filter):
        menu_name = '登録情報検索(IPv6)'
        try:
            menu_url, s = self.init_access(menu_name)
        except Exception as e:
            raise e
        r = s.get(self.base_url + '/jpnic/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        submit_url = soup.find('form')['action']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']

        json_data = {
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

        print(self.base_url + submit_url)
        r = s.post(
            self.base_url + submit_url,
            data=json_data,
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
            if all_count == 0:
                headers.append(i.text.strip())
            else:
                tmp_row.append(i.text.strip())

            count += 1
            if count == 9:
                count = 0
                if all_count > 0:
                    tables.append(tmp_row)
                    tmp_row = []
                all_count += 1

        return headers, tables

    def regist_assign_ipv4(self, data):
        # data = json.loads(input)
        menu_name = 'IPv4割り当て報告申請　〜ユーザ用〜'
        try:
            menu_url, s = self.init_access(menu_name)
        except Exception as e:
            raise e
        r = s.get(self.base_url + '/jpnic/' + menu_url)
        # auto encode
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        submit_url = soup.find('form')['action']
        token = soup.find('input', attrs={'name': 'org.apache.struts.taglib.html.TOKEN'})['value']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']
        aplyid = soup.find('input', attrs={'name': 'aplyid'})['value']

        json_data = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'destdisp': dest_disp,
            'aplyid': aplyid,
            'ipaddr': get_value(data.get('ipaddr')),
            'netwrk_nm': get_value(data.get('netwrk_nm')),
            'infra_usr_kind': get_value(data.get('infra_usr_kind')),  # 0: インフラストラクチャ 1: ユーザネットワーク 2: SUBA
            'org_nm_jp': get_value(data.get('org_nm_jp')),
            'org_nm': get_value(data.get('org_nm')),
            'zipcode': get_value(data.get('zipcode')),
            'addr_jp': get_value(data.get('addr_jp')),
            'addr': get_value(data.get('addr')),
            'adm_hdl': get_value(data.get('adm_hdl')),
            'tech_hdl': get_value(data.get('tech_hdl')),
            'nmsrv[0].nmsrv': get_value(data.get('nmsrv[0].nmsrv')),
            'nmsrv[1].nmsrv': get_value(data.get('nmsrv[1].nmsrv')),
            'ntfy_mail': get_value(data.get('ntfy_mail')),
            'plan_data': get_value(data.get('plan_data')),
            'deli_no': get_value(data.get('deli_no')),
            'rtn_date': get_value(data.get('rtn_date')),
            'aply_from_addr': get_value(data.get('aply_from_addr')),
            'aply_from_addr_confirm': get_value(data.get('aply_from_addr_confirm')),
            'action': '申請'
        }

        emp_count = int(get_value(data.get('emp_count')) or 0)
        for cou in range(emp_count):
            # [担当者情報]追加
            json_data['action'] = '[担当者情報]追加'
            req_sjis = urllib.parse.urlencode(json_data, encoding='shift-jis')
            r = s.post(
                self.base_url + submit_url,
                data=req_sjis,
            )

            # auto encode
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')
            submit_url = soup.find('form')['action']
            token = soup.find('input', attrs={'name': 'org.apache.struts.taglib.html.TOKEN'})['value']
            dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']
            aplyid = soup.find('input', attrs={'name': 'aplyid'})['value']

            del json_data['action']

            # kind: group(グループハンドル), person(JPNICハンドル)
            json_data['emp[' + str(cou) + '].kind'] = get_value(data.get('emp[' + str(cou) + '].kind'))
            json_data['emp[' + str(cou) + '].jpnic_hdl'] = get_value(data.get('emp[' + str(cou) + '].jpnic_hdl'))
            json_data['emp[' + str(cou) + '].name_jp'] = get_value(data.get('emp[' + str(cou) + '].name_jp'))
            json_data['emp[' + str(cou) + '].name'] = get_value(data.get('emp[' + str(cou) + '].name'))
            json_data['emp[' + str(cou) + '].email'] = get_value(data.get('emp[' + str(cou) + '].email'))
            json_data['emp[' + str(cou) + '].org_nm_jp'] = get_value(data.get('emp[' + str(cou) + '].org_nm_jp'))
            json_data['emp[' + str(cou) + '].org_nm'] = get_value(data.get('emp[' + str(cou) + '].org_nm'))
            json_data['emp[' + str(cou) + '].zipcode'] = get_value(data.get('emp[' + str(cou) + '].zipcode'))
            json_data['emp[' + str(cou) + '].addr_jp'] = get_value(data.get('emp[' + str(cou) + '].addr_jp'))
            json_data['emp[' + str(cou) + '].addr'] = get_value(data.get('emp[' + str(cou) + '].addr'))
            json_data['emp[' + str(cou) + '].division_jp'] = get_value(data.get('emp[' + str(cou) + '].division_jp'))
            json_data['emp[' + str(cou) + '].division'] = get_value(data.get('emp[' + str(cou) + '].division'))
            json_data['emp[' + str(cou) + '].division_jp'] = get_value(data.get('emp[' + str(cou) + '].division_jp'))
            json_data['emp[' + str(cou) + '].title_jp'] = get_value(data.get('emp[' + str(cou) + '].title_jp'))
            json_data['emp[' + str(cou) + '].title'] = get_value(data.get('emp[' + str(cou) + '].title'))
            json_data['emp[' + str(cou) + '].phone'] = get_value(data.get('emp[' + str(cou) + '].phone'))
            json_data['emp[' + str(cou) + '].fax'] = get_value(data.get('emp[' + str(cou) + '].fax'))
            json_data['emp[' + str(cou) + '].ntfy_mail'] = get_value(data.get('emp[' + str(cou) + '].ntfy_mail'))
            json_data['org.apache.struts.taglib.html.TOKEN'] = token
            json_data['destdisp'] = dest_disp
            json_data['aplyid'] = aplyid
            json_data['action'] = '申請'

        req_sjis = urllib.parse.urlencode(json_data, encoding='shift-jis')
        r = s.post(
            self.base_url + submit_url,
            data=req_sjis,
        )

        # auto encode
        r.encoding = r.apparent_encoding

        err = ''
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.findAll('font', attrs={'color': 'red'}):
            err += item.contents[0].text.strip() + ','
        if err != '':
            raise InvalidPostException(err[:-1])

        submit_url = soup.find('form')['action']
        token = soup.find('input', attrs={'name': 'org.apache.struts.taglib.html.TOKEN'})['value']
        prev_disp_id = soup.find('input', attrs={'name': 'prevDispId'})['value']
        dest_disp = soup.find('input', attrs={'name': 'destdisp'})['value']
        aplyid = soup.find('input', attrs={'name': 'aplyid'})['value']
        json_data = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'prevDispId': prev_disp_id,
            'destdisp': dest_disp,
            'aplyid': aplyid,
            'inputconf': '確認'
        }
        req_sjis = urllib.parse.urlencode(json_data, encoding='shift-jis')
        r = s.post(
            self.base_url + submit_url,
            data=req_sjis,
        )
        # auto encode
        r.encoding = r.apparent_encoding

        soup = BeautifulSoup(r.text, 'html.parser')
        recep_number = ""
        for item in soup.findAll('td'):
            if item.find_previous().text == '受付番号：':
                recep_number = item.text

        return recep_number
