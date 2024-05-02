DEBUG = True

USERNAME = 'root'
PASSWORD = 'Bola@2020'
SERVER = '85.239.239.196'
PORT = '3306'
DB = 'api_flask'

SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = True

#SQLALCHEMY_ENGINE_OPTIONS = {
    #'pool_pre_ping': True,
    #'pool_recycle': 300,
    #'pool_size': 10,
    #'max_overflow': 20
#}
