from flask import  Flask
#添加flask 与 mysql交互导入包
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    DEBUG = True
    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/project1'  # 是否追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
#添加配置
app.config.from_object(Config)

#初始化数据库
db = SQLAlchemy(app)


@app.route("/")
def index():
    return 'index3333'

if __name__ == '__main__':
    app.run()