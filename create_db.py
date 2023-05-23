import hashlib
from learning_tool import app, db
from learning_tool import models
from config import salt

with app.app_context():
    db.create_all()

    user = models.User("Test", hashlib.pbkdf2_hmac('sha256', "Test".encode('utf-8'), salt, 100000))
    db.session.add(user)
    db.session.commit()
