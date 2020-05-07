import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #sql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATBASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #recaptcha
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LcFCfQUAAAAANdXxEeHfDzKu_NkWhgIYR5Ht2-0'
    RECAPTCHA_PRIVATE_KEY = '6LcFCfQUAAAAAK7xSi0VLQ1fsCRWgr36t5vKtz6o'
    RECAPTCHA_OPTIONS = {'theme':'white'}
    #mail server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['votenight.pw@gmail.com']