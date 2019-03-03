import redis
import logging

class Config(object):
    """项目配置信息"""
    # base64.b64encode(os.urandom(32))
    SECRET_KEY = "2hj+Z5MJ9JJ7tISPUebJZzzQfrs3cfgDLWNspSVk+Hk="
    # DEBUG = True
    # 默认日志等级
    LOG_LEVEL = logging.DEBUG

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


class DevelopementConfig(Config):
    """开发模式下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.ERROR

# 定义配置字典
config = {
    "development": DevelopementConfig,
    "production": ProductionConfig
}