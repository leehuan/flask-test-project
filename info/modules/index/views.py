from flask import render_template, current_app, request, session, jsonify, g

from info.models import User, News, Category
from info.utils.captcha.common import user_login_data
from info.utils.response_code import RET
from . import index_blu
from info import redis_store, constants

@index_blu.route('/news_list')
def news_list():

    cid = request.args.get("cid","1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")


    #校验参数
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    filters = []
    print(cid)
    print(cid!="1")
    #查询数据
    if cid!="1":
        filters.append(News.category_id == cid )
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")

    news_model_list = paginate.items
    total_page= paginate.pages
    current_page = paginate.page

    news_dict_list = []

    for news_list in news_model_list:
        news_dict_list.append(news_list.to_basic_dict())

    data = {
        "news_right_list": news_dict_list,
        "total_page":total_page,
        "current_page":current_page,
    }
    print(data)

    return jsonify(errno=RET.OK, errmsg="OK",data=data)






@index_blu.route("/")
@user_login_data
def index():

    user = g.user

    news_list = []
     #右侧新闻排行的逻辑
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []

    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    categories = Category.query.all()

    category_list = []

    for categroy in categories:
        category_list.append(categroy.to_dict())


    data = {
        "user":user.to_dict() if user  else  None,
        "news_right_list":news_dict_li,
        "category_li":category_list
    }

    return render_template('news/index.html',data=data)

#加载网站小图标，游览器启动默认加载此路由
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')