import hashlib
from learning_tool import app, db, User, salt

with app.app_context():
    db.create_all()

    user = User("Lewin", hashlib.pbkdf2_hmac('sha256', "GeheimesPasswort123".encode('utf-8'), salt, 100000))
    db.session.add(user)
    user = User("Test", hashlib.pbkdf2_hmac('sha256', "Test".encode('utf-8'), salt, 100000))
    db.session.add(user)
    db.session.commit()
