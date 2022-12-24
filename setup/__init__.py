from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'iudsdbciud ccdoi'
    # tells flask where our sql database is located
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialize database by giving it the app
    db.init_app(app)

    from .features import features

    app.register_blueprint(features, url_prefix='/')
    # its empty in the decorator if it had something it would be /auth/hello
    #app.register_blueprint(auth, url_prefix='/auth/hello')
    # we need to import to make sure it defines the databases before you create them
    from .models import Nodes

    # this is new code stack overflow
    # db was not created in same directory take note
    with app.app_context():
        db.create_all()




    return app