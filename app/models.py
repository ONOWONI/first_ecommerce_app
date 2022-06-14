from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email =db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255))
    cash = db.Column(db.Float, nullable=False, default=0.00)
    seller = db.Column(db.Boolean,nullable=False, default="False")
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    my_cart = db.relationship('Cart', backref='owner', lazy=True)
    my_cart = db.relationship('Product', backref='seller', lazy=True)


    def __repr__(self):
        return f"user ({self.email}, {self.id})"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"cart ({self.user_id}, {self.quantity}, {self.product_id})"



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    product_pic = db.Column(db.String(60), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"Product ({self.name}, {self.id}, {self.price})"
