# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'wh'

from crawler_impl.communities_list_crawler import CommunitiesListCrawler as Crawler

import time

if __name__ == '__main__':
    crawler = Crawler()
    crawler.craw()
    # # #crawlerdetal = VideoDetailCrawler()
    # threads = []
    # for i in range(1, 13):
    # thread = Crawler(i)
    # threads.append(thread)
    # for i in range(0, 12):
    # threads[i].start()
    #
    # for i in range(0, 12):
    # threads[i].join()

    print("end in ", time.ctime())