import youtube_dl


class Downloader:
    base_url = "http://www.youtube.com/watch?v=%s"

    @staticmethod
    def video_metadata(url: str) -> dict:
        """
        Gathers the metadata of a given youtube resource and returns a dictionary containing its
        different versions, this will include the altervatives formats

        :param url: The full url to the youtube video
        :type url: str
        :return: A dict containing the video metadata
        :rtype: dict
        """

        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

        with ydl:
            result = ydl.extract_info(
                url,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        return video

    @staticmethod
    def download(url: str, name: str):
        """
        Saves a video to disk naming it with the given name

        The url may direct to an already existing vide or a live stream, they'll be
        downloaded in an equal manner regardless

        NOTE: As quality is not specified the highest available quality will be taken by
        default, for better results ffmpeg should be installed in the system

        :param url: The full url to the youtube video
        :type url: str
        :param name: The name the new file will have
        :type name: str
        :return:
        """

        # Replacing characters that cause conflicts with disk paths
        ydl_opts = {'outtmpl': "videos/%s" % name.replace("/", " ")}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Passed as a list

