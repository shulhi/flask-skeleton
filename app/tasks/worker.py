from time import sleep
from celery import chain

from ..app import create_app, create_celery


app = create_app(register_blueprints=False)
celery = create_celery(app)


@celery.task(bind=True)
def long_map_task(self, x, y):
    sleep(10)
    return x + y


@celery.task(bind=True)
def long_run_task(self, x, y):
    sleep(10)
    return x + y


def check_status_async(taskid):
    task = celery.AsyncResult(taskid)
    return task


def run_task_async():
    task = chain(long_run_task.s(2,2), long_map_task.s(4)).apply_async()
    return task
