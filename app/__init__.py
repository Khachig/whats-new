import os

from flask import Flask
from dotenv import load_dotenv

# init app
app = Flask(__name__)
load_dotenv()

# init config
if os.getenv('ENV') == 'development':
    app.config.from_object('config.DevelopmentConfig')
else:
    app.config.from_object('config.BaseConfig')

from app import routes
