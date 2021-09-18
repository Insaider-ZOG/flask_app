import uuid

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_web.models import dbase
from flask_web.models.models import Post, Category
from flask_web.shemas.post_shema import post_schema, posts_schema
from flask_web.views import post_api


class CreatePost(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        new_post = Post(
            post_id=str(uuid.uuid4()),
            creator=current_user,
            title=data['title'],
            content=data['content'],
            category=data['category']
        )

        category = Category.find_by_cat_name(new_post.category)

        if not category:
            return jsonify({'message': 'No category found!'})

        post_title = Post.find_by_title(new_post.title)
        if post_title:
            return {'message': 'Post in DATABASE'}

        dbase.session.add(new_post)
        dbase.session.commit()

        result = Post.find_by_title(new_post.title)

        return jsonify(post_schema.dump(result))


class OneDetailPost(Resource):
    @jwt_required()
    def get(self, post_id):
        current_account = get_jwt_identity()
        post = Post.find_by_post_id(post_id)
        if not post:
            return jsonify({'message': 'No post found!'})

        if post.creator != current_account:
            return {'message': 'Cannot perform that function!'}

        result = post_schema.dump(post)
        return jsonify(result)

    @jwt_required()
    def put(self, post_id):
        current_user = get_jwt_identity()
        data = request.get_json()
        post = Post.find_by_post_id(post_id)

        if not post:
            return {'message': 'No user found!'}

        if post.creator != current_user:
            return jsonify({'message': 'Cannot perform that function!'})

        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']

        dbase.session.commit()
        return {'message': 'The post has been promoted!'}

    @jwt_required()
    def delete(self, post_id):
        current_user = get_jwt_identity()
        post = Post.find_by_post_id(post_id)

        if not post:
            return jsonify({'message': 'No post found!'})

        if post.creator != current_user:
            return jsonify({'message': 'Cannot perform that function!'})

        dbase.session.delete(post)
        dbase.session.commit()
        return jsonify({'message': 'The user has been delete'})


class ListPost(Resource):
    def get(self):
        posts = Post.find_all()
        if not posts:
            return jsonify({'message': 'No user found!'})

        result = posts_schema.dump(posts)
        return jsonify(result)


post_api.add_resource(ListPost, '/posts/')
post_api.add_resource(CreatePost, '/post/create/')
post_api.add_resource(OneDetailPost, '/post/<post_id>/')