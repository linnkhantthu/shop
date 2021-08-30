from shop import db, create_app

app = create_app()

db.init_app(app)
with app.app_context():
    db.create_all()
