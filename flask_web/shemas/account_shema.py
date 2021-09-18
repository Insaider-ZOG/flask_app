from . import mallow
from flask_web.models import models


class AccountSchema(mallow.SQLAlchemySchema):
    class Meta:
        model = models.Account
        include_fk = True

    id = mallow.auto_field()
    user_id = mallow.auto_field()
    username = mallow.auto_field()
    email = mallow.auto_field()
    password = mallow.auto_field()
    created_on = mallow.auto_field()
    updated_on = mallow.auto_field()
    is_active = mallow.auto_field()
    is_staff = mallow.auto_field()
    is_admin = mallow.auto_field()
    rel_post = mallow.auto_field()
    rel_comment = mallow.auto_field()


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)