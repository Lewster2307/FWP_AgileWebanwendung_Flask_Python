import flask
from datetime import datetime

app = flask.Flask(__name__)


class Image:
    def __init__(self, img_id, filename, title, user_id):
        self.id = img_id
        self.filename = filename
        self.title = title
        self.user_id = user_id


images = [
    Image(1, "image(1).png", "Screenshot 1", "User1"),
    Image(2, "image(2).png", "Screenshot 2", "User1"),
    Image(3, "image(3).png", "Screenshot 3", "User1")
]


@app.get("/")
def index():
    now = datetime.now()
    images_with_id_1 = [image for image in images if image.id == 1]
    return flask.render_template("index.html", currenTime=now, image_filenames=images_with_id_1)


@app.get("/download/<image_name>")
def download(image_name):
    return flask.send_from_directory("images", image_name)


app.run()
