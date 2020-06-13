import logging
from pydantic import BaseModel, validator

logger = logging.getLogger(__name__)


class Server(BaseModel):
    KS_STREAM_KEY: str
    YOUTUBE_STREAM_KEY: str = None
    TWITTER_STREAM_KEY: str = None
    TWITCH_STREAM_KEY: str = None

    @validator("KS_STREAM_KEY")
    def validate_ks_stream_key(cls, ks_stream_key):
        if len(ks_stream_key) == 0:
            logger.error("invalid KS_STREAM_KEY")
            raise ValueError("you must set your own personal stream key")

        return ks_stream_key

    @validator("TWITCH_STREAM_KEY")
    def validate_has_one_key(cls, twitch_stream_key, values):
        """check that at least one stream key is set"""
        one_key_is_set = False
        for k, v in values.items():
            if k.startswith("KS_"):
                continue
            if v:
                one_key_is_set = True
        if not one_key_is_set:
            raise ValueError("you must set at least one stream key")
        return twitch_stream_key
