from . import mallow
from flask_web.models import models


class CommentSchema(mallow.SQLAlchemySchema):
    class Meta:
        model = models.Comment

    id = mallow.auto_field()
    comm_id = mallow.auto_field()
    text = mallow.auto_field()
    created_on = mallow.auto_field()
    post_id = mallow.auto_field()
    creator = mallow.auto_field()


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)