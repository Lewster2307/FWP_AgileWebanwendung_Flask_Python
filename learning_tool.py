from colour import Color


class User:
    def __init__(self, uu_id: int, username: str, password: str):
        self.uu_id = uu_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"UU_ID: {self.uu_id}, Username: {self.username}, Password: {self.password}\n"


class Subject:
    def __init__(self, us_id: int, subject_name: str, color: Color, creator: User):
        self.us_id = us_id
        self.subject_name = subject_name
        self.color = color
        self.creator = creator

    def __repr__(self):
        return f"US_ID: {self.us_id}, Subject: {self.subject_name}, Color: {self.color}, Creator: {self.creator.username}\n"


class Questions:
    def __init__(self, uq_id: int, question: str, answer: str, subject: Subject, creator: User):
        self.uq_id = uq_id
        self.question = question
        self.answer = answer
        self.subject = subject
        self.creator = creator

    def __repr__(self):
        return f"UQ_ID: {self.uq_id}, Question: {self.question}, Answer: {self.answer}, Subject: {self.subject.subject_name}, Creator: {self.creator.username}\n"


users = [
    User(1, "Lewin", "sicheresPasswort123#"),
    User(2, "Philipp", "unsicheresPasswort")
]


def get_user_by_id(uu_id: int):
    for user in users:
        if user.uu_id == uu_id:
            return user
    raise Exception("User not found")


subjects = [
    Subject(1, "Mathematik 1", Color("blue"), get_user_by_id(1)),
    Subject(2, "Programmieren 1", Color("purple"), get_user_by_id(1)),
    Subject(3, "Datenkommunikation", Color("red"), get_user_by_id(2))
]


def get_subject_by_id(us_id: int):
    for subject in subjects:
        if subject.us_id == us_id:
            return subject
    raise Exception("Subject not found")


def get_subjects_by_creator_id(uu_id: int):
    filtered_subjects = []
    for subject in subjects:
        if subject.creator.uu_id == uu_id:
            filtered_subjects.append(subject)
    filtered_subjects.sort(key=lambda x: x.us_id)
    return filtered_subjects


questions = [
    Questions(1, "Was macht der Parameter a der folgenden Funktion?\na*sin(b*x+c)+d",
              "Streckung/Stauchung entlang der y-Achse", get_subject_by_id(1), get_user_by_id(1)),
    Questions(2, "Wofür steht DNS",
              "Domain Name System", get_subject_by_id(3), get_user_by_id(2)),
]


def get_question_by_id(uq_id: int):
    for question in questions:
        if question.uq_id == uq_id:
            return question
    raise Exception("Question not found")


def get_questions_by_creator_id(uu_id: int):
    filtered_questions = []
    for question in questions:
        if question.creator.uu_id == uu_id:
            filtered_questions.append(question)
    filtered_questions.sort(key=lambda x: x.uq_id)
    return filtered_questions


def main():
    # print(f"Users: {users}")
    # print(f"Subjects {subjects}")
    # print(f"Questions {questions}")

    print(f"Questions by Philipp: {get_questions_by_creator_id(2)}")
    print(f"Subjects by Lewin {get_subjects_by_creator_id(1)}")


if __name__ == "__main__":
    main()
