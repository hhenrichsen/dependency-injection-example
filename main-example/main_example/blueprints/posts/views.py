import traceback

from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from psycopg2 import DatabaseError
from dependency_injector.wiring import Provide, inject
from container import Container

from . import posts
from db.queries import PostQueries, CommentQueries
from util.request import get_query_param_or_def, get_body_param_or_error


@posts.route("/")
@inject
def index(posts: PostQueries = Provide[Container.post_queries]):
    page = get_query_param_or_def("page", 0, int)
    size = max(get_query_param_or_def("page", 50, int), 100)
    posts = posts.get_most_recent(page * size, size)
    return jsonify(list(map(lambda p: p.to_dict(True), posts))), 200


@posts.route("/", methods=["POST"])
@jwt_required()
@inject
def create(posts: PostQueries = Provide[Container.post_queries]):
    errors = []
    title = get_body_param_or_error(errors, "title", str)
    content = get_body_param_or_error(errors, "content", str)
    if len(errors) > 0:
        return (jsonify({"errors": errors}), 400)

    id = posts.add_post(title, content, current_user.get_id())

    return (jsonify({"id": id}), 201)


@inject
@posts.route("/<id>")
def get_one(id: str, posts: PostQueries = Provide[Container.post_queries]):
    try:
        post = posts.get_post_by_id(id)
        if post is not None:
            return jsonify(post.to_dict(public=True)), 200
        else:
            return "", 404
    except (Exception, DatabaseError) as error:
        print(error)
        return ({"error": "internal error"}), 500


@posts.route("/<id>/comments")
@inject
def get_comments(
    id: str,
    posts: PostQueries = Provide[Container.post_queries],
    comments: CommentQueries = Provide[Container.comment_queries],
):
    try:
        post = posts.get_post_by_id(id)
        if post is not None:
            page = get_query_param_or_def("page", 0, int)
            size = max(get_query_param_or_def("page", 50, int), 100)
            comment_list = comments.get_comments_by_post(
                post.get_id(), page * size, size
            )
            return (
                jsonify(
                    list(
                        map(lambda comment: comment.to_dict(public=True), comment_list)
                    )
                ),
                200,
            )
        else:
            return "", 404
    except (Exception, DatabaseError) as error:
        print(error)
        print(traceback.format_exc())
        return ({"error": "internal error"}), 500


@posts.route("/<id>/comments", methods=["POST"])
@jwt_required()
@inject
def create_comment(
    id: str,
    posts: PostQueries = Provide[Container.post_queries],
    comments: CommentQueries = Provide[Container.comment_queries],
):
    try:
        post = posts.get_post_by_id(id)
        if post is not None:
            errors = []
            content = get_body_param_or_error(errors, "content", str)
            if len(errors) > 0:
                return (jsonify({"errors": errors}), 400)
            id = comments.add_comment(content, current_user.get_id(), post.get_id())
            return (jsonify({"id": id}), 201)
        else:
            return "", 404
    except (Exception, DatabaseError) as error:
        print(error)
        print(traceback.format_exc())
        return ({"error": "internal error"}), 500
