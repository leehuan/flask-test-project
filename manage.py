import logging

from flask_script import Manager
from flask import session
from flask_migrate import Migrate,MigrateCommand

from info import configapp,db

#修改开发环境，进行添加以及修改
app = configapp('development')

manager = Manager(app)
#将app与db关联
Migrate(app,db)
#将迁移命令添加manger中
manager.add_command('db',MigrateCommand)

@app.route("/")
def index():
    return 'index3333'

if __name__ == '__main__':
    manager.run()