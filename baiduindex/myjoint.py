import redisConn, myBaiduIndex
import multiprocessing, time, random, pytesseract, os, traceback
from PIL import Image


def _run_proc(i, *args):
    print('pid %s is running' % (os.getpid()))
    print(i)
    # print(random.random())
    time.sleep(random.random() * 3)
    # print(args)


def img_recognition(save_dir, index):
    pytesseract.pytesseract.tesseract_cmd = myBaiduIndex.tesseract_exe
    print('%s\Puzzle%s.png' % (save_dir, index))
    jpgzoom = Image.open(r'%s\Puzzle%s.png' % (save_dir, index))
    jpgzoom.show()
    # print(type(jpgzoom))
    (x, y) = jpgzoom.size
    x_s = 2 * x
    y_s = 2 * y
    out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
    # print(type(out))
    out.show()
    out.save('%s/zoom%s.jpg' % (save_dir, index), quality=95)
    num = pytesseract.image_to_string(out, config="-psm 7")
    # print(num,type(num))
    if num:
        num = num.replace("'", '').replace('.', '').replace(',', '').replace('?', '7').replace("S", '5').replace(" ",
                                                                                                                 "").replace(
            "E", "8").replace("B", "8").replace("I", "1").replace("$", "8")
    else:
        num = ''
    # print(num)
    return num


def single_joint(id):
    cur.execute("SELECT * FROM baidu_index_v2 WHERE id = %s", [id])
    row_info = cur.fetchall()[0]
    margin_left = [int(x) for x in row_info['margin_left'].split(',')]
    width = [int(x) for x in row_info['width'].split(',')]
    location = row_info['location']
    dir = row_info['dir']
    refer_date = row_info['refer_date_begin']
    # print(margin_left,width,location,dir,refer_date)
    file_path = '%s\\Puzzle%s.png' % (dir, refer_date)
    try:
        origin_img = Image.open(location)
        w, h = origin_img.size  # 返回当前图片宽,长元组
        target = Image.new('RGB', (sum(width), h))
        # origin_img.show()
        for i in range(len(width)):
            img_crop = origin_img.crop((margin_left[i], 0, width[i] + margin_left[i], h))
            target.paste(img_crop, (sum(width[0:i]), 0, sum(width[0:i + 1]), h))  # 切片运算符是左开右闭
            # target.show()
        target.show()
        target.save(file_path)
        return dir, refer_date
    except Exception as e:
        print(e)


def get_queue_info(redis_name, dest_name):
    myQueue = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)

    time_wait = 10
    i = 0
    while i < 9:
        try:
            info = myQueue.redis.brpoplpush(redis_name, dest_name, 30)
            if info:
                id = int(info.split('|')[0])
                dir, refer_date = single_joint(id)
                num = img_recognition(dir, refer_date)
                print(num)
                cur.execute('UPDATE  baidu_index_v2 SET process_status = 1,recognitions = %s WHERE id = %s',
                            [int(num), id])
                conn.commit()
                time_wait = 10  # 重置等待时间
            else:  # 当前无
                time_wait *= 2
                print('nothing to do')
                time.sleep(time_wait)
        except Exception as e:
            traceback.print_exc()
            print(e)
        finally:
            i += 1
            pass
    # info = myQueue.redis.lrange('baidu_index', -1, -1)

def  test():
    print('this new process has been invoked ,pid as %s'%(os.getpid()))
    pool = multiprocessing.Pool()
    for i in range(0, 15):
        pool.apply_async(func=_run_proc, args=(i,))
    print('All subprocess has benn applied')
    pool.close()
    pool.join()
    print('All Done')

if __name__ == '__main__':
    print('Parent process %s is running' % (os.getpid()))
    conn, cur = myBaiduIndex.conn, myBaiduIndex.cur
    # myQueue = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    new_process = multiprocessing.Process(target=test,args=())
    new_process.start()
    new_process.join()
    print('here')
    # pool = multiprocessing.Pool()

    # for i in range(0, 15):
    #     pool.apply_async(func=_run_proc, args=(i,))
    # print('All subprocess has benn applied')
    # pool.close()
    # pool.join()
    # print('All Done')

    # get_queue_info('baidu_index_temp', 'baidu_index_temp')
    # img_recognition(r'D:\download\baiduINdex2018-06-01 0936_LOVE LIVE','2006-06-04')
