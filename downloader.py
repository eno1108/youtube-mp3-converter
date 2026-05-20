import yt_dlp
import os
import shutil

def check_dependencies():
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlpがインストールされていません。'pip install yt-dlp' でインストールしてください。")
        return False

    # Check if ffmpeg is available in the system's PATH
    if not os.path.exists(shutil.which("ffmpeg") or ""):
        print("エラー: ffmpegがシステムのPATHに見つかりません。")
        print("ffmpegをインストールし、システム環境変数PATHに追加してください。")
        return False

    return True

def download_youtube_audio(url, download_directory):
    if not check_dependencies():
        return

    os.makedirs(download_directory, exist_ok=True)
    output_filename_template = os.path.join(download_directory, "%(title)s [%(id)s].%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_filename_template,
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            final_filepath = ydl.prepare_filename(info_dict)
            final_filepath = os.path.splitext(final_filepath)[0] + '.mp3'
            print(f"'{os.path.basename(final_filepath)}' が '{download_directory}' に正常に作成されました。")
    except Exception as e:
        print(f"音声のダウンロード中にエラーが発生しました: {e}")