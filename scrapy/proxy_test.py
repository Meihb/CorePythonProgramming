from urllib import request

if __name__ == "__main__":
    #访问网址
    url = 'http://122.112.248.56/showremoteAddr.php'
    url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=0&oid=10120347&pn=1'
    #这是代理IP
    proxy ={'https': 'https://113.121.243.153:47386', 'http': 'http://113.121.243.153:47386'}

    # proxy=None
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    # opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    #使用自己安装好的Opener
    response = request.urlopen(url)
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    #打印信息
    print(html)