from flask import Flask
from flask import jsonify
from dotenv import load_dotenv
import os
from src.Youtube import Youtube

app = Flask(__name__)

# Loading the env properties into the system
load_dotenv(".env")

app.config['YOUTUBE_API_KEY'] = os.getenv("YOUTUBE_API_KEY")
app.config['MAX_RESULTS'] = int(os.getenv("MAX_RESULTS_PER_CALL"))
app.config['MAX_DEPTH'] = int(os.getenv("MAX_DEPTH"))

youtube = Youtube(app.config['YOUTUBE_API_KEY'], app.config['MAX_RESULTS'], app.config['MAX_DEPTH'])


@app.route('/livestream/<channel_id>', methods=['GET'])
def find_livestreams_in_channel(channel_id):
    return jsonify({"status": "success", "message": youtube.list_available_videos(channel_id)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
