import ssl
import string
import random
import requests
from bs4 import BeautifulSoup
from jpnic.exception import InvalidGetDataException, InvalidSearchMenuException


def init_access(base_url, ca_path, cert_path, key_path, function_name):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    try:
        context.load_verify_locations(ca_path)
    except Exception as e:
        print('ca: ', e)
        raise e
    try:
        context.load_cert_chain(cert_path, key_path)
    except Exception as e:
        raise e

    # cookie
    random_str = get_random(32)
    cookies = dict(JSESSIONID=random_str)

    s = requests.Session()
    cert = (cert_path, key_path)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
    }

    r = s.get(base_url + '/jpnic/certmemberlogin.do', verify=ca_path, cert=cert, cookies=cookies, headers=headers)
    # auto encode
    r.encoding = r.apparent_encoding
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    # メンテナンスには未対応
    if soup.find('meta')['http-equiv'] != 'Refresh':
        return 'redirect error', '', ''
    login_url = soup.find('meta')['content'].partition('=')[2]

    r = s.get(base_url + '/jpnic/' + login_url, verify=ca_path, cert=cert, cookies=cookies, headers=headers)
    # auto encode
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')

    find_menu = soup.find('a', text=function_name)
    if find_menu is None:
        raise InvalidSearchMenuException(function_name)

    # return find_menu['href'], s, {'cert': cert, 'cookies': cookies, 'headers': headers}
    return find_menu['href'], s


def get_random(n):
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join([random.choice(dat) for i in range(n)])

# if __name__ == '__main__':
#     init_access()
