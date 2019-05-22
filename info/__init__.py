from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask
from config import Config,config
from flask_session import Session

app = Flask(__name__)
#添加配置
app.config.from_object(config['testconfig'])
#初始化数据库
db = SQLAlchemy(app)
#初始化redis对象
redis_store = StrictRedis(host=config['testconfig'].REDIS_HOST,port=config['testconfig'].REDIS_POST)
#开启当前项目csrf保护
CSRFProtect(app)
#设置session保存指定位置
Session(app)


