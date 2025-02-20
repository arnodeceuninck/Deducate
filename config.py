import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "!cz['Z_/32BT##(k" # This is a random string
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_URL = "127.0.0.1:5432"
    POSTGRES_USER = "postgres"
    POSTGRES_PW = "postgres"  # TODO: Make more secure for server
    POSTGRES_DB = "careercoach"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                          db=POSTGRES_DB)

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = 1 # os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = "noreply.careercoach@gmail.com"
    MAIL_PASSWORD = "49f)8~y2]Y,=KF%{"
    ADMINS = ['noreply.careercoach@gmail.com']
