from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from shop.config import Config
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    
    from shop.main.routes import main
    from shop.user.routes import user
    from shop.inventory.routes import inventory
    from shop.customers.routes import customer

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(inventory)
    app.register_blueprint(customer)

    return app
