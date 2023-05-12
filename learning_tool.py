import hashlib
import random
import secrets

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_learning_tool.sqlite"

db = SQLAlchemy(app)

salt = b'\x19\xab\x96\x02G\xb8\xd8ZP\xac\x1b\x91\x0e\xa9\x87m,\rhT\xca\xa7\xdd\x18\xf61\x10\'"/<\xf4'


class User(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    username: db.Mapped[str]
    password: db.Mapped[str]

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User ID: {self.id}, Username: {self.username}"


class Subject(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str]
    creator: db.Mapped[str] = db.mapped_column(db.ForeignKey(User.id))

    def __init__(self, name):
        self.name = name
        self.creator = session["current_user_id"]

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

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.subject = session["selected_subject_id"]
        self.creator = session["current_user_id"]
        self.count_correct = 0
        self.count_wrong = 0

    def __repr__(self):
        return f"Question ID: {self.id}, Subject: {self.subject}"


# --SESSION KEYS--
# session["logged_in"]
# session["current_user_id"]
# session["selected_subject_id"]
# session["question_id"]
# session["question"]
# session["answer"]
# session["flipped"]


@app.get("/")
def index():
    if session.get("logged_in") is not True:
        reset_session_values()
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])

    current_user_subjects = db.session.execute(
        db.select(Subject.id, Subject.name).filter(Subject.creator == session["current_user_id"])).all()
    if len(current_user_subjects) == 0:
        return render_template("form.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], formtype="subject",
                               logged_in=session["logged_in"])
    else:
        session["selected_subject_id"] = current_user_subjects[0].id
        get_random_question()
    return render_index()


def reset_session_values():
    session["logged_in"] = ""
    session["current_user_id"] = ""
    session["selected_subject_id"] = ""
    session["question_id"] = ""
    session["question"] = ""
    session["answer"] = ""
    session["flipped"] = ""


