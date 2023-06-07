# -*- coding: utf-8 -*-
"""
@File  : lb4.py
@Author: FxDr
@Time  : 2023/06/07 17:09
@Description:
"""
import copy
import random

PAGE_MEMORY = 4  # 系统可以容纳4个页面
INTERVAL = 1  # 模拟页面的访问时间间隔


# 访问时间模拟
def time_up(page_list):
    for p in page_list:
        p['time'] += INTERVAL


# 打印列表
def print_list(page_list):
    page_num = []
    for p in page_list:
        page_num.append(int(p['No']))
    print('当前页面队列：', end='')
    print(page_num)


# LRU打印最近访问时间
def print_time(page_list):
    for p in page_list:
        print('页面{},时间{}'.format(p['No'], p['time']))


# FIFO置换算法
def FIFO(pages_):
    pages = copy.deepcopy(pages_)
    print('FIFO:')
    print('页面请求序列为 8 9 10 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1')

    page_list = []
    page_faults = 0

    for p in pages:
        page_list_data = [page_['No'] for page_ in page_list]

        if p['No'] in page_list_data:
            print('\n\n下一个页面{}已在队列中，在队列第{}个'.format(
                p['No'], page_list_data.index(p['No']) + 1))
        else:
            if len(page_list) < PAGE_MEMORY:
                page_list.append(p)
                print(p['No'], end=' ')
            else:
                print('\n')
                replaced_page = page_list.pop(0)
                print("下一个页面:{}".format(p['No']))
                print('页面{}替换旧页面{}'.format(p['No'], replaced_page['No']))
                if replaced_page['modified']:
                    print('旧页面{}已被修改'.format(replaced_page['No']))
                page_list.append(p)

                page_faults += 1

                print_list(page_list)

                print('页面置换次数：', page_faults, end=' ')


# LRU置换算法
def LRU(page_):
    print('LRU:')
    print('页面请求序列为 8 9 10 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1')
    pages = copy.deepcopy(page_)
    page_list = []
    page_faults = 0

    for p in pages:
        page_list_data = [page_['No'] for page_ in page_list]
        time_up(page_list)

        if p['No'] in page_list_data:
            page_list[page_list_data.index(p['No'])]['time'] = 0
            print('\n下一个页面{}已在队列中，在队列第{}个\n'.format(
                p['No'], page_list_data.index(p['No']) + 1))
        else:
            if len(page_list) < PAGE_MEMORY:
                page_list.append(p)
            else:
                replaced_page = max(page_list, key=lambda t: t['time'])  # 最长时间，也就是最近未访问(最近未使用
                print_time(page_list)
                print("最近未访问的页面:{}".format(replaced_page['No']))
                page_list.remove(replaced_page)
                print('\n')
                print("下一个页面:{}".format(p['No']))
                print('页面{}替换旧页面{}'.format(p['No'], replaced_page['No']))
                if replaced_page['modified']:
                    print('旧页面%d已被修改' % replaced_page['No'])
                page_list.append(p)

            page_faults += 1

        print_list(page_list)

    print('页面置换次数：', page_faults)


'''
根据随机数来判断页面是否修改是为了模拟实际系统中页面的访问和修改行为。
在真实的计算机系统中，页面的修改是由操作系统和应用程序控制的，这取决于具体的使用情况和应用需求。
生成一个随机数来模拟页面的修改情况。当生成的随机数小于0.5时，将页面标记为未修改（False），表示该页面在被访问过程中没有被修改；
当随机数大于等于0.5时，将页面标记为已修改（True），表示该页面在被访问过程中被修改过。
这样做的目的是为了在页面置换算法中引入一定的随机性和变化性。'''


# 页面在访问过程中如果被修改了就需要将其写回磁盘或其他存储介质，以保持数据的一致性


def init(pages):
    for p in pages:
        p['time'] = 0
        p['visited'] = False  # 访问flag
        a = random.random()
        if a < 0.5:
            p['modified'] = False  # 修改flag
        else:
            p['modified'] = True


if __name__ == '__main__':
    pages = [
        {'No': 8}, {'No': 9}, {'No': 10}, {'No': 7}, {'No': 0}, {'No': 1}, {'No': 2},
        {'No': 0}, {'No': 3}, {'No': 0}, {'No': 4}, {'No': 2}, {'No': 3}, {'No': 0},
        {'No': 3}, {'No': 2}, {'No': 1}, {'No': 2}, {'No': 0}, {'No': 1}, {'No': 7},
        {'No': 0}, {'No': 1}
    ]

    init(pages)

    FIFO(pages)

    LRU(pages)
