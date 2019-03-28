import requests
import json


class Youtube():
    def __init__(self, api_key):
        # Componenets for the full url
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        self.parts = ["snippet", "id"]
        self.api_key = api_key
        self.url = ''

    def switch_channel(self, channel_id):
        concatenated_parts = ",".join(self.parts)
        parts_section = "part=%s" % concatenated_parts
        key_section = "%s%s" % ("key=", self.api_key)
        channel_section = "channelId=%s" % channel_id

        self.url = "%s?%s&%s&%s&order=date&maxResults=50" % (self.base_url, key_section, parts_section, channel_section)
        return self.url

    def fetch(self, url, page_token=None):
        if page_token:
            url = "%s&nextPageToken=%s" % (url, page_token)
        else:
            url = self.url

        raw = requests.get(url)

        return json.loads(raw.text)

    def get_videos(self, channel_id):
        url = self.switch_channel(channel_id)

        current_iteration = self.fetch(url)
        total_results = current_iteration["pageInfo"]["totalResults"]

        if total_results > 50:
            needed_iterations = total_results / 50

            count = 1
            all_videos = current_iteration

            while count <= needed_iterations:
                token = current_iteration["nextPageToken"]
                current_iteration = self.fetch(url, token)

                all_videos = all_videos["items"] + current_iteration["items"]

                count += 1

            return all_videos

        else:
            return current_iteration["items"]


youtube = Youtube("youtube-api-key")
print(youtube.get_videos("UCtXfnHIgLI2arDmwhBGYWVg"))
