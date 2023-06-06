# -*- coding: utf-8 -*-
"""
@File  : lb10.py
@author: FxDr
@Time  : 2023/06/06 16:01
@Description:
使用的是 `asyncio.Semaphore` 实例来模拟同步原语。
Semaphore 是一个计数器类，用于线程同步。
Semaphore 管理一个内部计数器，用来表示可用资源的数量。
调用 `asyncio.Semaphore.acquire()` 方法会将内部计数器减 1，如果计数器的值为 0，则 acuire() 方法会阻塞，直到有可用资源。
调用 `asyncio.Semaphore.release()` 方法会将内部计数器加 1，释放一个资源。
在这个实现中，我们使用 `asyncio.Semaphore` 实现了进程的同步。
在进程函数中，我们使用 `asyncio.Semaphore.acquire()` 方法获得信号量，表示进程需要访问共享变量或共享资源，从而保证不会出现数据竞争问题。
当一个进程获得信号量时，其他进程需要等待该进程释放信号量后才能继续执行，从而保证了进程的同步。
"""
import asyncio


# 定义进程函数
async def process_1(semaphore):
    print('进程 1 正在执行')
    await semaphore.acquire()  # 获得信号量
    print('进程 1 获得了信号量')
    print('信号量:', semaphore._value)  # 输出信号量的计数器值
    await asyncio.sleep(1)
    print('进程 1 释放了信号量')
    semaphore.release()  # 释放信号量
    print('信号量:', semaphore._value)  # 输出信号量的计数器值


async def process_2(semaphore):
    print('进程 2 正在执行')
    await semaphore.acquire()  # 获得信号量
    print('进程 2 获得了信号量')
    print('信号量:', semaphore._value)  # 输出信号量的计数器值
    await asyncio.sleep(1)
    print('进程 2 释放了信号量')
    semaphore.release()  # 释放信号量
    print('信号量:', semaphore._value)  # 输出信号量的计数器值


# 定义状态追踪器
# 记录了每个函数的名称、参数和关键字参数
class StateTracer:
    def __init__(self):
        self.states = []

    def __call__(self, func):
        async def wrapped(*args, **kwargs):
            self.states.append({'function': func.__name__, 'args': args, 'kwargs': kwargs})
            return await func(*args, **kwargs)

        return wrapped

    def get_states(self, function=None):
        if function:
            return [state for state in self.states if state['function'] == function]
        else:
            return self.states


# 定义语义解析器
def parse_algorithm(algorithm, semaphore):
    async def coroutine():
        await algorithm(semaphore)

    return coroutine


# 定义验证引擎
# 验证进程函数的同步关系。
# 通过检查信号量的计数器值来判断是否发生了死锁。如果有连续的两个状态都显示计数器为0，则表示发生了死锁。
def verify_algorithm(algorithm_name, state_tracer):
    states = state_tracer.get_states(algorithm_name)
    for i in range(len(states) - 1):
        if states[i]['args'][0]._value == 0 and states[i + 1]['args'][0]._value == 0:
            print(f"错误：{algorithm_name} 发生了死锁")
            return False
    print(f"{algorithm_name} 正确")
    return True


# 测试代码
async def main():
    semaphore = asyncio.Semaphore(1)  # 定义信号量 初始值为1
    state_tracer = StateTracer()  # 定义状态追踪器

    algorithm = parse_algorithm(process_1, semaphore)
    algorithm = state_tracer(algorithm)  # 进行状态追踪
    await algorithm()

    algorithm = parse_algorithm(process_2, semaphore)
    algorithm = state_tracer(algorithm)  # 进行状态追踪
    await algorithm()

    verify_algorithm("process_1", state_tracer)  # 进行算法验证
    verify_algorithm("process_2", state_tracer)


if __name__ == '__main__':
    asyncio.run(main())
