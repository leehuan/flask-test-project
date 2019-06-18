from flask import render_template, current_app
from . import index_blu
from info import redis_store


@index_blu.route("/")
def index():
    return render_template('news/index.html')

#加载网站小图标，游览器启动默认加载此路由
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')