from flask import Flask
from flask import jsonify
from dotenv import load_dotenv
import os
from src.Youtube import Youtube
from flask_sqlalchemy import SQLAlchemy

# Loading the env properties into the system
load_dotenv(".env")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%i/%s' % (
    os.getenv("DB_USER"),
    os.getenv("MYSQL_ROOT_PASSWORD"),
    os.getenv("DB_HOST"),
    int(os.getenv("DB_PORT")),
    os.getenv("DB_SCHEMA")
)
db = SQLAlchemy(app)


class Streams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.before_first_request
def initialize_database():
    db.create_all()


app.config['YOUTUBE_API_KEY'] = os.getenv("YOUTUBE_API_KEY")
app.config['MAX_RESULTS'] = int(os.getenv("MAX_RESULTS_PER_CALL"))
app.config['MAX_DEPTH'] = int(os.getenv("MAX_DEPTH"))

youtube = Youtube(app.config['YOUTUBE_API_KEY'], app.config['MAX_RESULTS'], app.config['MAX_DEPTH'])


@app.route('/livestream/<channel_id>', methods=['GET'])
def find_livestreams_in_channel(channel_id):
    return jsonify({"status": "success", "message": youtube.list_available_videos(channel_id)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
