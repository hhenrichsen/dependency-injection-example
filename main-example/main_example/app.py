from os import getenv

from dotenv import load_dotenv
load_dotenv()

from flask import Flask

from db.queries import UserQueries
from db.models import User
from blueprints.auth import auth
from blueprints.posts import posts
from flask_jwt_extended import JWTManager

from container import Container
from dependency_injector.wiring import Provide, inject

def create_app() -> Flask:
    container = Container()

    container.config.jwt_key.from_env("JWT_KEY", required=True)

    container.config.db_host.from_env("DB_HOST", required=True)
    container.config.db_database.from_env("DB_DATABASE", required=True)
    container.config.db_user.from_env("DB_USER", required=True)
    container.config.db_password.from_env("DB_PASSWORD", required=True)
    container.config.db_port.from_env("DB_PORT", 5432, as_=int)
    container.config.db_retries.from_env("DB_RETRIES", 10, as_=int)
    container.config.db_min_connections.from_env("DB_MIN_CONNECTIONS", 4, as_=int)
    container.config.db_max_connections.from_env("DB_MAX_CONNECTIONS", 16, as_=int)
    
    container.wire(packages=["blueprints"])

    container.connection_pool().connect()

    app = Flask(__name__)
    app.container = container
    app.config['JWT_SECRET_KEY'] = container.config.jwt_key()
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(posts, url_prefix="/posts")

    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user: User):
        return user.get_id()

    @jwt.user_lookup_loader
    @inject
    def user_lookup_loader(_, data):
        return container.user_queries().get_user_by_id(data['sub'])
    
    return app