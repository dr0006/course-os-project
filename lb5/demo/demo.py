# -*- coding: utf-8 -*-
"""
@File  : lb4.py
@author: FxDr
@Time  : 2023/06/07 16:54
@Description:
"""
import threading
from collections import deque


# 消息队列类
class MessageQueue:
    def __init__(self, max_messages):
        self.max_messages = max_messages  # 设置消息队列的最大消息数
        self.messages = deque()  # 使用双端队列来保存消息
        self.lock = threading.Lock()  # 创建互斥锁，用于保证对消息队列的访问互斥
        self.condition = threading.Condition()  # 创建条件变量，用于实现进程间的同步

    # 发送进程调用
    def send_message(self, sender, message):
        with self.condition:
            with self.lock:
                if len(self.messages) >= self.max_messages:
                    self.messages.popleft()  # 如果消息队列已满，则移除最旧的一条消息
                self.messages.append((sender, message))
                print(f"{sender}发送消息：{message}")
                self.condition.notify()  # 通知接收进程有新消息到达

    # 接收进程调用
    def receive_message(self, receiver):
        with self.condition:
            while len(self.messages) == 0:
                self.condition.wait()  # 如果消息队列为空，则等待直到有新消息到达
            with self.lock:
                print(f"{receiver}接收到的最近十条消息：")
                for sender, message in self.messages:
                    print(f"发送者：{sender}，消息内容：{message}")


# 测试函数
def sender_process(queue):
    while True:
        choice = input("请选择操作：\n1. 发送消息\n2. 查看最近十条消息\n")
        if choice == '1':
            message = input("请输入要发送的消息：")
            queue.send_message("发送方", message)
        elif choice == '2':
            queue.receive_message("接收方")
        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    queue = MessageQueue(10)

    sender_thread = threading.Thread(target=sender_process, args=(queue,))
    sender_thread.start()

    sender_thread.join()
