# -*- coding: utf-8 -*-
"""
@File  : lb7.py
@author: FxDr
@Time  : 2023/06/06 23:38
@Description:
"""
import copy

TRACK_REQUEST_COUNT = 10  # 请求访问的磁道数量
TRACK_START = 50  # 磁道起始位置
SCAN_DIRECTION = 1  # 1表示向磁道号增加的方向扫描，0表示向磁道号减小的方向


# FCFS（先来先服务）
def fcfs(track_request):
    """
    :param track_request:
    :return: 起始位置加原来序列
    """
    queue_fcfs = [TRACK_START] + track_request[:]
    return queue_fcfs


# SSTF（最短寻道时间优先）
def find_nearest(current, track_request, visited):
    """
    用于找到当前位置 current 最近的未访问磁道
    :param current:当前位置
    :param track_request:磁道请求序列
    :param visited:已访问标记列表
    :return:最近磁道的索引和距离
    """
    # 初始的最小距离为正无穷大,用于比较和更新最小距离。
    min_dis = float('inf')
    # 设置初始的最小距离磁道的索引为-1，用于记录最小距离磁道的位置。
    min_index = -1
    # 遍历磁道请求序列
    for i in range(len(track_request)):
        # 假如没被访问
        if not visited[i]:
            # 计算当前位置和磁道请求的距离
            dis = abs(current - track_request[i])
            # 如果计算得到的距离小于当前最小距离，更新最小距离和最小距离磁道的索引。
            if dis < min_dis:
                min_dis = dis
                min_index = i
    # 将最小距离磁道标记为已访问
    visited[min_index] = True
    return min_index, min_dis


def SSTF(track_request):
    """
    最短寻道时间优先（SSTF）磁盘调度算法
    :param track_request: 磁道请求序列
    :return: 按照SSTF算法排序后的磁道访问序列
    """
    # TRACK_REQUEST_COUNT请求访问的磁道数量 这里是10
    # 这是构造了一个 有10个False的序列
    visited = [False] * TRACK_REQUEST_COUNT
    queue_SSTF = []
    current = TRACK_START  # 起始的磁道
    # 遍历磁道序列
    for _ in range(len(track_request)):
        # 得到距离当前访问的磁道的最短距离的磁道的 索引和距离
        index, _ = find_nearest(current, track_request, visited)
        # 加入最终序列
        queue_SSTF.append(current)
        # 更新当前磁道
        current = track_request[index]
    return queue_SSTF


# SCAN（电梯算法）
def SCAN(track_request):
    # 全局变量 ，扫描的方向
    global SCAN_DIRECTION
    # 最终序列
    queue_SCAN = []

    track_request_copy = copy.deepcopy(track_request)  # 复制磁道请求序列，以免修改原始序列
    track_request_copy.sort()  # 将磁道请求序列按升序排序

    # 执行扫描操作，直到所有磁道都被访问完毕
    while track_request_copy:
        if SCAN_DIRECTION == 1:
            # 当前扫描方向为向磁道号增加的方向
            for track in track_request_copy.copy():
                if TRACK_START <= track:
                    # 将满足条件的磁道加入到访问序列中
                    queue_SCAN.append(track)
                    # 从复制的序列中移除已访问的磁道
                    track_request_copy.remove(track)
            # 改变扫描方向为向磁道号减小的方向
            # 因为已经结束了
            SCAN_DIRECTION = 0

        if SCAN_DIRECTION == 0:
            # 当前扫描方向为向磁道号减小的方向
            # 反转磁道请求序列，以实现向减小的方向扫描
            track_request_copy.reverse()
            # 遍历
            for track in track_request_copy.copy():
                if TRACK_START >= track:
                    queue_SCAN.append(track)  # 将满足条件的磁道加入到访问序列中
                    track_request_copy.remove(track)  # 从复制的序列中移除已访问的磁道
            SCAN_DIRECTION = 1  # 改变扫描方向为向磁道号增加的方向

    return queue_SCAN


def calculate(queue):
    print('访问的磁道序列为:', queue)
    sum_gap = sum([abs(queue[i] - queue[i - 1]) for i in range(1, len(queue))])
    print('移动的磁道数为：%d' % sum_gap)
    print('平均移动的磁道数为：%.2f' % (sum_gap / TRACK_REQUEST_COUNT), end='\n')


if __name__ == '__main__':
    # 磁道序列
    track_request = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    print("磁道序列:")
    print(track_request, end='\n')

    print("FCFS:")
    calculate(fcfs(track_request))

    print("SSTF:")
    calculate(SSTF(track_request))

    print("SCAN:")
    calculate(SCAN(track_request))
