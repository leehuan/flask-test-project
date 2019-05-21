from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask
#添加flask 与 mysql交互导入包
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    DEBUG = True
    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/project1'  # 是否追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = '6379'


app = Flask(__name__)
#添加配置
app.config.from_object(Config)
#初始化数据库
db = SQLAlchemy(app)
#初始化redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_POST)
#开启当前项目csrf保护
CSRFProtect(app)


@app.route("/")
def index():
    return 'index3333'

if __name__ == '__main__':
    app.run()