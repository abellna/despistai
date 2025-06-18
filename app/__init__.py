from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    if not os.path.exists(os.path.join('app', 'static', 'uploads', 'locations')):
        os.makedirs(os.path.join('app', 'static', 'uploads', 'locations'))

    if not os.path.exists(os.path.join('app', 'static', 'uploads', 'items')):
        os.makedirs(os.path.join('app', 'static', 'uploads', 'items'))

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '.', 'instance', 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    return app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS