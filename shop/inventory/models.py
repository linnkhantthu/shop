from shop import db


class ProductTypeChoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choices = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='favicon.ico')
    unit = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float)
    extra_costs = db.Column(db.Float)
    percentage = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    p_type = db.Column(db.String(20), nullable=False)


class UnitChoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choices = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
