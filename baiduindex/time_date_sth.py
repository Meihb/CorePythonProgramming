import  time,datetime
#列表生成器创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。


def baidu_index_datetime(enddate):
    enddate_timestamp = int(time.mktime(time.strptime(enddate,'%Y-%m-%d')))
    print(enddate_timestamp)
    i = 1
    start  = '2011-01-01'
    while True:
        currentenddate_timestamp = int(time.mktime(time.strptime(start, '%Y-%m-%d')))
        if  enddate_timestamp>=currentenddate_timestamp+13*24*4600:
            if i == 1:
                yield {'start': start, 'end': start}
                start = time_intverl(start, 24 * 3600)  #
            else:
                yield {'start': start, 'end': time_intverl(start, 6 * 24 * 3600)}
                start = time_intverl(start, 7 * 24 * 3600)  #
            i += 1
        else:
            break
    # while enddate_timestamp>=currentenddate_timestamp+13*24*4600:#以获取的日期范围尾部距离核定结尾超过一周,则仍有计算方式
    #     if i==1:
    #         yield {'start': start, 'end': start}
    #         start = time_intverl(start,24*3600)#
    #     else:
    #         yield {'start':start,'end':time_intverl(start,6*24*3600)}
    #         start = time_intverl(start,7*24*3600)#
    #     i+=1
    # return True

def test_time():
    enddate = '2018-05-23'
    timearray = time.strptime(enddate, '%Y-%m-%d')
    print(timearray)
    timestamp = time.mktime(timearray)
    print(int(timestamp))
    timelocal = time.localtime(timestamp + 7 * 24 * 3600)
    print(timelocal)
    new_date = time.strftime('%Y-%m-%d', timelocal)
    print(new_date)

def time_intverl(start,interval):
    return time.strftime('%Y-%m-%d',time.localtime(time.mktime(time.strptime(start,'%Y-%m-%d'))+int(interval)))

'''获取指定日期之后第一个指定周天(1-7分指周一至周日)'''
def get_weekday(weekday,offsetdate = '2011-01-01'):
    timestamp = time.mktime(time.strptime(offsetdate,'%Y-%m-%d'))
    offsetdate = datetime.date.fromtimestamp(timestamp)
    return time.strftime("%Y-%m-%d",time.localtime((weekday-offsetdate.isoweekday())%7*3600*24+timestamp))

if __name__=='__main__':
    # y = baidu_index_datetime('2018-05-22')
    # i=0
    # while i<388:
    #     try:
    #         print(next(y))
    #         i += 1
    #     except StopIteration:
    #         pass
    print(get_weekday(7))
