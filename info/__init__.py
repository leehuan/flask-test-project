import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask
from config import Config,config
from flask_session import Session

db = SQLAlchemy()

def setup_log(config_name):
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    file_log_handler = RotatingFileHandler("logs/log",maxBytes=1024*1024*100,backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d%(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


def configapp(config_name):
    #配置日志
    setup_log(config_name)
    #创建flask
    app = Flask(__name__)
    #添加配置
    app.config.from_object(config[config_name])
    #初始化数据库
    db.init_app(app)
    #初始化redis对象
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_POST)
    #开启当前项目csrf保护
    CSRFProtect(app)
    #设置session保存指定位置
    Session(app)
    return app


