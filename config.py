# flask配置文件
import os


class BaseConfig:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '1234567890@ABCDEFGHIJKLMN'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///novels.db'


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///novels.db'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///novels.db'
    DEBUG = False
    TESTING = False
