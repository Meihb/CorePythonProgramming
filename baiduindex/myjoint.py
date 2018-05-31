import redisConn, myBaiduIndex
import multiprocessing, time, random, pytesseract
from PIL import Image


def _run_proc(i, *args):
    print(i)
    # print(random.random())
    # time.sleep(random.random()*3)
    # print(args)


def img_recognition(save_dir, index):
    pytesseract.pytesseract.tesseract_cmd = myBaiduIndex.tesseract_exe
    jpgzoom = Image.open(r'%s\Puzzle%s.png' % (save_dir, index))
    # print(type(jpgzoom))
    (x, y) = jpgzoom.size
    x_s = 4 * x
    y_s = 4 * y
    out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
    # print(type(out))
    out.save('%s/zoom%s.jpg' % (save_dir, index), quality=95)
    num = pytesseract.image_to_string(out)
    if num:
        num = num.replace("'", '').replace('.', '').replace(',', '').replace('?', '7').replace("S", '5').replace(" ",
                                                                                                                 "").replace(
            "E", "8").replace("B", "8").replace("I", "1").replace("$", "8")
    else:
        num = ''
    print(num)
    return int(num)


def single_joint(id):
    conn, cur = myBaiduIndex.conn, myBaiduIndex.cur
    cur.execute("SELECT * FROM baidu_index WHERE id = %s", [id])
    row_info = cur.fetchall()[0]
    margin_left = [int(x) for x in  row_info['margin_left'].split(',')]
    width =  [int(x) for x in  row_info['width'].split(',')]
    location = row_info['location']
    dir = row_info['dir']
    refer_date = row_info['refer_date_begin']
    # print(margin_left,width,location,dir,refer_date)
    file_path = '%s\\Puzzle%s.png'%(dir,refer_date)
    try:
        origin_img  = Image.open(location)
        w,h = origin_img.size#返回当前图片宽,长元组
        target = Image.new('RGB',(sum(width),h))
        origin_img.show()
        for i in range(len(width)):
            img_crop = origin_img.crop((margin_left[i],0,width[i]+margin_left[i],h))
            target.paste(img_crop,(sum(width[0:i]),0,sum(width[0:i+1]),h))#切片运算符是左开右闭
            target.show()
        target.save(file_path)
    except Exception as e:
        print(e)



def get_queue_info():
    # myQueue = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    # info = myQueue.redis.lrange('baidu_index', -1, -1)
    # print(info, type(info))
    # info = info[0].split('|')

    single_joint(3)


if __name__ == '__main__':
    # myQueue = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    pool = multiprocessing.Pool(2)

    for i in range(0, 5):
        pool.apply_async(func=_run_proc, args=(i,))
    pool.close()
    pool.join()
    print('All Done')

    get_queue_info()
