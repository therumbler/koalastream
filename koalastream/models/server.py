from pydantic import BaseModel


class Server(BaseModel):
    KS_STREAM_KEY: str
    YOUTUBE_STREAM_KEY: str = None
    TWITTER_STREAM_KEY: str = None
    TWITCH_STREAM_KEY: str = None
