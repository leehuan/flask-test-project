import random
import re
from datetime import datetime

from flask import render_template, current_app, request, abort, make_response, json, jsonify, session

from info.models import User
from info.utils.response_code import RET
from . import passport_blu
from info import redis_store, constants, db
from info.utils.captcha.captcha import captcha
from info.libs.sms import CCP


@passport_blu.route("/register", method=["POST"])
def regist():
    #  获取参数
    # 检验参数
    # 获取服务器保存的验证码内容
    # 是否输入一致，如果一致创建初始化user模型，并赋值
    # 数据库添加user
    # 返回结果
    param_dice = request.json


    mobile = param_dice.get('mobile')
    image_code = param_dice.get("smscode")
    password = param_dice.get("password")

    if not all([mobile,image_code,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    try:
        real_sms_code  = redis_store.get("SMS_"+mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询失败")

    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码过期")

    if real_sms_code != image_code:
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")


    user = User()
    user.mobile = mobile
    user.nick_name = mobile
    #记录用户最后一次登录时间
    user.last_login  = datetime.now()
    #TODO  对密码做处理

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as  e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    #注册成功 保存数据session中
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name

    return jsonify(errno=RET.OK, errmsg="注册成功")


@passport_blu.route('/image_code')
def get_image_code():
    # 生成验证码并返回
    image_code_id = request.args.get("imageCodeId", None)

    # 非空判断
    if not image_code_id:
        return abort(403)

    # 获取验证码以及图片
    name, text, image = captcha.generate_captcha()
    try:
        # 将生成的验证码保存在redis中
        redis_store.setex('ImageCodeId_' + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        print(e)
        abort(500)
    response = make_response(image)
    response.headers["Content-Type"] = "image/jpg"
    return response


@passport_blu.route('/sms_code', methods=["POST"])
def send_sms_code():
    # 手机号 图片验证码 图片验证码编号
    # 校验参数
    # 发送短信
    # {mobile:18821656926 image_code:"AAAA image_code_id}
    params_dict = request.json
    mobile = params_dict.get('mobile')
    image_code = params_dict.get("image_code")
    image_code_id = params_dict.get("image_code_id")

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    if not re.match('1[35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    try:
        real_img_code = redis_store.get('ImageCodeId_' + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询失败')
    if not real_img_code:
        return jsonify(errno=RET.PARAMERR, errmsg='图片验证码过期')

    if real_img_code.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg='验证码输入错误')

    sms_code_str = "%06d" % random.randint(0, 999999)
    current_app.logger.error("验证码: %s" % sms_code_str)

    result = CCP().send_template_sms(mobile, [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES / 5], "1")

    if result != 0:
        return jsonify(errno=RET.THIRDERR, errmsg='发送短信失败')
    try:
        redis_store.setex("SMS_" + mobile, sms_code_str, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='数据保存失败')

    return jsonify(errno=RET.OK, errmsg='发送短信成功')
