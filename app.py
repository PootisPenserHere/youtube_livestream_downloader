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
    title = db.Column(db.String(250), nullable=False, unique=True, server_default="")
    video_id = db.Column(db.String(50), nullable=False, unique=True, server_default="")
    channel_id = db.Column(db.String(50), nullable=False, server_default="")
    channel_name = db.Column(db.String(100), nullable=False, server_default="")
    raw = db.Column(db.JSON, nullable=False)
    status = db.Column(db.Enum("queued", "downloading", "done"), nullable=False, server_default="downloading")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # FIXME the server_onupdate clause is not adding the respective sql codes
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, title, video_id, channel_id, channel_name, raw):
        self.title = title
        self.video_id = video_id
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.raw = raw

    def __repr__(self):
        return '<Title %s video_id %s channel_id %s channel name %s status %s>' % (
            self.title,
            self.video_id,
            self.channel_id,
            self.channel_name,
            self.status
        )


@app.before_first_request
def initialize_database():
    db.create_all()


app.config['YOUTUBE_API_KEY'] = os.getenv("YOUTUBE_API_KEY")
app.config['MAX_RESULTS'] = int(os.getenv("MAX_RESULTS_PER_CALL"))
app.config['MAX_DEPTH'] = int(os.getenv("MAX_DEPTH"))

youtube = Youtube(app.config['YOUTUBE_API_KEY'], app.config['MAX_RESULTS'], app.config['MAX_DEPTH'])


@app.route('/list/<channel_id>', methods=['GET'])
def find_livestreams_in_channel(channel_id):
    return jsonify({"status": "success", "message": youtube.list_available_videos(channel_id)})


@app.route('/download/<channel_id>', methods=['GET'])
def download_livestreams_from_channel(channel_id):
    current_streams = youtube.list_available_videos(channel_id)

    for current in current_streams:
        title = current["snippet"]["title"]
        src_channel_id = current["snippet"]["channelId"]
        channel_name = current["snippet"]["channelTitle"]
        video_id = current["id"]["videoId"]

        row = db.session.query(Streams).filter_by(video_id=video_id).first()

        # If the stream was found in the database and has a status that mark it as anything different
        # than queued we ignore this entry
        #
        # A queued stream is one that had already begin to be downloaded and was cancelled thus needs
        # to be restarted
        if row and row.status != os.getenv("STREAM_STATUS_QUEUE"):
            continue
        else:
            # Determines if there are streams that need to be restarted
            if row and row.status == os.getenv("STREAM_STATUS_QUEUE"):
                row.status = os.getenv("STREAM_STATUS_DOWNLOADING")  # Changing its status to reflect the restart
                db.session.commit()

                # TODO restart the download here

            # Streams that are not found in the database are new and beging their download process here
            else:
                insert = Streams(
                    title=title,
                    video_id=video_id,
                    raw=current,
                    channel_id=src_channel_id,
                    channel_name=channel_name
                )

                db.session.add(insert)
                db.session.commit()

    return jsonify({"status": "success", "message": youtube.list_available_videos(channel_id)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
