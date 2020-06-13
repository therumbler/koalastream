"""Koalastream ffmpeg"""
import asyncio
import contextlib
import logging
import os
import socket
from uuid import uuid4

from koalastream.models.server import Server

logger = logging.getLogger(__name__)

STREAMS = [
    {"url": "rtmp://a.rtmp.youtube.com/live2", "name": "YouTube"},
    {"url": "rtmp://va.pscp.tv:80/x", "name": "Twitter"},
    {"url": "rtmp://live-iad05.twitch.tv/app", "name": "Twitch"},
]
KS_STREAM_KEY = os.environ["KS_STREAM_KEY"]


def _get_service_urls():
    urls = []
    for stream in STREAMS:
        env_var = f"{stream['name'].upper()}_STREAM_KEY"
        stream_key = os.getenv(env_var)
        if stream_key:
            urls.append(f"{stream['url']}/{stream_key}")
        else:
            logger.debug("no key for %s", env_var)
    return urls


async def ffmpeg():
    """run ffmpeg output to multiple outputs"""
    service_urls = _get_service_urls()
    if not service_urls:
        logger.error("no services configured")
        return
    args = [
        "-i",
        f"rtmp://localhost:1935/live/{KS_STREAM_KEY}",
        "-c",
        "copy",
        # "-c:v", "libx264",
        # "-c:a",
        "-f",
        "tee",
        "-map",
        "0:v",
        "-map",
        "0:a",
        "|".join([f"[f=flv]{u}" for u in service_urls]),
    ]
    logger.info("about to run %s", args)
    process = await asyncio.create_subprocess_exec(
        "ffmpeg", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    logger.info("process created")
    # stdout, stderr = await process.communicate()
    # logger.error('exited ffmpeg')
    # logger.info('output %s, %s', stdout.decode(), stderr.decode())
    while True:
        line = await process.stdout.readline()
        if not line:
            logger.error("end of ffmpeg")
            break
        logger.info("line = %s", line.decode().strip())

    logger.error("ffmpeg exited")


def _unused_tcp_port():
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


async def _run_cmd(cmd):
    logger.info("running %s", " ".join(cmd))
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
    except FileNotFoundError:
        error_message = f"cannot find process {cmd[0]}".encode()
        logger.error(error_message)
        return None, error_message
    stdout, stderr = await process.communicate()
    if stderr:
        logger.error(stderr.decode())
    stdout = stdout.decode()
    return stdout, stderr


async def _docker_run(image_name: str, tcp_port: int, **env_vars):
    """Run a docker container locally"""

    logger.info("about to run %s", env_vars)
    env_list = [("-e", f"{k}={v}") for k, v in env_vars.items() if v]
    flattened = [i for sublist in env_list for i in sublist]

    cmd = [
        "docker",
        "run",
        "--name",
        f"koalastream_{uuid4()}",
        "-p",
        f"{tcp_port}:1935",
        "-d",
        *flattened,
        image_name,
    ]
    stdout, stderr = await _run_cmd(cmd)
    if stderr:
        return {"error": stderr}
    container_id = stdout
    logger.info("docker started %s", container_id)
    return {"container_id": container_id}


async def create_local_docker(server: Server):
    """run a local docker instance of koalachat"""
    logger.info("starting server %s", server)
    logger.info(dict(server))
    image_name = "therumbler/koalastream"
    port = _unused_tcp_port()
    logger.info("port = %s", port)
    resp = await _docker_run(image_name, tcp_port=port, **dict(server))
    resp["port"] = port
    return resp


async def delete_local_docker(container_id):
    cmd = ["docker", "stop", container_id]
    stdout, stderr = await _run_cmd(cmd)
    if stderr:
        logger.error("could not stop %s", container_id)
        return {"error": str(stderr.decode())}
    cmd = ["docker", "rm", container_id]

    stdout, stderr = await _run_cmd(cmd)
    return {"container_id": container_id}
