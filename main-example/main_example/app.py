from os import getenv

from dotenv import load_dotenv
load_dotenv()

from flask import Flask

from db.queries import UserQueries
from db.models import User
from blueprints.auth import auth
from blueprints.posts import posts
from flask_jwt_extended import JWTManager

__users = UserQueries()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = getenv("JWT_KEY")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(posts, url_prefix="/posts")

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.get_id()

@jwt.user_lookup_loader
def user_lookup_loader(_, data):
    return __users.get_user_by_id(data['sub'])