# -*- coding: utf-8 -*-
"""
@File  : demo.py
@author: FxDr
@Time  : 2023/06/07 22:40
@Description:
"""
import os


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.files = []


class File:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions


class FileSystem:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.current_directory = ""

    def create_user(self, username, password):
        if username in self.users:
            print("用户名已存在")
            return
        user = User(username, password)
        self.users[username] = user

    def login(self, username, password):
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                self.current_user = user
                self.current_directory = "/" + user.username
                print("登录成功")
                return
        print("登录失败")

    def create_file(self, name, permissions):
        if self.current_user:
            filename = os.path.join(self.current_directory, name)
            if not os.path.exists(filename):
                with open(filename, "w") as file:
                    file.write("")
                os.chmod(filename, permissions)
                self.current_user.files.append(File(name, permissions))
                print("文件创建成功")
            else:
                print("文件已存在")
        else:
            print("请先登录")

    def delete_file(self, name):
        if self.current_user:
            filename = os.path.join(self.current_directory, name)
            if os.path.exists(filename):
                os.remove(filename)
                file = next((file for file in self.current_user.files if file.name == name), None)
                if file:
                    self.current_user.files.remove(file)
                print("文件删除成功")
            else:
                print("文件不存在")
        else:
            print("请先登录")

    def read_file(self, name):
        if self.current_user:
            filename = os.path.join(self.current_directory, name)
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    content = file.read()
                print("文件内容:")
                print(content)
            else:
                print("文件不存在")
        else:
            print("请先登录")

    def write_file(self, name, content):
        if self.current_user:
            filename = os.path.join(self.current_directory, name)
            if os.path.exists(filename):
                with open(filename, "w") as file:
                    file.write(content)
                print("文件写入成功")
            else:
                print("文件不存在")
        else:
            print("请先登录")

    def copy_file(self, source_name, destination_name):
        if self.current_user:
            source_filename = os.path.join(self.current_directory, source_name)
            destination_filename = os.path.join(self.current_directory, destination_name)
            if os.path.exists(source_filename):
                if not os.path.exists(destination_filename):
                    with open(source_filename, "r") as source_file:
                        content = source_file.read()
                    with open(destination_filename, "w") as destination_file:
                        destination_file.write(content)
                    print("文件复制成功")
                else:
                    print("目标文件已存在")
            else:
                print("源文件不存在")
        else:
            print("请先登录")

    def list_directory(self):
        if self.current_user:
            files = os.listdir(self.current_directory)
            print("目录列表:")
            for file in files:
                print(file)
        else:
            print("请先登录")

    def execute_command(self, command):
        if not self.current_user:
            if command.startswith("login"):
                _, username, password = command.split(" ")
                self.login(username, password)
            else:
                print("请先登录")
        else:
            if command.startswith("create_user"):
                _, username, password = command.split(" ")
                self.create_user(username, password)
            elif command.startswith("login"):
                _, username, password = command.split(" ")
                self.login(username, password)
            elif command == "exit":
                print("退出文件系统")
                return
            else:
                print("无效命令")


# 使用示例
filesystem = FileSystem()

while True:
    print("请输入命令：")
    command = input()

    filesystem.execute_command(command)
