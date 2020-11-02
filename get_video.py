# -*- coding: utf-8 -*-
import requests
from contextlib import closing
import time


def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024 * 10
        content_size = int(r.headers['content-length'])
        print('下载开始')
        with open(path, "wb") as f:
            p = ProgressData(size=content_size, unit='Kb', block=chunk_size)
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                p.output()


class ProgressData(object):

    def __init__(self, block, size, unit, file_name='', ):
        self.file_name = file_name
        self.block = block / 1000.0
        self.size = size / 1000.0
        self.unit = unit
        self.count = 0
        self.start = time.time()

    def output(self):
        self.end = time.time()
        self.count += 1
        speed = self.block / (self.end - self.start) if (self.end - self.start) > 0 else 0
        self.start = time.time()
        loaded = self.count * self.block
        progress = round(loaded / self.size, 4)
        if loaded >= self.size:
            print(u'%s下载完成\r\n' % self.file_name)
        else:
            print(u'{0}下载进度{1:.2f}{2}/{3:.2f}{4} 下载速度{5:.2%} {6:.2f}{7}/s'. \
                  format(self.file_name, loaded, self.unit, \
                         self.size, self.unit, progress, speed, self.unit))
            print('%50s' % ('/' * int((1 - progress) * 50)))


if __name__ == '__main__':
    url = 'https://f.video.weibocdn.com/0037d7KOgx07AOW5N3AI01041200g8QV0E010.mp4?label=mp4_720p&template=1280x720.25.0&trans_finger=1f0da16358befad33323e3a1b7f95fc9&Expires=1581352524&ssig=XVs9so5tyO&KID=unistore,video&media_id=1034:4470113890402329&tp=YTkl0eM8:YTkl0eM8&us=6jCvkV&ori=0&ctb=0&ot=h&ps=4pdsh0&ab=1410-g0,540-g1,1326-g1,966-g1,1055-g0,878-g1,1493-g0,1192-g0,1091-g1,1191-g0,1046-g2,1258-g0,1277-g3'
    path = "weibo/1.mp4"
    download_file(url, path)
