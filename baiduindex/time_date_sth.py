import time, datetime


# 列表生成器创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。


def baidu_index_datetime(enddate):
    enddate_timestamp = int(time.mktime(time.strptime(enddate, '%Y-%m-%d')))
    print(enddate_timestamp)
    i = 1
    start = '2011-01-01'
    while True:
        currentenddate_timestamp = int(time.mktime(time.strptime(start, '%Y-%m-%d')))
        if enddate_timestamp >= currentenddate_timestamp + 13 * 24 * 4600:
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


def baidu_index_date_generator(begin, end):
    endtimestamp = time.mktime(time.strptime(end, '%Y-%m-%d'))
    while True:
        temp_end = get_weekday(6, begin)
        if (time.mktime(time.strptime(temp_end, '%Y-%m-%d'))) > endtimestamp:  # 计算日期段结尾已超过deadline,结算按照deadline计算,并退出循环
            yield {'start': begin, 'end': end}
            break
        else:
            yield {'start': begin, 'end': temp_end}
            begin = time_intverl(temp_end, 24 * 3600)


def baidu_index_date_generator_v2(begin, end):
    begin_timestamp = time.mktime(time.strptime(begin, '%Y-%m-%d'))
    end_timestamp = time.mktime(time.strptime(end, '%Y-%m-%d'))

    duration = int((end_timestamp - begin_timestamp) / (3600 * 24))  # 天数
    print(duration)


def test_time():
    print(type(time.strftime('%Y-%m-%d')))
    print(type(datetime.date.today()))
    # time.strftime()和datetime.date.today() 的返回结果不同,前者是字符串,后者是 object
    enddate = '2018-05-23'
    timearray = time.strptime(enddate, '%Y-%m-%d')
    print(
        timearray)  # time.struct_time(tm_year=2018, tm_mon=5, tm_mday=23, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=143, tm_isdst=-1)
    timestamp = time.mktime(timearray)
    print(int(timestamp))  # 1527004800
    timelocal = time.localtime(timestamp + 7 * 24 * 3600)
    print(
        timelocal)  # time.struct_time(tm_year=2018, tm_mon=5, tm_mday=30, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=150, tm_isdst=0)
    new_date = time.strftime('%Y-%m-%d', timelocal)
    print(new_date)  # 2018-05-30


def time_intverl(start, interval):
    return time.strftime('%Y-%m-%d', time.localtime(time.mktime(time.strptime(start, '%Y-%m-%d')) + int(interval)))


'''获取指定日期之后第一个指定周天(1-7分指周一至周日)'''


def get_weekday(weekday, offsetdate='2011-01-01'):
    timestamp = time.mktime(time.strptime(offsetdate, '%Y-%m-%d'))
    offsetdate = datetime.date.fromtimestamp(timestamp)
    return time.strftime("%Y-%m-%d", time.localtime((weekday - offsetdate.isoweekday()) % 7 * 3600 * 24 + timestamp))


# 日期比较大小
def date_comparision(date1, date2, mode=1):
    date1_timestamp = int(time.mktime(time.strptime(date1, '%Y-%m-%d')))
    date2_timestamp = int(time.mktime(time.strptime(date2, '%Y-%m-%d')))
    if (max(date1_timestamp, date2_timestamp) == date1_timestamp):
        max_date = date1
        min_date = date2
    else:
        max_date = date2
        min_date = date1
    if mode == 1:  # 比较较大值
        return max_date
    else:
        return min_date


def get_row_date():
    global baidu_generator
    try:
        row_date = next(baidu_generator)
    except StopIteration:
        baidu_generator = baidu_index_date_generator('2011-01-01', time_intverl(time.strftime('%Y-%m-%d'), -24 * 3600))
        row_date = next(baidu_generator)
    return row_date


def split_date(start, end):
    '''
    限制start>=pc_start,end<=yesterday,且end>=start
    共四种情况
      start                                                        end                                                                              result
    pc_start<=start<all-start                pc_start<end<all_start                             start-end   +[]
                                                                    all_start<end                                                     start-pc_end + all_start-end
    start>=all_start                            all_start<end                                                           []                     +  start-end
    :param start >2006-06-01:
    :param end:
    :return:
    '''
    # pc_start = '2006-06-01'
    pc_end = '2010-12-31'
    all_start = '2011-01-01'

    pc_result = []
    all_result = []
    if date_comparision(all_start, start) == all_start:  # 起始时间低于all_start
        pc_result.append(start)
        if date_comparision(end, all_start) == all_start:#结束时间同样低于all_start
            pc_result.append(end)
        else:#结束时间高于all_start
            pc_result.append(pc_end)
            all_result.append(all_start)
            all_result.append(end)
    else:#起始时间高于all_start
        all_result.append(start)
        all_result.append(end)
    return pc_result, all_result


def date_duration(date1,date2):
    date1_timestamp = time.mktime(time.strptime(date1,'%Y-%m-%d'))
    date2_timestamp = time.mktime(time.strptime(date2,'%Y-%m-%d'))

    return int((date2_timestamp-date1_timestamp)/(3600*24))

# 每日跨度
def enddate_generator(period_begin, period_end, step=24 * 3600 * 360):
    temp_startdate = period_begin
    while True:
        temp_enddate = time_intverl(temp_startdate, step)
        # print(temp_enddate,start_date)
        if date_comparision(period_end, temp_enddate) == period_end:  # 未到时间の尽头
            yield temp_startdate, temp_enddate
            temp_startdate = time_intverl(temp_enddate, 24 * 3600)
        else:  # now we are ONE!
            yield temp_startdate, period_end
            break

if __name__ == '__main__':
    # y = baidu_index_datetime('2018-05-22')
    # print(time.strftime("%Y-%m-%d",time.localtime(int(time.time())-24*3600)))
    # baidu_generator = baidu_index_date_generator('2011-01-01', '2012-01-03')
    # i = 0
    # while i < 484:
    #     print(get_row_date())
    #     i += 1

    # print(get_weekday(6))
    # test_time()
    # print(time_intverl(time.strftime('%Y-%m-%d'),-24*3600))
    # start = '2011-02-03'
    # end = '2012-02-01'
    # baidu_index_date_generator_v2(start,end)
    import myBaiduIndex

    # print(time_intverl('2006-06-01', 24 * 3600 * 625))
    # print(date_duration('2006-06-01','2018-05-31'))

    g = enddate_generator('2006-06-01','2010-12-31')


    while True:
        try:
            info = next(g)
            print(info)
        except StopIteration:
            print('end')
            break
