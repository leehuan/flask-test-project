from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask
from config import Config


app = Flask(__name__)
#添加配置
app.config.from_object(Config)
#初始化数据库
db = SQLAlchemy(app)
#初始化redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_POST)
#开启当前项目csrf保护
CSRFProtect(app)
#设置session保存指定位置
Session(app)
