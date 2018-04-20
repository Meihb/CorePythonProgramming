import requests
from bs4 import BeautifulSoup  # 安装bs4,lxml
import telnetlib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}
url = 'http://www.xicidaili.com/wn/'  # 代理网站
success_ip_list = []


def get_ip_list(url, headers):
    """ 从代理网站上获取代理"""
    ip_list = []
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr', limit=22)
    for i in range(1, len(ul_list)):
        line = ul_list[i].find_all('td')
        ip = line[1].text
        port = line[2].text
        address = ip + ':' + port
        ip_list.append(address)
    return ip_list


def get_proxy(aip):
    """构建格式化的单个proxies"""
    proxy_ip = 'http://' + aip
    proxy_ips = 'https://' + aip
    proxy = {'https': proxy_ips, 'http': proxy_ip}
    return proxy


def test_connect_ip(proxies):
    """利用http://www.whatismyip.com.tw/显示访问的ip"""
    # cookies = {
    #     'sc_is_visitor_unique': 'rx6392240.1508897278.298AFF0AE2624F7BC72BADF517B67AEE.2.2.2.2.2.2.1.1.1',
    # }

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }
    url = 'http://www.whatismyip.com.tw/'
    global  success_ip_list
    try:
        page = requests.get(url, headers=headers, proxies=proxies)
        # hd, port = proxies.split(':')
        # telnetlib.Telnet(hd, port=port, timeout=20)
    except:
        print('fail to connect to ' + str(proxies))
    else:
        print('成功连接' + str(proxies))
        success_ip_list.append(get_proxy(proxies))


# def get_result_proxy():
#     proxy_list = get_ip_list(url, headers)
#     print('待测试列表为' + proxy_list.__str__())
#     for proxies in proxy_list:
#         test_connect_ip(proxies)
#     # print('result is ' + success_ip_list.__str__())
#     if (len(success_ip_list) == 0):
#         get_result_proxy()
#     return success_ip_list

def  get_result_proxy():
    ip_list = ['113.121.243.153:47386',
               '175.167.60.70:36805',
               '180.122.148.211:43635','49.81.81.254:32545','116.54.77.254:38759']
    for proxies in ip_list:

        success_ip_list.append(get_proxy(proxies))
    return success_ip_list

if __name__=='__main__':
    get_result_proxy()
    print(success_ip_list.__str__())
