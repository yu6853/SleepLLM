USERNAME = 'root'  # 设置登录账号
PASSWORD = '123456'  # 设置登录密码
HOST = '127.0.0.1'  # 设置主机地址
PORT = '3306'  # 设置端口号
DATABASE = 'flaskdb'  # 设置访问的数据库
auth_plugin = 'mysql_native_password'   # 设置验证插件

# 创建URI（统一资源标志符）
'''
SQLALCHEMY_DATABASE_URI的固定格式为：
'{数据库管理系统名}://{登录名}:{密码}@{IP地址}:{端口号}/{数据库名}?charset={编码格式}'
'''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

# 设置数据库的连接URI
SQLALCHEMY_DATABASE_URI = DB_URI
# 设置动态追踪修改,如未设置只会提示警告
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 设置查询时会显示原始SQL语句
SQLALCHEMY_ECHO = True

