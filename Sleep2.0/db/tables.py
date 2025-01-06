from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()   # 采用延迟初始化方式，在使用数据库之前务必进行初始化操作
