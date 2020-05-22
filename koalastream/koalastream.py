"""Koalastream ffmpeg"""
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

STREAMS = [
    {"url": "rtmp://a.rtmp.youtube.com/live2", "name": "YouTube"},
    {"url": "rtmp://va.pscp.tv:80/x", "name": "Twitter"},
    {"url": "rtmp://live-iad05.twitch.tv/app", "name": "Twitch"},

]
KS_STREAM_KEY = os.environ["KS_STREAM_KEY"]

def _get_urls():
    urls = []
    for stream in STREAMS:
        env_var = f"{stream['name'].upper()}_STREAM_KEY"
        stream_key = os.getenv(env_var)
        if stream_key:
            urls.append(f"{stream['url']}/{stream_key}") 
        else:
            logger.debug('no key for %s', env_var)
    return urls

async def ffmpeg():
    """run ffmpeg output to multiple outputs"""
    urls = _get_urls()

    args = [
        "-i", f"rtmp://localhost:1935/live/{KS_STREAM_KEY}", 
        
        "-c", "copy",
        #"-c:v", "libx264", 
        #"-c:a", 

        "-f", "tee", 
        "-map", "0:v", 
        "-map", "0:a", 
        "|".join([f"[f=flv]{u}" for u in urls]) 
    ]    
    logger.info('about to run %s', args)
    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE

    )


    logger.info('process created')
    #stdout, stderr = await process.communicate()
    #logger.error('exited ffmpeg')
    #logger.info('output %s, %s', stdout.decode(), stderr.decode())
    while True:
        line = await process.stdout.readline()
        if not line:
            logger.error('end of ffmpeg')
            break
        logger.info('line = %s', line.decode().strip())

    logger.error('ffmpeg exited')

