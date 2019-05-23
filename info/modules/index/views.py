from . import index_blu
from info import redis_store
@index_blu.route("/")
def index():
    redis_store.set("test","asdasdasd")
    return 'index3333'