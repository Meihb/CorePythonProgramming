#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
uid = "371001411"

for _ in range(200):
    try:
        url = "http://act.dota2.com.cn/neverlosefaith/share?uid={}&task=zan".format(uid)
        response = requests.get(url)
        print(response.text)
        time.sleep(1)
    except:
        pass

