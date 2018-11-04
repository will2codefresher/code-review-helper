# -*- coding: UTF-8 -*-

import chardet
import os
import re
import time
from bs4 import BeautifulSoup
from urllib import urlopen, urlretrieve

ckxx_home = r'http://www.hqck.net'


def get_bs(url):
    tmp0 = urlopen(url).read()
    urlcode = chardet.detect(tmp0).get('encoding', 'utf-8')
    text = tmp0.decode(urlcode, 'ignore')
    bs = BeautifulSoup(text, "html.parser")
    return bs


paper_dict = {}


def get_all_daily(daily_ul):
    for li in daily_ul.find_all(name='li'):
        title = li.a.span.text.strip()
        href = li.a['href']
        paper_dict[title] = "%s%s" % (ckxx_home, href)
        # print k


def get_today(daily_ul):
    today_str = time.strftime("%Y-%m-%d", time.localtime())
    return daily_ul.find(text=re.compile(".* %s.*" % today_str))


def get_recent(bs):
    return bs.select("ul > li > a > span.cRed")[0]


def get_img_dict(start_page_url):
    img_dict = {}
    bs = get_bs(start_page_url)
    base_url = start_page_url.split('/')
    base_url.pop()
    links = bs.select("div.paging > ul")[1]
    # print links
    for li in links.find_all(text=re.compile("^\d+$")):
        if '#' in li.parent['href']:
            img_dict[li] = start_page_url
        else:
            img_dict[li] = "%s/%s" % ('/'.join(base_url), li.parent['href'])
    return img_dict


def dl_img(src_link, dist_name):
    bs = get_bs(src_link)
    img = bs.find('img')
    print u"下载%s" % dist_name
    urlretrieve(img['src'], dist_name)


def download_img(title, img_dict, dst_path):
    dir_path = "%s/%s" % (dst_path, title)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for (i, v) in img_dict.items():
        dist_name = "%s/%s.jpg" % (dir_path, i)
        dl_img(v, dist_name)


if __name__ == "__main__":
    bs = get_bs(ckxx_home)
    daily_ul = bs.find(name='ul', class_='baozhi-list')
    # get_all_daily(daily_ul)

    # get today
    # today_paper = get_today(daily_ul)
    # print today_paper.parent.parent['href']
    # print today_paper

    # get recent
    recent_paper = get_recent(bs)
    # print recent_paper
    recent_home_url = "%s%s" % (ckxx_home, recent_paper.parent['href'])
    # print recent_home_url

    img_dict = get_img_dict(recent_home_url)
    # print img_dict

    title = 'test'
    dst_path = r'd:/'
    download_img(title, img_dict, dst_path)

    # for (k, v) in paper_dict.items():
    #     print "%s -- %s" % (k, v)
