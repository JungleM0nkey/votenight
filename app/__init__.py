#!/usr/bin/env python3

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.flask_client import OAuth
#from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)
#mail = Mail(app)

# Initialize OAuth
oauth = OAuth(app)
discord = oauth.register(
    name='discord',
    client_id=app.config['DISCORD_CLIENT_ID'],
    client_secret=app.config['DISCORD_CLIENT_SECRET'],
    access_token_url='https://discord.com/api/oauth2/token',
    access_token_params=None,
    authorize_url='https://discord.com/api/oauth2/authorize',
    authorize_params=None,
    api_base_url='https://discord.com/api/',
    client_kwargs={'scope': 'identify email'},
)

from app import routes, models

