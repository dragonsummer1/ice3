import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    # SQLite数据库文件
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'community_forum.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 登录配置
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # 生产环境应设为True（使用HTTPS）
    
    # CSRF保护
    WTF_CSRF_TIME_LIMIT = 3600  # CSRF令牌有效期（秒）
    
    # 调试配置
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True
    SQLALCHEMY_ECHO = False  # 是否打印SQL语句
    WTF_CSRF_ENABLED = False  # 开发环境禁用CSRF以支持跨域请求

class TestingConfig(Config):
    # 测试环境配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # 测试时禁用CSRF

class ProductionConfig(Config):
    # 生产环境配置
    SESSION_COOKIE_SECURE = True  # 生产环境启用HTTPS cookie
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

# 配置映射，方便根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}