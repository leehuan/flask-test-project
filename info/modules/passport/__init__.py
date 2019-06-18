#登录注册的业务逻辑
from flask import Blueprint

passport_blu = Blueprint('passport',__name__,url_prefix="/passprot")


from . import views