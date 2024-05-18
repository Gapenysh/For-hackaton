import os
import re
from flask import render_template, request, Flask, current_app, send_from_directory
from project import app


# your request handles here with @core.route()


@app.route("/map/<filename>", methods=["GET"])
def video(filename):
    headers = request.headers
    if not "range" in headers:
        return current_app.response_class(status=400)

    video_path = os.path.abspath(os.path.join("/home/user/videos", filename))
    if not os.path.exists(video_path):
        return current_app.response_class(status=404)

    size = os.stat(video_path)
    size = size.st_size

    chunk_size = (10 ** 6) * 3 #1000kb makes 1mb * 3 = 3mb (this is based on your choice)
    start = int(re.sub("\D", "", headers["range"]))
    end = min(start + chunk_size, size - 1)

    content_lenght = end - start + 1

    def get_chunk(video_path, start, chunk_size):
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(chunk_size)
        return chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_lenght,
        "Content-Type": "video/mp4",
    }

    if "Content-Length" in headers and headers["Content-Length"] == str(os.stat(video_path).st_size):
        return send_from_directory(directory=os.path.dirname(video_path), filename=os.path.basename(video_path), as_attachment=False)
    else:
        return current_app.response_class(get_chunk(video_path, start,chunk_size), 206, headers)