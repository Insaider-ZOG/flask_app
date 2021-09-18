import uuid

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,\
    set_access_cookies, set_refresh_cookies

from flask_web.models import dbase
from flask_web.models.models import Account, Post
from flask_web.shemas.account_shema import account_schema, accounts_schema
from flask_web.shemas.post_shema import posts_schema
from flask_web.views import account_api


class RegisterAccount(Resource):
    def post(self):
        data = request.get_json()
        new_user = Account(
            user_id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            secret=data['password']
        )

        name = Account.find_by_name(new_user.username)
        if name:
            return {'message': 'User in DATABASE'}

        mail = Account.find_by_email(new_user.email)
        if mail:
            return {'message': 'email in DATABASE'}

        dbase.session.add(new_user)
        dbase.session.commit()

        result = Account.find_by_name(new_user.username)

        return jsonify(account_schema.dump(result))


class LoginAccount(Resource):
    def post(self):
        data = request.get_json()
        account = Account.find_by_name(username=data.get('username'))
        if not account:
            return {'message': 'Could not verify username'}

        authorized = account.check_password(data.get('password'))
        if not authorized:
            return {'message': 'Could not verify Password'}

        else:
            access_token = create_access_token(identity=account.user_id)
            refresh_token = create_refresh_token(identity=account.user_id)

            resp = jsonify(login=True)

            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return {'access_token': access_token, 'refresh_token': refresh_token}


class ListAccount(Resource):
    def get(self):
        account = Account.find_all()
        if not account:
            return jsonify({'message': 'No user found!'})

        result = accounts_schema.dump(account)
        return jsonify(result)


class ListAccountPosts(Resource):
    def get(self, user_id):
        posts = Post.find_by_creator(user_id)
        if not posts:
            return jsonify({'message': 'No post found!'})

        result = posts_schema.dump(posts)
        return jsonify(result)


class OneDetailAccount(Resource):
    @jwt_required()
    def get(self, user_id):
        account = Account.find_by_account_id(user_id)
        current_account = get_jwt_identity()
        if not account:
            return jsonify({'message': 'No user found!'})

        if account.user_id != current_account:
            return {'message': 'Cannot perform that function!'}

        result = account_schema.dump(account)
        return jsonify(result)

    @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        account = Account.find_by_account_id(user_id)

        if not account:
            return {'message': 'No user found!'}

        if 'username' in data:
            account.username = data['username']
        if 'email' in data:
            account.email = data['email']

        dbase.session.commit()
        return {'message': 'The user has been promoted!'}

    @jwt_required()
    def delete(self, user_id):
        current_user = get_jwt_identity()
        account = Account.find_by_account_id(user_id)

        if not account:
            return jsonify({'message': 'No user found!'})

        if account.user_id != current_user:
            return jsonify({'message': 'Cannot perform that function!'})

        dbase.session.delete(account)
        dbase.session.commit()
        return jsonify({'message': 'The user has been delete'})


account_api.add_resource(RegisterAccount, '/register/')
account_api.add_resource(LoginAccount, '/login/')
account_api.add_resource(ListAccount, '/users/')
account_api.add_resource(OneDetailAccount, '/user/<user_id>/')
account_api.add_resource(ListAccountPosts, '/user/<user_id>/posts/')