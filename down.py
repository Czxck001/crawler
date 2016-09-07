import requests
from multiprocessing.dummy import Pool


def down(url, path):
    with open(path, "wb") as code:
        code.write(requests.get(url).content)
    print(url, 'finished')


def multi_down(params):
    pool = Pool()
    pool.map(lambda param: down(**param), params)
