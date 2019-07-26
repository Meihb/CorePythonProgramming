from multiprocessing import Pool, Process, Queue
import os, time, random
import requests, json


def read(q):
    print('Process to read:%s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue:' % value)


def long_time_task(name, drawings_params, handicrafts_params):
    # 业务
    codes = [
        'FF889426917',
        'FF826758956',
        'FF224293124',
        'FF995773163',
        'FF411946468',
        'FF291972562',
        'FF840638067',
        'FF130142089',
        'FF970999439',
        'FF099811473'

    ]
    try:
        params = {'api_type': 'vote', 'code': random.choice(codes), 'drawings[]': drawings_params,
                  'handicrafts[]': handicrafts_params}
        response = requests.get("http://act1.ff.sdo.com/FF14Fanart/index.php", params)
        print(response.url)
        content = response.json()
        print(content)
        res = content["Data"]
        return res
    except Exception as e:
        pass


def test_pool():
    # global results
    time.sleep(random.randint(500, 999) * 0.001)
    print('Parent process %s.' % os.getpid())
    p = Pool()
    drawings = [1, 17, 57, 62, 63, 67, 70]
    handicrafts = [76, 82, 84]
    for i in range(10000):
        drawings_params = []
        handicrafts_params = []
        [drawings_params.append(random.choice(drawings)) for i in range(0, random.randint(1, len(drawings)))]
        [handicrafts_params.append(random.choice(handicrafts)) for i in range(0, random.randint(1, len(handicrafts)))]
        results.append(
            p.apply_async(long_time_task, args=(i, list(set(drawings_params)), list(set(handicrafts_params)))))
    print('Waiting for all subprocess done...')
    p.close()
    p.join()
    print('All subprocess done.')


if __name__ == '__main__':
    start_time = time.time()
    results = []
    # drawings =[1,17,57,62,63,67,70]
    # handicrafts = [76,82,84]
    # drawings_params = []
    # handicrafts_params = []
    # [drawings_params.append(random.choice(drawings)) for i in range(0, random.randint(1, len(drawings)),1)]
    # [handicrafts_params.append(random.choice(handicrafts)) for i in range(0, random.randint(1, len(handicrafts)),1)]

    # print(list(set(drawings_params)),list(set(handicrafts_params)))
    # long_time_task(1,list(set(drawings_params)),list(set(handicrafts_params)))
    test_pool()
    print("costs:" + str(time.time() - start_time))
