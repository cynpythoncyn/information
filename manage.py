from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)


class Config(object):
    """项目配置信息"""
    # base64.b64encode(os.urandom(32))
    SECRET_KEY = "2hj+Z5MJ9JJ7tISPUebJZzzQfrs3cfgDLWNspSVk+Hk="
    DEBUG = True

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/infor"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    PASSWORD = "123456"

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,password=PASSWORD)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 86400  # session 的有效期，单位是秒


app.config.from_object(Config)
db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,password=Config.PASSWORD)
CSRFProtect(app)
Session(app)
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)



@app.route('/')
def index():

    return "hello world"


if __name__ == "__main__":
    manager.run()