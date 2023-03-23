from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Configuration

from services.password.argonpassword import Argon2PasswordService
from db import Connection
from db.queries import UserQueries, PostQueries, CommentQueries


class Container(DeclarativeContainer):
    config = Configuration(strict=True)

    password_service = Singleton(Argon2PasswordService)

    connection_pool = Singleton(
        Connection,
        host=config.db_host,
        database=config.db_database,
        user=config.db_user,
        password=config.db_password,
        port=config.db_port,
        retries=config.db_retries,
        min_conn=config.db_min_connections,
        max_conn=config.db_max_connections,
    )

    user_queries = Singleton(
        UserQueries,
        connection=connection_pool,
        hasher=password_service,
    )

    post_queries = Singleton(PostQueries, connection=connection_pool)

    comment_queries = Singleton(CommentQueries, connection=connection_pool)
