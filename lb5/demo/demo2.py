# -*- coding: utf-8 -*-
"""
@File  : demo2.py
@author: FxDr
@Time  : 2023/06/07 16:28
@Description:请无视我，就当是拓展数据库了
"""
import pyodbc
import threading


# 连接 SQL Server 数据库
def get_db():
    server_name = 'localhost'  # 主机名或 IP 地址
    database_name = 'OS'  # 数据库名称
    user_id = 'sa'  # 数据库账号
    mima = 'root'  # 数据库密码
    mydb = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={server_name}; '
                          f'DATABASE={database_name}; UID={user_id}; PWD={mima}')
    return mydb


# 消息队列类
class MessageQueue:
    def __init__(self, max_messages):
        self.max_messages = max_messages  # 设置消息队列的最大消息数
        self.lock = threading.Lock()  # 创建互斥锁，用于保证对消息列表的访问互斥

    # 发送进程调用
    def send_message(self, sender, message):
        with self.lock:
            mydb = get_db()
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO Message (sender, receiver, message) VALUES (?, ?, ?)",
                           (sender, '接收方', message))
            mydb.commit()
            print(f"{sender}发送消息：{message}")

    # 接收进程调用
    def receive_message(self, receiver):
        with self.lock:
            mydb = get_db()
            cursor = mydb.cursor()
            cursor.execute("SELECT TOP 10 sender, message FROM Message WHERE receiver = ? ORDER BY timestamp",
                           (receiver,))
            rows = cursor.fetchall()
            if rows:
                print(f"{receiver}接收到的最近十条消息：")
                for row in rows:
                    sender, message = row
                    print(f"发送者：{sender}，消息内容：{message}")
            else:
                print(f"{receiver}没有收到任何消息。")


# 测试函数
def sender_process(queue):
    while True:
        choice = input("请选择操作：\n1. 发送消息\n2. 查看最近十条消息\n")
        if choice == '1':
            message = input("请输入要发送的消息：")
            queue.send_message("Fxx", message)
        elif choice == '2':
            queue.receive_message("接收方")
        else:
            print("无效的选择，请重新输入。")


if __name__ == "__main__":
    queue = MessageQueue(10)

    sender_thread = threading.Thread(target=sender_process, args=(queue,))
    sender_thread.start()

    sender_thread.join()
