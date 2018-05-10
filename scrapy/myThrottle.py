#!/user/bin/python3
import urllib.parse
import time


class Throttle():
    '''
    add a delay between downloads to the same domain
    '''

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        # print(domain.netloc)
        print(self.domains)
        if self.domains.get(domain):
            last_access_interval = self.delay-(time.time() - self.domains.get(domain) )
            print(last_access_interval)
            if last_access_interval > 0:
                print('sleep for %ss' % (last_access_interval))
                time.sleep(int(last_access_interval))
        else:
            pass
        self.domains[domain] = time.time()


if __name__ == '__main__':
    myThrottle = Throttle(2)
    myThrottle.wait('http://www.baidu.com')
    myThrottle.wait('http://www.baidu.com')
