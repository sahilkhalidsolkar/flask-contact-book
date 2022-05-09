from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'afaflkaflkasfmslkfkl f;ahf;af;af;af;a;f'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, urlprefixer='/')
    app.register_blueprint(auth, urlprefixer='/')
# import all the schemas created for database
    from .models import User, Contact

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# check if the database is created or not


def create_database(application):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=application)
        print('Database created...')
