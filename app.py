import requests
import json


class Youtube():
    def __init__(self, api_key):
        # Componenets for the full url
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        self.parts = ["snippet", "id"]
        self.api_key = api_key

    def _switch_channel(self, channel_id: str) -> str:
        """
        Forms a fully working url to the youtube api that may then be used to query the
        list of available videos in the chosen channel

        :param channel_id: The id of the public channel to which the queries will be directed
        :type channel_id: str
        :return: A url to the youtube data api to query the channel videos
        :rtype: str
        """

        concatenated_parts = ",".join(self.parts)
        parts_section = "part=%s" % concatenated_parts
        key_section = "%s%s" % ("key=", self.api_key)
        channel_section = "channelId=%s" % channel_id

        return "%s?%s&%s&%s&order=date&maxResults=50" % (self.base_url, key_section, parts_section, channel_section)

    @staticmethod
    def _fetch_from_api(url, page_token=None):
        """
        Retrives the channel information from the youtube data api

        A list of dictionaries containing each of the videos found will be included with
        the fields of each dictionary being dependant of the queried arguments determined
        in the self.parts attribute

        NOTE: the api has a max results of 50, if more results are desired it'll need to
        be called several times passing a token value at "nextPageToken" to work through
        the different pages

        :param url: The full url to the youtube api including the api key and channel_id
        :type url: str
        :param page_token: Optinal argument, used to fetch subsecuent pages of the video list
        :type page_token: str
        :return: A list containing the listing of available videos in the channel limited by the max results
        :rtype: dict
        """

        if page_token:
            url = "%s&nextPageToken=%s" % (url, page_token)

        raw = requests.get(url)

        return json.loads(raw.text)

    def list_available_videos(self, channel_id):
        """
        Forms a full list of the videos found in a given channel by calling the youtube data
        api in a loop to retrieve all of its paginated results

        :param channel_id: The id of the public channel to which the queries will be directed
        :type channel_id: str
        :return: A full list of all videos in a given channel
        :rtype: list
        """

        url = self._switch_channel(channel_id)
        current_iteration = self._fetch_from_api(url)
        print(json.dumps(current_iteration))
        all_videos = current_iteration["items"]

        total_results = current_iteration["pageInfo"]["totalResults"]

        if total_results > 50:
            needed_iterations = total_results / 50

            count = 1
            while count < needed_iterations:
                print(count)
                token = current_iteration["nextPageToken"]
                current_iteration = self._fetch_from_api(url, token)

                all_videos = all_videos + current_iteration["items"]

                count += 1

            return all_videos

        else:
            return all_videos


youtube = Youtube("youtube-api-key")
videos = youtube.list_available_videos("UCLA_DiR1FfKNvjuUpBHmylQ")

# Eliminating duplicated entries
new = []
for video in videos:
    if video not in new:
        new.append(video)

print(len(videos))
print(len(new))
