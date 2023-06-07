# -*- coding: utf-8 -*-
"""
@File  : lb5.1.py
@author: FxDr
@Time  : 2023/06/07 15:42
@Description:平平无奇发送
"""
import threading
import time


# 中间实体类
class MessageQueue:
    def __init__(self, max_messages):
        """
        构造函数
        :param max_messages: 最大消息数
        """
        self.max_messages = max_messages  # 设置消息队列的最大消息数
        self.messages = []  # 初始化消息列表，用于存储消息
        self.lock = threading.Lock()  # 创建互斥锁，用于保证对消息列表的访问互斥
        self.not_empty = threading.Condition(self.lock)  # 创建条件变量，用于同步发送和接收操作

    # 发送进程调用
    def send_message(self, sender, message):
        """
        发送消息的方法
        :param sender: 发送者标识
        :param message: 消息内容
        """
        self.lock.acquire()  # 获取互斥锁，确保同一时间只有一个线程访问消息列表

        while len(self.messages) >= self.max_messages:  # 如果消息队列已满
            self.not_empty.wait()  # 等待条件变量，释放互斥锁并进入等待状态，直到被其他线程唤醒

        self.messages.append((sender, message))  # 将消息添加到消息队列中
        print(f"{sender}发送消息：{message}")  # 打印发送者和消息内容
        self.not_empty.notify_all()  # 通知所有等待的线程，消息队列已经有可接收的消息
        self.lock.release()  # 释放互斥锁，允许其他线程访问消息列表

    # 接收进程调用
    def receive_message(self, receiver):
        """
        接收消息的方法
        :param receiver: 接收者标识
        """
        self.lock.acquire()  # 获取互斥锁，确保同一时间只有一个线程访问消息列表

        while len(self.messages) == 0:  # 如果消息队列为空
            self.not_empty.wait()  # 等待条件变量，释放互斥锁并进入等待状态，直到被其他线程唤醒

        sender, message = self.messages.pop(0)  # 从消息队列中取出第一个消息
        print(f"{receiver}接收到来自{sender}的消息：{message}")  # 打印接收者、发送者和消息内容
        self.not_empty.notify_all()  # 通知所有等待的线程，消息队列有空闲位置可以发送新消息
        self.lock.release()  # 释放互斥锁，允许其他线程访问消息列表


def sender_process(queue):
    for i in range(1, 20):
        time.sleep(1)
        queue.send_message("发送进程", f"消息{i}:" + input("请输入要发送的消息\n"))


def receiver_process(queue):
    for i in range(1, 20):
        time.sleep(2)
        queue.receive_message("接收进程")


if __name__ == "__main__":
    queue = MessageQueue(10)

    sender_thread = threading.Thread(target=sender_process, args=(queue,))
    receiver_thread = threading.Thread(target=receiver_process, args=(queue,))

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()
    receiver_thread.join()
