from flask import render_template, current_app, request, session

from info.models import User
from . import index_blu
from info import redis_store


@index_blu.route("/")
def index():

    user_id = session.get('user_id',None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    data = {
        "user":user.to_dict() if user  else  None
    }



    return render_template('news/index.html',data=data)

#加载网站小图标，游览器启动默认加载此路由
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')