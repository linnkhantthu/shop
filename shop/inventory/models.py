from email.policy import default
from shop import db


class ProductTypeChoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choices = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ProductTypeChoices: {self.choices}'


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='favicon.ico')
    unit = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, default=0.0)
    extra_costs = db.Column(db.Float, default=0.0)
    percentage = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    p_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Products: {self.name}'


class UnitChoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choices = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<UnitChoices: {self.choices}'
