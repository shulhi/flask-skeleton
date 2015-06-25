from flask import Blueprint, render_template


module_one = Blueprint('module_one', __name__)


@module_one.route('/', methods=['GET'])
def index():
    return render_template("module_one/index.html")
