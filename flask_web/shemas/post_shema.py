from . import mallow
from flask_web.models import models


class PostSchema(mallow.SQLAlchemySchema):
    class Meta:
        model = models.Post
        include_fk = True

    id = mallow.auto_field()
    post_id = mallow.auto_field()
    title = mallow.auto_field()
    content = mallow.auto_field()
    created_on = mallow.auto_field()
    is_published = mallow.auto_field()
    creator = mallow.auto_field()
    category = mallow.auto_field()
    rel_comment = mallow.auto_field()


post_schema = PostSchema()
posts_schema = PostSchema(many=True)