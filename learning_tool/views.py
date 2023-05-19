import hashlib
import random

from flask import session, render_template, request

from config import salt
from learning_tool import app, db
from learning_tool.models import Subject, Questions, User


print("THE CODE GOT INTO THE views.py?!")


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
        return get_random_question()


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
        session["question_id"] = ""
        session["question"] = ""
        session["answer"] = ""
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

    # Checks if logged in. If not -> opens login/register
    if session.get("logged_in") is not True and link != "register":
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    if link == "register":
        return render_template("form.html", subjects="", selected_subject="", formtype="register",
                               logged_in=session["logged_in"])

    # Gets all subjects of the current user
    current_user_subjects = db.session.execute(
        db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()

    # Forces card to be not be flipped when it shouldn't
    if link != "flip":
        session["flipped"] = False

    # Checks all different args passed in link
    # Opens new quiz form if a subject exists else opens new subject form
    if link == "new_quiz":
        if session["selected_subject_id"] != "":
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject=session["selected_subject_id"], formtype="quiz",
                                   logged_in=session["logged_in"])
        else:
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject="", formtype="subject",
                                   logged_in=session["logged_in"])
    # Opens a list of all the questions for the selected subject
    elif link == "question_table":
        selected_subject_questions = db.session.execute(
            db.select(Questions.id, Questions.question, Questions.answer).filter(
                Questions.creator == session["current_user_id"]).filter(
                Questions.subject == session["selected_subject_id"])).all()
        return render_template("question_table.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], questions=selected_subject_questions,
                               logged_in=session["logged_in"])
    elif link == "progress":
        count_all_subjects = []
        for subject in current_user_subjects:
            count_wrong = 0
            count_correct = 0
            percent_correct = 0
            percent_wrong = 0
            questions = db.session.execute(
                db.select(Questions.count_wrong, Questions.count_correct).filter(Questions.subject == subject.id)).all()
            for question in questions:
                count_wrong += question.count_wrong
                count_correct += question.count_correct
                count_sum = count_correct + count_wrong
                if count_sum != 0:
                    percent_correct = round(count_correct / count_sum, 3)
                    percent_wrong = round(count_wrong / count_sum, 3)
            count_all_subjects.append((subject.name, percent_correct, percent_wrong, count_correct, count_wrong))
        return render_template("progress.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], data=count_all_subjects,
                               logged_in=session["logged_in"])
    # Opens login form
    elif link == "login":
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    # Resets all session cookies and opens login form
    elif link == "logout":
        reset_session_values()
        return render_template("form.html", subjects="", selected_subject="", formtype="login",
                               logged_in=session["logged_in"])
    # Opens new subject form
    elif link == "new_subject":
        return render_template("form.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], formtype="subject",
                               logged_in=session["logged_in"])
    # Deletes the current selected if a subject exists else opens the new subject form
    elif link == "delete_subject":
        if session.get("selected_subject_id") is None or session.get("selected_subject_id") == "":
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject=session["selected_subject_id"], formtype="subject",
                                   logged_in=session["logged_in"])
        db.session.query(Questions).filter(Questions.subject == session["selected_subject_id"]).delete()
        delete_subject = db.session.execute(
            db.select(Subject).filter(Subject.creator == session["current_user_id"]).filter(
                Subject.id == session["selected_subject_id"])).scalar()
        db.session.delete(delete_subject)
        db.session.commit()
        session["question_id"] = ""
        session["question"] = ""
        session["answer"] = ""
        current_user_subjects = db.session.execute(
            db.select(Subject.id, Subject.name).filter(Subject.creator == session["current_user_id"])).all()
        if len(current_user_subjects) == 0:
            session["selected_subject_id"] = ""
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject=session["selected_subject_id"], formtype="subject",
                                   logged_in=session["logged_in"])
        else:
            session["selected_subject_id"] = current_user_subjects[0].id
            return get_random_question()
    # Deletes the selected question
    elif link.startswith("delete_question"):
        qid = link[link.find("=") + 1:]
        delete_question = db.session.execute(
            db.select(Questions).filter(
                Questions.creator == session["current_user_id"]).filter(
                Questions.id == qid)).scalar()
        db.session.delete(delete_question)
        db.session.commit()
        selected_subject_questions = db.session.execute(
            db.select(Questions.id, Questions.question, Questions.answer).filter(
                Questions.creator == session["current_user_id"]).filter(
                Questions.subject == session["selected_subject_id"])).all()
        session["question_id"] = ""
        session["question"] = ""
        session["answer"] = ""
        return render_template("question_table.html", subjects=current_user_subjects,
                               selected_subject=session["selected_subject_id"], questions=selected_subject_questions,
                               logged_in=session["logged_in"])
    # Flips the card by changing the card_text from question to answer and vice versa
    elif link == "flip":
        if not session["flipped"]:
            session["flipped"] = True
            return render_template("index.html", subjects=current_user_subjects, card_text=session["answer"],
                                   flipped=session["flipped"], selected_subject=session["selected_subject_id"],
                                   logged_in=session["logged_in"])
        else:
            session["flipped"] = False
            return render_index()
    # Increments the correct answer count for the current question and loads a new question
    elif link == "correct_answer":
        question = db.session.execute(db.select(Questions).filter(Questions.id == session["question_id"])).scalar()
        question.count_correct += 1
        db.session.merge(question)
        db.session.commit()

        get_random_question()
        return render_index()
    # Increments the wrong answer count for the current question and loads a new question
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
        check_for_subject = db.session.execute(
            db.select(Subject.id).filter(Subject.name == form_data["field_subject"])).scalar()
        if check_for_subject is not None:
            current_user_subjects = db.session.execute(
                db.select(Subject.name, Subject.id).filter(Subject.creator == session["current_user_id"])).all()
            return render_template("form.html", subjects=current_user_subjects,
                                   selected_subject=session["selected_subject_id"], formtype="subject",
                                   logged_in=session["logged_in"],
                                   error_message=f"Subject name already taken.")
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
                                   selected_subject=session["selected_subject_id"], formtype="subject",
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
                                   error_message=f"Username must be at least 5 characters long.")
        check_for_user = db.session.execute(
            db.select(User.id).filter(User.username == new_user.username)).scalar()
        db.session.execute()
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
