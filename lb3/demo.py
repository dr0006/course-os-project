import os
import stat

# 定义全局变量,存储当前登录的用户名
current_user = None


def create_user(command):
    _, username, password = command.split()
    # 检查用户是否已经存在
    user_folder = os.path.join('User', username)
    if os.path.exists(user_folder):
        print(f"用户'{username}'已经存在")
        return
    # 在根目录创建用户文件夹
    os.makedirs(user_folder)
    # 创建密码文件，将密码写入
    password_file = os.path.join(user_folder, 'password.txt')
    with open(password_file, 'w') as file:
        file.write(password)
    # 设置密码文件的权限
    os.chmod(password_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)  # 设置为只读权限
    print(f"用户'{username}'已创建")


def login(command):
    global current_user  # 声明全局变量
    _, username, password = command.split()
    # 检查用户文件夹是否存在
    user_folder = os.path.join('User', username)
    if os.path.exists(user_folder):
        # 检查密码文件是否存在
        password_file = os.path.join(user_folder, 'password.txt')
        if os.path.exists(password_file):
            # 验证密码是否正确
            with open(password_file, 'r') as file:
                stored_password = file.read().strip()
            if password == stored_password:
                # 进入用户文件夹
                os.chdir(user_folder)
                current_user = username  # 设置当前登录的用户名
                print(f"用户'{username}'已登录")
                return
            else:
                print("密码不正确")
                return
    print(f"用户'{username}'不存在")


def logout():
    global current_user  # 声明全局变量
    current_user = None
    os.chdir('..')  # 退出用户文件夹
    print("已退出登录")


def open_file(filename):
    # 构建文件的路径
    file_path = os.path。join(os.getcwd(), filename)
    # 检查文件是否存在
    if os.path。exists(file_path):
        # 打开文件
        with open(file_path, 'r') as file:
            contents = file.read()
        print(f"文件'{filename}'的内容：")
        print(contents)
    else:
        print(f"文件'{filename}'不存在")


def create_file(filename):
    # 构建文件的路径
    file_path = os.path。join(os.getcwd(), filename)
    # 检查文件是否存在
    if os.path。exists(file_path):
        print(f"文件'{filename}'已存在")
    else:
        # 创建文件
        with open(file_path, 'w') as file:
            print(f"文件'{filename}'已创建")


def edit_file(filename):
    # 构建文件的路径
    file_path = os.path。join(os.getcwd(), filename)
    # 检查文件是否存在
    if os.path。exists(file_path):
        try:
            # 打开文件进行编辑
            print(f"正在编辑文件'{filename}'...")
            print("请在下面输入内容（输入':q'保存并退出）：")
            contents = []
            while True:
                line = input()
                if line == ':q':
                    # 保存并退出编辑
                    with open(file_path, 'w') as file:
                        file.write('\n'。join(contents))
                    print(f"文件'{filename}'已保存")
                    break
                else:
                    contents.append(line)
        except PermissionError:
            print(f"无法编辑文件'{filename}'，该文件为密码文件，无法修改")
    else:
        print(f"文件'{filename}'不存在")


def delete_file(filename):
    # 构建文件的路径
    file_path = os.path。join(os.getcwd(), filename)
    # 检查文件是否存在
    if os.path。exists(file_path):
        try:
            # 删除文件
            os.remove(file_path)
            print(f"文件'{filename}'已删除")
        except PermissionError:
            print(f"无法删除文件'{filename}'，该文件为密码文件，无法删除")
    else:
        print(f"文件'{filename}'不存在")


# 主循环
while True:
    command = input("请输入命令：")
    if command.startswith('create_user'):
        create_user(command)
    elif command.startswith('login'):
        login(command)
    elif command.startswith('logout'):
        logout()
    elif not current_user 和 not command.startswith('create_user'):
        print("请先登录账号,没有账号可以注册")
    elif command.startswith('open'):
        _, filename = command.split()
        open_file(filename)
    elif command.startswith('create'):
        _, filename = command.split()
        create_file(filename)
    elif command.startswith('edit'):
        _, filename = command.split()
        edit_file(filename)
    elif command.startswith('delete'):
        _, filename = command.split()
        delete_file(filename)
    else:
        print("无效的命令")
