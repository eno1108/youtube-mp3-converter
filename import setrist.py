import os
import yt_dlp

# ダウンロードするYouTubeプレイリストのURLを指定
playlist_url = "https://youtube.com/playlist?list=PL2y1wRoO2eWMZ-pS3Xd2F9O2g2mF2HCzf&si=rIcpVT8j1uPu9h7b"
# ダウンロード先のディレクトリを作成
download_directory = "F:\\pc\\music\\にじさんじ"
if not os.path.exists(download_directory):
    os.makedirs(download_directory)
filename_template = os.path.join(download_directory, '%(title)s.%(ext)s')

ydl_opts = {
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': filename_template,
    'quiet': False,
    'noplaylist': True,
    'ignoreerrors': True,
    'no_warnings': False,
    'progress_hooks': [],
    'retries': 10,
    'retry_sleep': 5,
    'socket_timeout': 10,
    'keepvideo': False,
    'cookies': "F:\\pc\\music\\cookies.txt",
    'sleep_interval': 5,  # ← 5秒の遅延を追加
}

# プレイリストの全曲をMP3に変換
print(f"ダウンロード中: {playlist_url}")
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=True)
        for entry in info_dict['entries']:
            final_filepath = ydl.prepare_filename(entry)
            final_filepath = os.path.splitext(final_filepath)[0] + '.mp3'
            print(f"'{os.path.basename(final_filepath)}' が '{download_directory}' に正常に作成されました。")
except Exception as e:
    print(f"音声のダウンロード中にエラーが発生しました: {e}")

print("すべての動画のダウンロードと変換が完了しました。")