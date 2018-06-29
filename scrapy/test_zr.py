import  requests

r = requests.get('http://sh.ziroom.com/detail/info?id=60934745&house_id=60150379')
print(r.status_code)