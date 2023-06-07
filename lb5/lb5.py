# -*- coding: utf-8 -*-
"""
@File  : lb5.py
@author: FxDr
@Time  : 2023/06/07 16:05
@Description:加了一个最近十条
"""
import threading


class MessageQueue:
    def __init__(self, max_messages):
        """
        构造函数
        :param max_messages: 最大消息数
        """
        self.max_messages = max_messages  # 设置消息队列的最大消息数
        self.messages = []  # 初始化消息列表，用于存储消息
        self.recent_messages = []  # 初始化最近消息列表，用于存储最近的消息
        self.lock = threading.Lock()  # 创建互斥锁，用于保证对消息列表的访问互斥
        self.not_empty = threading.Condition(self.lock)  # 创建条件变量，用于同步发送和接收操作

    # 发送进程调用
    def send_message(self, message):
        """
        发送消息的方法
        :param message: 消息内容
        """
        self.lock.acquire()  # 获取互斥锁，确保同一时间只有一个线程访问消息列表

        while len(self.messages) >= self.max_messages:  # 如果消息队列已满
            self.not_empty.wait()  # 等待条件变量，释放互斥锁并进入等待状态，直到被其他线程唤醒

        self.messages.append(message)  # 将消息添加到消息队列中
        self.recent_messages.append(message)  # 将消息添加到最近消息列表中
        print(f"Fxx发送消息：{message}")  # 打印发送者和消息内容
        self.not_empty.notify_all()  # 通知所有等待的线程，消息队列已经有可接收的消息
        self.lock.release()  # 释放互斥锁，允许其他线程访问消息列表

    # 接收进程调用
    def receive_message(self):
        """
        接收消息的方法
        """
        self.lock.acquire()  # 获取互斥锁，确保同一时间只有一个线程访问消息列表

        while len(self.messages) == 0:  # 如果消息队列为空
            self.not_empty.wait()  # 等待条件变量，释放互斥锁并进入等待状态，直到被其他线程唤醒

        message = self.messages.pop(0)  # 从消息队列中取出第一个消息
        print(f"接收方接收到消息：{message}")  # 打印接收者和消息内容
        self.not_empty.notify_all()  # 通知所有等待的线程，消息队列有空闲位置可以发送新消息
        self.lock.release()  # 释放互斥锁，允许其他线程访问消息列表

    # 获取最近十条消息
    def get_recent_messages(self):
        """
        获取最近十条消息
        :return: 最近十条消息列表
        """
        return self.recent_messages[-10:]


def sender_process(queue):
    while True:
        print('**********************************************************')
        choice = input("请选择操作：\n1. 发送消息\n2. 查看最近十条消息\n")

        if choice == "1":
            message = input("请输入要发送的消息：")
            queue.send_message(message)
        elif choice == "2":
            recent_messages = queue.get_recent_messages()
            print("最近十条消息：")
            for message in recent_messages:
                print(message)
        else:
            print("无效的选择，请重新输入。")


def receiver_process(queue):
    while True:
        queue.receive_message()


if __name__ == "__main__":
    queue = MessageQueue(10)

    sender_thread = threading.Thread(target=sender_process, args=(queue,))
    receiver_thread = threading.Thread(target=receiver_process, args=(queue,))

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()
    receiver_thread.join()
