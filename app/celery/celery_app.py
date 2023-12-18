import os

from celery import Celery

from app.base import app
from app.configs import celery_config


def discover_tasks_modules(task_dir="tasks"):
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建task_dir的绝对路径
    task_abs_dir = os.path.join(current_dir, task_dir)
    module_dir = "app.celery.tasks"
    modules = []
    for file in os.listdir(task_abs_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"{module_dir}.{file[:-3]}"  # 去除.py后缀
            modules.append(module_name)
    return modules


def make_celery():
    celery = Celery(app.name, include=discover_tasks_modules())
    celery.config_from_object(celery_config)
    return celery


celery_app = make_celery()
