from learning_tool import app, db

with app.app_context():
    db.create_all()
