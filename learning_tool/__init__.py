from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from learning_tool import views

# --SESSION KEYS--
# session["logged_in"]
# session["current_user_id"]
# session["selected_subject_id"]
# session["question_id"]
# session["question"]
# session["answer"]
# session["flipped"]


if __name__ == "__main__":
    app.run()
