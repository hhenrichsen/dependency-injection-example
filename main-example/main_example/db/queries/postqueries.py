from uuid import UUID


from db import pool
from db.models import Post, User
from util.valid import validate_param


class PostQueries:
    def get_post_by_id(self, id: str):
        validate_param('id', id, str)

        with pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    posts.id as id, title, content, posts.created as created,
                    users.id as userid, users.username as username, users.display_name as display_name, users.email as email
                FROM posts
                LEFT JOIN users on users.id = posts.userid
                WHERE posts.id=%s;
                """,
                (id, ),
            )

            results = cursor.fetchmany()
            if len(results) == 1:
                result = results[0]
                # Probably not the best way to do this, but it'll work for now.
                return Post(*result[:-4], User(*result[-4:]))
            else:
                return None

    def get_most_recent(self, offset: int, count: int = 50):
        validate_param('offset', offset, int)
        validate_param('count', count, int)

        with pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    posts.id as id, title as title, content, posts.created as created,
                    users.id as userid, users.username as username, users.display_name as display_name, users.email as email
                FROM posts
                LEFT JOIN users on users.id = posts.userid
                WHERE posts.visible=true AND users.active=true ORDER BY posts.created LIMIT %s OFFSET %s;
                """,
                (count, offset),
            )

            results = []
            for row in cursor:
                # Probably not the best way to do this, but it'll work for now.
                results.append(Post(*row[:-4], User(*row[-4:])))

            return results

    def add_post(self, title: str, content: str, author_id: str | UUID):
        validate_param('title', title, str)
        validate_param('content', content, str)
        validate_param('author_id', author_id, [str, UUID])

        with pool.getconn() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO posts(title, content, userid) 
                VALUES (%s, %s, %s) 
                RETURNING id;
                """,
                (title, content, str(author_id)),
            )
            
            res = cursor.fetchone()
            return res[0]
