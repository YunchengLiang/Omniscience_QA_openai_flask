HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'oa_project'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'


MAIL_SERVER ="smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = "870327837@qq.com"
MAIL_PASSWORD = "ekhcmczqnsbqbdfb"
MAIL_DEFAULT_SENDER = "870327837@qq.com"

SECRET_KEY = "akdajfwejfwecnwejnfiwenc"