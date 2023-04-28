import random, secrets

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
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
        return f"ID: {self.id}, Subject: {self.name}, Creator: {self.creator}\n"


class Questions(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    question: db.Mapped[str]
    answer: db.Mapped[str]
    subject: db.Mapped[str] = db.mapped_column(db.ForeignKey(Subject.id))
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))

    def __repr__(self):
        return f"ID: {self.id}, Question: {self.question}, Answer: {self.answer}, Subject: {self.subject}, Creator: {self.creator}\n"


@app.get("/")
def index():
    session["current_user"] = 1
    session["selected_subject"] = 4
    session["question"] = ""
    session["answer"] = ""
    session["flipped"] = False

    current_user_subjects = db.session.execute(db.select(Subject.name).filter(Subject.creator == session["current_user"])).all()
    get_random_question()

    return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])


def get_random_question():
    selected_subject_questions = db.session.execute(db.select(Questions).filter(Questions.creator == session["current_user"]).filter(Questions.subject == session["selected_subject"])).all()
    selected_question_row = random.choice(selected_subject_questions)
    session["question"] = selected_question_row._mapping["Questions"].question
    session['answer'] = selected_question_row._mapping["Questions"].answer


@app.route("/clicked")
def clicked():
    current_user_subjects = db.session.execute(db.select(Subject.name).filter(Subject.creator == session["current_user"])).all()

    link = request.args.get("link")

    if link != "flip":
        session["flipped"] = False

    if link == "new_quiz":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "subjects":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "progress":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "login":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "new_subject":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "flip":
        if not session["flipped"]:
            session["flipped"] = True
            return render_template("index.html", subjects=current_user_subjects, card_text=session["answer"], flipped=session["flipped"])
        else:
            session["flipped"] = False
            return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])
    elif link == "correct_answer":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"],flipped=session["flipped"])
    elif link == "wrong_answer":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"],flipped=session["flipped"])
    else:
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"])


if __name__ == "__main__":
    app.run()
