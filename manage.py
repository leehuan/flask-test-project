from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask,session
#添加flask 与 mysql交互导入包
from flask_sqlalchemy import SQLAlchemy
#可以用来指定session保存位置
from  flask_session import Session


class Config(object):
    DEBUG = True
    #配置session加密串
    SECRET_KEY = "bGVlZWVlZWVlZWh1YW5hc2Rhc2Rhc2Rhc2Rhc2Rhc2QxMjMxMmFzZGE="
    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/project1'  # 是否追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = '6379'

    #配置session
    SESSION_TYPE = 'redis'
    #开启session签名
    SESSION_USE_SIGNER = True
    #是否过期
    SESSION_PERMANENT = False
    #配置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    #配置redis
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_POST)





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

@app.route("/")
def index():
    session['name'] = 'test'
    return 'index3333'

if __name__ == '__main__':
    app.run()