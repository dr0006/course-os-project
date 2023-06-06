# -*- coding: utf-8 -*-
"""
@File  : lb8.py
@author: FxDr
@Time  : 2023/06/06 17:52
@Description:
"""


class Job:
    def __init__(self, job_id, arrival_time, service_time, priority):
        self.job_id = job_id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.priority = priority


class Scheduler:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.jobs = []
        self.schedule = []

    def add_job(self, job):
        self.jobs.append(job)

    def run_scheduler(self):
        if self.algorithm == 'FIFO':
            self.schedule = self.fifo_scheduler()
        elif self.algorithm == 'SJF':
            self.schedule = self.sjf_scheduler()
        elif self.algorithm == 'Priority':
            self.schedule = self.priority_scheduler()

    # 通俗易懂 FIFO先来先服务
    def fifo_scheduler(self):
        sorted_jobs = sorted(self.jobs, key=lambda job: job.arrival_time)
        return [job.job_id for job in sorted_jobs]

    # SJF 短作业优先，我是非抢占
    def sjf_scheduler(self):
        current_time = 0
        remaining_jobs = self.jobs.copy()
        schedule = []
        while remaining_jobs:
            eligible_jobs = [job for job in remaining_jobs if job.arrival_time <= current_time]
            if eligible_jobs:
                shortest_job = min(eligible_jobs, key=lambda job: job.service_time)
                schedule.append(shortest_job.job_id)
                remaining_jobs.remove(shortest_job)
                current_time += shortest_job.service_time
            else:
                current_time += 1
        return schedule

    # 优先级调度，我是非抢占
    def priority_scheduler(self):
        current_time = 0
        remaining_jobs = self.jobs.copy()
        schedule = []
        while remaining_jobs:
            eligible_jobs = [job for job in remaining_jobs if job.arrival_time <= current_time]
            if eligible_jobs:
                highest_priority_jobs = [job for job in eligible_jobs if
                                         job.priority == min(eligible_jobs, key=lambda j: j.priority).priority]
                shortest_job = min(highest_priority_jobs, key=lambda job: job.service_time)
                schedule.append(shortest_job.job_id)
                remaining_jobs.remove(shortest_job)
                current_time += shortest_job.service_time
            else:
                current_time += 1
        return schedule


# 测试代码
def main(plan):
    # 创建作业调度器，选择算法为 ..
    scheduler = Scheduler(plan)

    # 添加作业
    # 数字越小优先级越高
    job1 = Job(1, 0, 4, 2)  # 作业 1 到达时间 0 服务时间4 优先级 2
    job2 = Job(2, 1, 3, 1)
    job3 = Job(3, 2, 2, 3)
    job4 = Job(4, 3, 1, 4)
    scheduler.add_job(job1)
    scheduler.add_job(job2)
    scheduler.add_job(job3)
    scheduler.add_job(job4)

    # 执行作业调度
    scheduler.run_scheduler()

    # 输出调度次序
    print("调度次序:", scheduler.schedule, '\n')


if __name__ == '__main__':
    while True:
        main(input("输出选择的算法: FIFO OR SJF OR Priority\n"))