def render_index():
    current_user_subjects = db.session.execute(
        db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()
    return render_template("index.html", subjects=current_user_subjects, card_text=session["question"],
                           flipped=session["flipped"], selected_subject=session["selected_subject_id"],
                           logged_in=session["logged_in"])


def get_random_question():
    current_user_subjects = db.session.execute(
        db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()

    selected_subject_questions = db.session.execute(
        db.select(Questions.id, Questions.question, Questions.answer).filter(
            Questions.creator == session["current_user_id"]).filter(
            Questions.subject == session["selected_subject_id"])).all()
    if len(selected_subject_questions) == 0:
        return render_template("form.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], formtype="quiz",
                               logged_in=session["logged_in"])
    selected_question_row = random.choice(selected_subject_questions)
    session["question_id"] = selected_question_row.id
    session["question"] = selected_question_row.question
    session['answer'] = selected_question_row.answer
    return render_index()


@app.route("/clicked")
def clicked():
    link = request.args.get("link")
    if session.get("logged_in") is not True and link != "register":
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    if link == "register":
        return render_template("form.html", subjects="", selected_subject="", formtype="register",
                               logged_in=session["logged_in"])

    current_user_subjects = db.session.execute(
        db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()

    if link != "flip":
        session["flipped"] = False

    if link == "new_quiz":
        return render_template("form.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], formtype="quiz",
                               logged_in=session["logged_in"])
    elif link == "subjects":
        return render_index()
    elif link == "progress":
        return render_index()
    elif link == "login":
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    elif link == "logout":
        [session.pop(key) for key in list(session.keys())]
        reset_session_values()
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    elif link == "new_subject":
        return render_template("form.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], formtype="subject",
                               logged_in=session["logged_in"])
    elif link == "flip":
        if not session["flipped"]:
            session["flipped"] = True
            return render_template("index.html", subjects=current_user_subjects, card_text=session["answer"],
                                   flipped=session["flipped"], selected_subject=session["selected_subject_id"],
                                   logged_in=session["logged_in"])
        else:
            session["flipped"] = False
            return render_index()
    elif link == "correct_answer":
        question = db.session.execute(db.select(Questions).filter(Questions.id == session["question_id"])).scalar()
        question.count_correct += 1
        db.session.merge(question)
        db.session.commit()

        get_random_question()
        return render_index()
    elif link == "wrong_answer":
        question = db.session.execute(db.select(Questions).filter(Questions.id == session["question_id"])).scalar()
        question.count_wrong += 1
        db.session.merge(question)
        db.session.commit()

        get_random_question()
        return render_index()
    else:
        for subject in current_user_subjects:
            if link == subject.name:
                session["selected_subject_id"] = subject.id
                return get_random_question()
        return render_index()


@app.route("/new_question_form", methods=["POST"])
def new_question_form():
    if request.method == "POST":
        form_data = request.form
        question = Questions(form_data["field_question"], form_data["field_answer"])
        db.session.add(question)
        db.session.commit()
        return get_random_question()


@app.route("/new_subject_form", methods=["POST"])
def new_subject_form():
    if request.method == "POST":
        form_data = request.form
        subject = Subject(form_data["field_subject"])
        db.session.add(subject)
        db.session.commit()
        session["selected_subject_id"] = db.session.execute(
            db.select(Subject.id).filter(Subject.creator == session["current_user_id"])).scalar()
        return get_random_question()


@app.route("/login_form", methods=["POST"])
def login_form():
    if request.method == "POST":
        form_data = request.form
        check_for_user = db.session.execute(
            db.select(User.id).filter(User.username == form_data["field_username"])).scalar()
        if check_for_user is None:
            return render_template("form.html", subjects="", selected_subject="", formtype="login",
                                   logged_in=session["logged_in"],
                                   error_message=f"Username doesn't exist.")

        hashed_password = hashlib.pbkdf2_hmac('sha256', form_data["field_password"].encode('utf-8'), salt, 100000)

        check_for_user = db.session.execute(
            db.select(User.id).filter(User.username == form_data["field_username"]).filter(
                User.password == hashed_password)).scalar()
        if check_for_user is None:
            return render_template("form.html", subjects="", selected_subject="", formtype="login",
                                   logged_in=session["logged_in"],
                                   error_message=f"Password is wrong.")
        session["logged_in"] = True
        session["current_user_id"] = check_for_user
        current_user_subjects = db.session.execute(
            db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()
        if len(current_user_subjects) == 0:
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject=session["selected_subject_id"], formtype="quiz",
                                   logged_in=session["logged_in"])
        else:
            session["selected_subject_id"] = current_user_subjects[0].id
            get_random_question()
        return render_index()


@app.route("/register_form", methods=["POST"])
def register_form():
    if request.method == "POST":
        form_data = request.form

        hashed_password = hashlib.pbkdf2_hmac('sha256', form_data["field_password"].encode('utf-8'), salt, 100000)

        new_user = User(form_data["field_username"], hashed_password)
        if len(new_user.username) < 5:
            return render_template("form.html", subjects="", selected_subject="", formtype="register",
                                   logged_in=session["logged_in"],
                                   error_message=f"Username '{new_user.username}' must be at least 5 characters long.")
        check_for_user = db.session.execute(
            db.select(User.id).filter(User.username == new_user.username)).scalar()
        if check_for_user is not None:
            return render_template("form.html", subjects="", selected_subject="", formtype="register",
                                   logged_in=session["logged_in"],
                                   error_message=f"Username '{new_user.username}' already taken.")
        db.session.add(new_user)
        db.session.commit()
        check_for_user = db.session.execute(
            db.select(User.id).filter(User.username == User.username).filter(
                User.password == hashed_password)).scalar()
        session["logged_in"] = True
        session["current_user_id"] = check_for_user
        return render_template("form.html", subjects="",
                               selected_subject=session["selected_subject_id"], formtype="subject",
                               logged_in=session["logged_in"])


if __name__ == "__main__":
    app.run()
