# -*- coding: utf-8 -*-
"""
@File  : lb6.py
@author: FxDr
@Time  : 2023/06/07 0:56
@Description:
"""
import numpy as np

"""
何为银行家算法？
首先，算法检查系统中是否存在足够的资源可以满足当前未完成的进程的需求。即检查进程的需求向量（Need）是否小于等于可用资源向量（Available）。
然后，算法模拟资源的分配，将请求的资源分配给进程，并更新系统的资源分配情况。
接下来，算法检查系统是否存在一个安全序列，即一个进程执行的顺序，使得每个进程在执行时都能够完成，并且不会发生资源竞争。
如果存在安全序列，系统被认为是安全的，并且资源分配是可行的。安全序列指示系统中的进程按照一定的顺序执行，每个进程都能够顺利完成，并释放所使用的资源。
如果不存在安全序列，系统被认为是不安全的，当前请求的资源将导致系统陷入死锁状态。在这种情况下，资源请求被拒绝，进程需要等待，直到资源可用或系统重新进入安全状态。
"""

# 初始化各数据结构
# 可利用各资源总数
Available = np.array([3, 3, 2])
print('Available\n', Available)
length_Available = len(Available)
# 各进程最大需求资源数
Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
print('Max\n', Max)
length_processes = len(Max)
# 已分配各进程的资源数
Allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
print('Allocation\n', Allocation)
# 各进程尚需的资源数
Need = Max - Allocation
print('Need\n', Need)

# 安全进程执行序列
safe_sequence = []

"""
Available（可利用资源向量）：表示系统中当前可用的资源数量。在安全序列的查找过程中，Available会不断更新，模拟进程执行过程中资源的释放和回收。
Allocation（已分配矩阵）：表示当前系统中已经分配给各个进程的资源数量。在安全序列的查找过程中，Allocation会模拟进程执行过程中的资源分配情况。
Need（需求矩阵）：表示各个进程还需要的资源数量。在安全序列的查找过程中，Need会根据进程执行过程中的资源分配情况进行更新。
"""


def simulateBankerAlgorithm(process_name, requested_resources):
    global Available, Allocation, Need, safe_sequence

    # 检查请求是否合法
    if not np.all(requested_resources <= Need[process_name]):
        print("您输入的是进程{},\n请求资源数:{}".format(process_name, requested_resources))
        print(requested_resources, '<=', Need[process_name])
        print("请求的资源超过了进程的最大需求资源数")
        print("***************************************")
        return

    if not np.all(requested_resources <= Available):
        print("您输入的是进程{},\n请求资源数:{}".format(process_name, requested_resources))
        print(requested_resources, '<=', Available)
        print("没有足够的资源可用于满足请求")
        print("***************************************")
        return

    # 模拟资源分配
    Available -= requested_resources
    Allocation[process_name] += requested_resources
    Need[process_name] -= requested_resources

    # 运行银行家算法进行安全性检查
    work = Available.copy()
    finish = np.zeros(length_processes, dtype=bool)

    while True:
        # 在进程集合中找到一个 Finish[i] = false 且 Need[i] <= Work 的进程
        found = False
        for i in range(length_processes):
            if not finish[i] and np.all(Need[i] <= work):
                work += Allocation[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True

                # 打印信息
                print("进程 {} 满足条件：Need[{}] = {} <= Available = {}".format(i, i, Need[i], work - Allocation[i]))
                print("更新 Available: {} + {} = {}".format(work, Allocation[i], work))
                print("更新 finish[{}] = True".format(i))
                print("更新安全序列: {}\n".format(safe_sequence))

        if not found:
            break

    # 检查系统是否处于安全状态
    if np.all(finish):
        print("***************************************")
        print("您输入的请求进程是: {}".format(process_name))
        print("您输入的请求资源数: {}".format(requested_resources))
        print("系统安全性: 安全")
        print("安全序列为: {}".format(safe_sequence))
        print("资源分配情况:")
        print("Available: {}".format(work))
        print("Allocation:")
        print(Allocation)
        print("Need:")
        print(Need)
        print("***************************************")
    else:
        print("***************************************")
        print("您输入的请求进程是: {}".format(process_name))
        print("您输入的请求资源数: {}".format(requested_resources))
        print("系统安全性: 不安全")
        print("资源分配情况:")
        print("Available: {}".format(work))
        print("Allocation:")
        print(Allocation)
        print("Need:")
        print(Need)
        print("***************************************")


# 测试
# 安全
simulateBankerAlgorithm(3, np.array([0, 0, 1]))  # 0 0 1 / 3 2 2
# 不安全
simulateBankerAlgorithm(2, np.array([6, 0, 0]))  # 没有足够的资源可用于满足请求 6 0 0 / 3 2 2
simulateBankerAlgorithm(1, np.array([1, 2, 3]))  # 请求的资源超过了进程的最大需求资源数 1 2 3 / 1 2 2
