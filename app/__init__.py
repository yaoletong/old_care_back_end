from flask import Flask
from flask_httpauth import HTTPBasicAuth

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

from app import config


app = Flask(__name__)

CORS(app, supports_credentials=True)  # 跨域


db = SQLAlchemy()
app.config.from_object(config)
db.init_app(app)  # 绑定到我们到应用程序
db.app = app


