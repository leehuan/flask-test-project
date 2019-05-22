from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask,session
from flask_script import Manager
#添加flask 与 mysql交互导入包
from flask_sqlalchemy import SQLAlchemy
#可以用来指定session保存位置
from  flask_session import Session
from flask_migrate import Migrate,MigrateCommand
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

manager = Manager(app)
#将app与db关联
Migrate(app,db)
#将迁移命令添加manger中
manager.add_command('db',MigrateCommand)

@app.route("/")
def index():
    session['name'] = 'test'
    return 'index3333'

if __name__ == '__main__':
    manager.run()