import flask
from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_learning_tool.sqlite"

db = SQLAlchemy(app)


class User(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    username: db.Mapped[str]
    password: db.Mapped[str]

    def __repr__(self):
        return f"ID: {self.id}, Username: {self.username}, Password: {self.password}\n"


class Subject(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str]
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))

    def __repr__(self):
        return f"ID: {self.id}, Subject: {self.name}, Creator: {self.creator.username}\n"


class Questions(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    question: db.Mapped[str]
    answer: db.Mapped[str]
    subject: db.Mapped[str] = db.mapped_column(db.ForeignKey(Subject.id))
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))

    def __repr__(self):
        return f"ID: {self.id}, Question: {self.question}, Answer: {self.answer}, Subject: {self.subject.name}, Creator: {self.creator.username}\n"


@app.get("/")
def index():
    all_subjects = db.session.execute(db.select(Subject).filter(Subject.id == 1)).scalars().all()
    return render_template("index.html", subjects=all_subjects)


@app.route("/clicked")
def clicked():
    link = request.args.get("link")
    if link == "new_quiz":
        print("NEW QUIZ")
    else:
        print("else")
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
