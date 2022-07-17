import random
import string

DIALECT = 'mysql'  # 要用是什么数据库，我使用的是 mysql
DRIVER = 'pymysql'  # 连接数据库驱动，pymysql 是 mysql 的驱动
USERNAME = 'root'  # 用户名 ，你的数据库用户名
PASSWORD = 'llk~8025'  # 密码 ，你的数据库密码
HOST = 'bj-cynosdbmysql-grp-emlryw58.sql.tencentcdb.com'  # 服务器 ，数据库所在服务器的ip，本地即 127.0.0.1
PORT = '27327'  # 端口 ，数据库的默认端口 3306
DATABASE = 'old_care'  # 数据库名 ，你需要链接的具体数据库的名字 ，这里是报修数据库的名字

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)  # 拼接成数据库的 URI ，一般不需要修改
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 用于追踪数据库修改 ， 默认为True ，设置为 True 会增加内存消耗
JSON_AS_ASCII = False

# 密钥，可随意修改
SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))