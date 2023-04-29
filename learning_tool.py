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
        return f"User ID: {self.id}, Username: {self.username}"


class Subject(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str]
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))

    def __repr__(self):
        return f"Subject ID: {self.id}, Name: {self.name}"


class Questions(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    question: db.Mapped[str]
    answer: db.Mapped[str]
    subject: db.Mapped[str] = db.mapped_column(db.ForeignKey(Subject.id))
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))
    count_correct: db.Mapped[int]
    count_wrong: db.Mapped[int]

    def __repr__(self):
        return f"Question ID: {self.id}, Subject: {self.subject}"


@app.get("/")
def index():
    session["current_user"] = 1
    session["selected_subject"] = 1
    session["question_id"] = 0
    session["question"] = ""
    session["answer"] = ""
    session["flipped"] = False

    current_user_subjects = db.session.execute(db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user"])).all()
    get_random_question()

    return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])


def get_random_question():
    selected_subject_questions = db.session.execute(db.select(Questions).filter(Questions.creator == session["current_user"]).filter(Questions.subject == session["selected_subject"])).all()
    selected_question_row = random.choice(selected_subject_questions)
    session["question_id"] = selected_question_row._mapping["Questions"].id
    session["question"] = selected_question_row._mapping["Questions"].question
    session['answer'] = selected_question_row._mapping["Questions"].answer


@app.route("/clicked")
def clicked():
    current_user_subjects = db.session.execute(db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user"])).all()

    link = request.args.get("link")

    if link != "flip":
        session["flipped"] = False

    if link == "new_quiz":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "subjects":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "progress":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "login":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "new_subject":
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "flip":
        if not session["flipped"]:
            session["flipped"] = True
            return render_template("index.html", subjects=current_user_subjects, card_text=session["answer"], flipped=session["flipped"], selected_subject=session["selected_subject"])
        else:
            session["flipped"] = False
            return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "correct_answer":
        question = db.session.execute(db.select(Questions).filter(Questions.id == session["question_id"])).scalar()
        question.count_correct += 1
        db.session.merge(question)
        db.session.commit()
        get_random_question()
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    elif link == "wrong_answer":
        question = db.session.execute(db.select(Questions).filter(Questions.id == session["question_id"])).scalar()
        question.count_wrong += 1
        db.session.merge(question)
        db.session.commit()
        get_random_question()
        get_random_question()
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])
    else:
        for subject in current_user_subjects:
            if link == subject.name:
                session["selected_subject"] = subject.id
                get_random_question()
        return render_template("index.html", subjects=current_user_subjects, card_text=session["question"], flipped=session["flipped"], selected_subject=session["selected_subject"])


if __name__ == "__main__":
    app.run()
