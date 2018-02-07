import os,re

with open('whodata.txt','r') as f:
    for rachline in f:
        print(re.split(r'\s\s+',rachline))


        