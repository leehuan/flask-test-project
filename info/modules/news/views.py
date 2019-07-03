from flask import render_template, jsonify

from info.models import News
from info.utils.response_code import RET
from . import news_blu

@news_blu.route('/<int:news_id>')
def news_detail(news_id):

    try:
        new = News.query.filter(News.id==news_id).first()
    except Exception as e:
        return jsonify(errno=RET.DATAERR, errmsg="数据查询错误")




    # data = {
    #     "title":new.title,
    #     "digest":new.digest,
    # }


    return  render_template("news/detail.html",data = new.to_basic_dict())