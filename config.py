import logging

from redis import StrictRedis
#配置常用工具
class Config(object):
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

    #设置日志等级
    LOG_LEVEL =logging.DEBUG

class Development(Config):
    '''开发环境'''
    DEBUG = True


class ReleseConfig(Config):
    '''生产环境'''
    DEBUG = False
    #修改ip以及port 或者用户名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/project1'  # 是否追踪数据库的修改
    LOG_LEVEL = logging.WARNING

class TestConfig(Config):
    '''单元测试环境下配置'''
    DEBUG = True
    TESTING = True

config = {
    'development': Development,
    'release': ReleseConfig,
    'testconfig':TestConfig
}