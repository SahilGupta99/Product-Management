import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def save_uploaded_files(request):
    image_urls = []
    video_url = None

    # Handle Images
    image_files = request.files.getlist("images")
    for file in image_files:
        if file and allowed_file(file.filename, Config.ALLOWED_IMAGE_EXTENSIONS):
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_urls.append(f"/static/uploads/{filename}")

    # Handle Video
    video_file = request.files.get("video")
    if video_file and allowed_file(video_file.filename, Config.ALLOWED_VIDEO_EXTENSIONS):
        filename = secure_filename(video_file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        video_file.save(filepath)
        video_url = f"/static/uploads/{filename}"

    return image_urls, video_url
