import json

from ytmusicapi import YTMusic
from ytmusicapi.auth.oauth import OAuthCredentials

from youtube_music_history_downloader import config

def get_history():
    with open((config.ROOT_DIR / ".local/client_secret.json").as_posix(), "r") as f:
        client_secret = json.load(f)

    ytmusic = YTMusic(
        (config.ROOT_DIR / ".local/oauth.json").as_posix(),
        oauth_credentials=OAuthCredentials(
            client_id=client_secret["installed"]["client_id"],
            client_secret=client_secret["installed"]["client_secret"],
        )
    )

    return ytmusic.get_history()
