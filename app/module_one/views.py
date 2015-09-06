from flask import Blueprint, render_template, current_app, jsonify

from ..tasks import worker


module_one = Blueprint('module_one', __name__)


@module_one.route('/', methods=['GET'])
def index():
    return render_template("module_one/index.html")


@module_one.route('/run', methods=['GET'])
def run_task():
    # run job in celery
    task = worker.run_task_async()
    return jsonify(name=current_app.name, status='Task is running', taskid=task.id), 202


@module_one.route('/status/<taskid>', methods=['GET'])
def task_status(taskid):
    task = worker.check_status_async(taskid)
    return jsonify(status=task.state)
