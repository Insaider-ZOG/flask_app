from . import mallow
from flask_web.models import models


class CategorySchema(mallow.SQLAlchemySchema):
    class Meta:
        model = models.Category

    id = mallow.auto_field()
    cat_id = mallow.auto_field()
    cat_name = mallow.auto_field()
    rel_post = mallow.auto_field()


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)