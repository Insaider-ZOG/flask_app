import uuid

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_web.models import dbase
from flask_web.models.models import Comment, Post
from flask_web.shemas.comment_shema import comment_schema, comments_schema
from flask_web.shemas.post_shema import posts_schema
from flask_web.views import comment_api


class CreateComment(Resource):
    @jwt_required()
    def post(self, post_id):
        current_user = get_jwt_identity()
        data = request.get_json()
        new_comment = Comment(
            comm_id=str(uuid.uuid4()),
            text=data['text'],
            creator=current_user,
            post_id=post_id
        )
        dbase.session.add(new_comment)
        dbase.session.commit()

        result = Comment.find_by_comm_id(new_comment.comm_id)

        return jsonify(comment_schema.dump(result))


class ListComment(Resource):
    def get(self):
        comments = Comment.find_all()
        if not comments:
            return jsonify({'message': 'No comments found!'})

        result = comments_schema.dump(comments)
        return jsonify(result)


class ListCommentPost(Resource):
    def get(self, post_id):
        post = Post.find_by_post_id(post_id)
        if not post:
            return jsonify({'message': 'No post found!'})

        result = posts_schema.dump(post)
        return jsonify(result)


class OneDetailComment(Resource):
    @jwt_required()
    def get(self, post_id, comm_id):
        current_account = get_jwt_identity()

        post = Post.find_by_post_id(post_id)
        if not post:
            return jsonify({'message': 'No post found!'})

        comment = Comment.find_by_comm_id(comm_id)
        if not comment:
            return jsonify({'message': 'No comment found!'})

        if comment.creator != current_account:
            return {'message': 'Cannot perform that function!'}

        result = comment_schema.dump(comment)
        return jsonify(result)

    @jwt_required()
    def put(self, post_id, comm_id):
        current_user = get_jwt_identity()

        post = Post.find_by_post_id(post_id)
        if not post:
            return jsonify({'message': 'No post found!'})

        comment = Comment.find_by_comm_id(comm_id)
        if not comment:
            return jsonify({'message': 'No comment found!'})

        if comment.creator != current_user:
            return jsonify({'message': 'Cannot perform that function!'})

        data = request.get_json()

        if 'text' in data:
            comment.title = data['text']

        dbase.session.commit()
        return {'message': 'The comment has been promoted!'}

    @jwt_required()
    def delete(self, post_id, comm_id):
        current_user = get_jwt_identity()

        post = Post.find_by_post_id(post_id)
        if not post:
            return jsonify({'message': 'No post found!'})

        comment = Comment.find_by_comm_id(comm_id)
        if not comment:
            return jsonify({'message': 'No comment found!'})

        if comment.creator != current_user:
            return jsonify({'message': 'Cannot perform that function!'})

        dbase.session.delete(comment)
        dbase.session.commit()
        return jsonify({'message': 'The comment has been delete'})


comment_api.add_resource(CreateComment, '/post/<post_id>/create/comment/')
comment_api.add_resource(ListComment, '/comments/')
comment_api.add_resource(ListCommentPost, '/post/<post_id>/comments/')
comment_api.add_resource(OneDetailComment, '/post/<post_id>/comment/<comm_id>/')