from flask import flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.models import Product

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.seller == True:
            return True
        return False

    form_excluded_columns = ('seller_id')


    def on_model_change(self, form, Product, is_created):
        if is_created:
            Product.seller_id = current_user.id
            return True




    def delete(self, Product):
        if current_user.id != Product.seller_id:
            can_edit = False
            return can_edit


