#!/usr/local/bin/python3

import urllib.request
from time import ctime

number = []


def download(url, user_agent='wswp', num_retries=2):
    print('Downloading ', url)
    headers ={'User-agent':user_agent}
    request = urllib.request.Request(url,headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.request.URLError as e:
        print('Error', e.reason)
        html = None
        # recursively retry 5xx HTTP errors

        if hasattr(e, 'code') and e.code >= 500 and e.code < 600 :
            if num_retries>0:
                url = url
            else:
                url =  "http://httpstat.us/200"
            print('retry download')
            html = download(url,user_agent,num_retries-1)
    return html


url = input('Please input url :')
html = download(url)
print(html)
