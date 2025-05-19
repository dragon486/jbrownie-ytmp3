from flask import Flask, request, send_file, render_template, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format = request.form['format']  # 'mp3' or 'mp4'
    filename = str(uuid.uuid4())
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': filepath + '.%(ext)s',
    }

    if format == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:  # MP4
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

    ext = 'mp3' if format == 'mp3' else 'mp4'
    return send_file(filepath + '.' + ext, as_attachment=True)

# ✅ Route for robots.txt
@app.route("/robots.txt")
def robots():
    return send_from_directory('.', 'robots.txt')

# ✅ Route for sitemap.xml
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
