"""Koalastream ffmpeg"""
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

KS_STREAM_KEY = os.environ["KS_STREAM_KEY"]
async def ffmpeg(outputs:list):
    """run ffmpeg comment to multiple outputs"""

    args = [
        "-i", f"rtmp://localhost:1935/live/{KS_STREAM_KEY}", 
        
        "-c", "copy",
        #"-c:v", "libx264", 
        #"-c:a", 

        "-f", "tee", 
        "-map", "0:v", 
        "-map", "0:a", 
        "|".join([f"[f=flv]{o}" for o in outputs]) 
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
    for line in await process.stdout.readline():
        logger.info('ffmpeg output = %s', line)

    logger.error('ffmpeg exited')

