from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_web.models import dbase


class Account(dbase.Model, UserMixin):
    __tablename__ = 'accounts'
    id = dbase.Column(dbase.Integer, primary_key=True)
    user_id = dbase.Column(dbase.String(50), unique=True)
    username = dbase.Column(dbase.String(30), unique=True)
    email = dbase.Column(dbase.String(100), unique=True)
    password = dbase.Column(dbase.String(100), unique=True)
    created_on = dbase.Column(dbase.DateTime, server_default=dbase.func.now())
    updated_on = dbase.Column(dbase.DateTime, server_default=dbase.func.now(), server_onupdate=dbase.func.now())
    is_active = dbase.Column(dbase.Boolean, default=None)
    is_staff = dbase.Column(dbase.Boolean, default=None)
    is_admin = dbase.Column(dbase.Boolean, default=None)
    rel_post = dbase.relationship('Post', backref='accounts')
    rel_comment = dbase.relationship('Comment', backref='accounts')

    def __init__(self, username, email, user_id, secret):
        self.username = username
        self.user_id = user_id
        self.email = email
        self.password = generate_password_hash(secret)
        self.is_active = True
        self.is_staff = False
        self.is_admin = False

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"<Account : {self.username}>"

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_account_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class Category(dbase.Model):
    __tablename__ = 'categories'
    id = dbase.Column(dbase.Integer, primary_key=True)
    cat_id = dbase.Column(dbase.String(50), unique=True)
    cat_name = dbase.Column(dbase.String(100), unique=True)
    rel_post = dbase.relationship('Post', backref='categories')

    def __init__(self, cat_id, cat_name):
        self.cat_id = cat_id
        self.cat_name = cat_name

    def __repr__(self):
        return f"<Category : {self.cat_name}>"

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_cat_id(cls, cat_id):
        return cls.query.filter_by(cat_id=cat_id).first()

    @classmethod
    def find_by_cat_name(cls, cat_name):
        return cls.query.filter_by(cat_name=cat_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class Post(dbase.Model):
    __tablename__ = 'posts'
    id = dbase.Column(dbase.Integer, primary_key=True)
    post_id = dbase.Column(dbase.String(50), unique=True)
    title = dbase.Column(dbase.String(100), unique=True)
    content = dbase.Column(dbase.String(300))
    created_on = dbase.Column(dbase.DateTime, server_default=dbase.func.now())
    is_published = dbase.Column(dbase.Boolean, default=None)
    creator = dbase.Column(dbase.String(), dbase.ForeignKey('accounts.user_id'))
    category = dbase.Column(dbase.String(), dbase.ForeignKey('categories.cat_id'))
    rel_comment = dbase.relationship('Comment', backref='posts')

    def __init__(self, post_id, title, content, creator, category):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.is_published = True
        self.creator = creator
        self.category = category

    def __repr__(self):
        return f"<Post : {self.title}>"

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_creator(cls, creator):
        return cls.query.filter_by(creator=creator).all()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()


class Comment(dbase.Model):
    __tablename__ = 'comments'
    id = dbase.Column(dbase.Integer, primary_key=True)
    comm_id = dbase.Column(dbase.String(50), unique=True)
    text = dbase.Column(dbase.String(100), unique=True)
    created_on = dbase.Column(dbase.DateTime, server_default=dbase.func.now())
    creator = dbase.Column(dbase.String(), dbase.ForeignKey('accounts.user_id'))
    post_id = dbase.Column(dbase.String(), dbase.ForeignKey('posts.post_id'))

    def __init__(self, comm_id, creator,  text, post_id):
        self.comm_id = comm_id
        self.text = text
        self.creator = creator
        self.post_id = post_id

    @classmethod
    def find_by_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id).first()

    @classmethod
    def find_by_comm_id(cls, comm_id):
        return cls.query.filter_by(comm_id=comm_id).first()

    @classmethod
    def find_by_creator(cls, creator):
        return cls.query.filter_by(creator=creator).all()

    @classmethod
    def find_by_text(cls, text):
        return cls.query.filter_by(text=text).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f"<Comment: {self.comm_id}>"