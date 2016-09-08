import os
import json
import argparse
from multiprocessing.dummy import Pool

import requests


def down(url, path):
    if os.path.isfile(path):
        print(path, 'already exists')
    else:
        with open(path, "wb") as code:
            code.write(requests.get(url).content)
        print(url, '->', path, 'finished')


def multi_down(params, outdir):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for param in params:
        param['path'] = os.path.join(outdir, param['path'])
    pool = Pool()
    pool.map(lambda param: down(**param), params)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Downloader')
    parser.add_argument('-i', '--input',
                        help='Path of download parameters file')
    parser.add_argument('-o', '--output',
                        help='Output folder directory')

    FLAGS = parser.parse_args()
    if not os.path.isdir(FLAGS.output):
        os.mkdir(FLAGS.output)

    params = json.load(open(FLAGS.input))
    multi_down(params, FLAGS.output)
