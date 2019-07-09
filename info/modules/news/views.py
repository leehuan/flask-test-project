from flask import render_template, jsonify, current_app, session, g, abort, request

from info import constants
from info.models import News, User
from info.utils.captcha.common import user_login_data

from info.utils.response_code import RET
from . import news_blu

@news_blu.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
    new = None
    try:
        new = News.query.filter(News.id==news_id).first()
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")

    if not new:
        abort(404)

    new.clicks += 1


    news_list = []
    # 右侧新闻排行的逻辑
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []

    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    user = g.user

    is_collected = False

    #如果用户收藏了此新闻，及为True
    if user:
        if new in user.collection_news:
            is_collected = True


    data = {
        "news_right_list": news_dict_li,
        "user": user.to_dict() if user else None,
        "news": new.to_dict(),
        "is_collected":is_collected,
    }
    return  render_template("news/detail.html",data = data)

@news_blu.route("/news_collect",methods=["POST"])
@user_login_data
def collect_news():

    user = g.user

    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="参数错误")

    news_id = request.json.get('news_id')
    action = request.json.get('action')

    if not all([news_id,action]):
        return jsonify(errno=RET.PARAMERR,errmsg = "参数错误")

    if action not in ["collect","cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        news_id = int(news_id)
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    news  = None

    try:
        news = News.query.get(news_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not news:
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if action == "collect":
        if news not in user.collection_news:
            user.collection_news.append(news)
    else:
        if news  in user.collection_news:
            user.collection_news.remove(news)

    return jsonify(errno=RET.OK, errmsg="操作成功")

