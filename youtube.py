from copy import deepcopy
import requests
import json

YOUTUBE_API = "https://youtube.googleapis.com/youtube/v3/videos"

class YoutubeClient:
    def __init__(self) -> None:
        self.parameters = {
            "part": "snippet",
            "key": "AIzaSyAK7VqVcv32RKQX-73fVhnX5mxuAd1VYCo"
        }
    
    def getVideoDetails(self, youtubeId):
        copiedParam = deepcopy(self.parameters)
        copiedParam["id"] = youtubeId
        r = requests.get(YOUTUBE_API, params=copiedParam)
        return r.json()["items"][0]["snippet"]["title"]
