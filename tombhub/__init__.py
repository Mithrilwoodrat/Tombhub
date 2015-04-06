from flask import Flask
from flask_login import LoginManager


tombhub = Flask(__name__)
tombhub.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(tombhub)
login_manager.login_view = 'login'



from tombhub import views, models