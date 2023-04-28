from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_gallery.sqlite"

db = SQLAlchemy(app)


class Image(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    filename: db.Mapped[str]
    title: db.Mapped[str]
    user_id: db.Mapped[int]


@app.get("/")
def index():

    all_images = db.session.execute(db.select(Image).filter(Image.id == 1)).scalars().all()
    # SELECT * FROM image WHERE id=1;
    print(all_images)
    now = datetime.now()
    return render_template("index_gallery.html", currenTime=now, image_filenames=all_images)


@app.get("/download/<image_name>")
def download(image_name):
    return send_from_directory("images", image_name)


if __name__ == '__main__':
    app.run()
