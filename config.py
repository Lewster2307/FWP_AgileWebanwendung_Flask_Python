import secrets

SECRET_KEY = secrets.token_hex(16)
SQLALCHEMY_DATABASE_URI = "sqlite:///database_learning_tool.sqlite"

# Used for password hashing
salt = b'\x19\xab\x96\x02G\xb8\xd8ZP\xac\x1b\x91\x0e\xa9\x87m,\rhT\xca\xa7\xdd\x18\xf61\x10\'"/<\xf4'
