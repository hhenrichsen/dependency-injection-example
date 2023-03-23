from uuid import UUID

from db.models import Comment


from db import Connection
from db.models import Post, User
from util.valid import validate_param


class CommentQueries:
    def __init__(
        self,
        connection: Connection,
    ):
        self.__connection = connection

    def get_comment_by_id(self, id: str):
        validate_param('id', id, str)
        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    comments.id as id, content as content, comments.created as created
                    users.id as userid, users.username as username, users.display_name as display_name, users.email as email,
                    comments.postid as post_id
                FROM comments
                LEFT JOIN users on users.id = comments.userid
                WHERE posts.id=%s;
                """,
                (id, ),
            )

            results = cursor.fetchmany()
            if len(results) == 1:
                result = results[0]
                # Probably not the best way to do this, but it'll work for now.
                return Comment(*result[:-5], User(*result[-5:-1]), result[-1])
            else:
                return None

    def get_comments_by_post(self, post_id: str | UUID, offset: int, count: int = 50):
        validate_param('post_id', post_id, [str, UUID])
        validate_param('offset', offset, int)
        validate_param('count', count, int)

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    comments.id as id, content as content, comments.created as created,
                    users.id as userid, users.username as username, users.display_name as display_name, users.email as email,
                    comments.postid as post_id
                FROM comments
                LEFT JOIN users on users.id = comments.userid
                WHERE comments.visible=true AND users.active=true AND comments.postid=%s ORDER BY comments.created LIMIT %s OFFSET %s;
                """,
                (str(post_id), count, offset),
            )

            results = []
            for row in cursor:
                # Probably not the best way to do this, but it'll work for now.
                results.append(Comment(*row[:-5], User(*row[-5:-1]), row[-1]))

            return results

    def add_comment(self, content: str, author_id: str | UUID, post_id: str | UUID):
        validate_param('content', content, str)
        validate_param('author_id', author_id, [str, UUID])
        validate_param('post_id', post_id, [str, UUID])

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO comments(content, userid, postid) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """,
                (content, str(author_id), str(post_id)),
            )
            
            res = cursor.fetchone()
            return res[0]
