import uuid

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_web.models import dbase
from flask_web.models.models import Category
from flask_web.shemas.category_shema import category_schema, categories_schema
from flask_web.views import category_api


class CreateCategory(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_category = Category(
            cat_id=str(uuid.uuid4()),
            cat_name=data['cat_name']
        )

        category = Category.find_by_cat_name(new_category.cat_name)
        if category:
            return {'message': 'Category in DATABASE'}

        dbase.session.add(new_category)
        dbase.session.commit()

        result = Category.find_by_id(new_category.cat_id)

        return jsonify(categories_schema.dump(result))


class ListCategories(Resource):
    @jwt_required()
    def get(self):
        categories = Category.find_all()
        if not categories:
            return jsonify({'message': 'No comments found!'})

        result = categories_schema.dump(categories)
        return jsonify(result)


class OneDetailCategory(Resource):
    @jwt_required()
    def get(self, cat_id):
        category = Category.find_by_cat_id(cat_id)

        result = category_schema.dump(category)
        return jsonify(result)

    @jwt_required()
    def delete(self, cat_id):
        category = Category.find_by_cat_id(cat_id)

        dbase.session.delete(category)
        dbase.session.commit()
        return jsonify({'message': 'The category has been delete'})


category_api.add_resource(CreateCategory, '/create/category/')
category_api.add_resource(ListCategories, '/categories/')
category_api.add_resource(OneDetailCategory, '/category/<cat_id>/')