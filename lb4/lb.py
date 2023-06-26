# -*- coding: utf-8 -*-
"""
@File  : lb.py
@Time  : 2023/06/26 19:39
@Description:
"""

import random

# PAGE_MEMORY = 4  # 系统可以容纳4个页面
PAGE_MEMORY = int(input("请输入初始分配的块数:"))
INTERVAL = 1  # 模拟页面的访问时间间隔


class Page:
    def __init__(self, number):
        """
        number: 页面的编号。
        time: 页面的访问时间，初始值为0。在LRU算法中，每次访问页面时，该时间会递增，用于记录页面的访问顺序。
        visited: 表示页面是否被访问过的标志。初始值为False，在页面被访问时会被设置为True。
        modified: 表示页面是否被修改过的标志。使用随机数生成，如果生成的随机数大于等于0.5，则表示页面被修改过；否则，表示页面未被修改过。
        """
        self.number = number
        self.time = 0
        self.visited = False
        self.modified = random.random() >= 0.5


# 访问时间模拟
def time_up(page_list):
    for p in page_list:
        p.time += INTERVAL


# 打印列表
def print_list(page_list):
    page_num = [p.number for p in page_list]
    print('当前页面队列：', page_num)


# LRU打印最近访问时间
def print_time(page_list):
    for p in page_list:
        print('页面{},时间{}'.format(p.number, p.time))


# FIFO置换算法
def FIFO():
    print('FIFO:')
    page_sequence = list(map(int, input("请输入页面请求序列，以空格分隔: ").split()))
    print('页面请求序列为', ' '.join(map(str, page_sequence)))

    page_list = []
    page_faults = 0

    for page_number in page_sequence:
        p = Page(page_number)
        page_list_data = [page.number for page in page_list]

        if p.number in page_list_data:
            print('\n\n下一个页面{}已在队列中，在队列第{}个'.format(
                p.number, page_list_data.index(p.number) + 1))
        else:
            if len(page_list) < PAGE_MEMORY:
                page_list.append(p)
                print(p.number, end=' ')
            else:
                print('\n')
                replaced_page = page_list.pop(0)
                print("下一个页面:{}".format(p.number))
                print('页面{}替换旧页面{}'.format(p.number, replaced_page.number))
                if replaced_page.modified:
                    print('旧页面{}已被修改'.format(replaced_page.number))
                page_list.append(p)

                page_faults += 1

                print_list(page_list)

                print('页面置换次数：', page_faults, end=' ')


# LRU置换算法 最近最少使用
def LRU():
    print('LRU:')
    page_sequence = list(map(int, input("请输入页面请求序列，以空格分隔: ").split()))  # 要求输入请求序列
    print('页面请求序列为', ' '.join(map(str, page_sequence)))  # 打印
    page_list = []  # 当前页面队列
    page_faults = 0  # 记录页面置换次数

    for page_number in page_sequence:
        p = Page(page_number)  # 对于每个页面，它会创建一个 Page 对象，该对象的属性包括页面号码、时间、是否被访问和是否被修改。
        page_list_data = [page.number for page in page_list]
        time_up(page_list)

        if p.number in page_list_data:
            page_list[page_list_data.index(p.number)].time = 0
            print('\n下一个页面{}已在队列中，在队列第{}个\n'.format(
                p.number, page_list_data.index(p.number) + 1))
        else:
            if len(page_list) < PAGE_MEMORY:
                page_list.append(p)
            else:
                replaced_page = max(page_list, key=lambda t: t.time)  # 最长时间，也就是最近未访问(最近未使用
                print_time(page_list)
                print("最近未访问的页面:{}".format(replaced_page.number))
                page_list.remove(replaced_page)
                print('\n')
                print("下一个页面:{}".format(p.number))
                print('页面{}替换旧页面{}'.format(p.number, replaced_page.number))
                if replaced_page.modified:
                    print('旧页面%d已被修改' % replaced_page.number)
                page_list.append(p)

            page_faults += 1

        print_list(page_list)

    print('页面置换次数：', page_faults)


if __name__ == '__main__':
    FIFO()

    LRU()
