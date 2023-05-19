from flask import session

from learning_tool import db


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
