import traceback

from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from psycopg2 import DatabaseError

from . import posts
from db.queries import PostQueries, CommentQueries
from util.request import get_query_param_or_def, get_body_param_or_error

__posts = PostQueries()
__comments = CommentQueries()


@posts.route("/")
def index():
    page = get_query_param_or_def("page", 0, int)
    size = max(get_query_param_or_def("page", 50, int), 100)
    posts = __posts.get_most_recent(page * size, size)
    return jsonify(list(map(lambda p: p.to_dict(True), posts))), 200


@posts.route("/", methods=["POST"])
@jwt_required()
def create():
    errors = []
    title = get_body_param_or_error(errors, "title", str)
    content = get_body_param_or_error(errors, "content", str)
    if len(errors) > 0:
        return (jsonify({"errors": errors}), 400)

    id = __posts.add_post(title, content, current_user.get_id())

    return (jsonify({"id": id}), 201)


@posts.route("/<id>")
def get_one(id):
    try:
        post = __posts.get_post_by_id(id)
        if post is not None:
            return jsonify(
                post.to_dict(public=True)
            ), 200
        else:
            return '', 404
    except (Exception, DatabaseError) as error:
        print(error)
        return ({"error": "internal error"}), 500


@posts.route("/<id>/comments")
def get_comments(id):
    try:
        post = __posts.get_post_by_id(id)
        if post is not None:
            page = get_query_param_or_def("page", 0, int)
            size = max(get_query_param_or_def("page", 50, int), 100)
            comments = __comments.get_comments_by_post(post.get_id(), page * size, size)
            return jsonify(
                list(map(lambda comment: comment.to_dict(public=True), comments))
            ), 200
        else:
            return '', 404
    except (Exception, DatabaseError) as error:
        print(error)
        print(traceback.format_exc())
        return ({"error": "internal error"}), 500
    
@posts.route("/<id>/comments", methods=["POST"])
@jwt_required()
def create_comment(id):
    try:
        post = __posts.get_post_by_id(id)
        if post is not None:
            errors = []
            content = get_body_param_or_error(errors, "content", str)
            if len(errors) > 0:
                return (jsonify({"errors": errors}), 400)
            id = __comments.add_comment(content, current_user.get_id(), post.get_id())
            return (jsonify({"id": id}), 201)
        else:
            return '', 404
    except (Exception, DatabaseError) as error:
        print(error)
        print(traceback.format_exc())
        return ({"error": "internal error"}), 500