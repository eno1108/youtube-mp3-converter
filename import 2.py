import os

# ダウンロードするYouTube動画の"",
              #URLのリスト
video_urls = [ "https://youtu.be/Kk-2sm1yXNk?si=Srq2WYLdMJPmvIuL" ,
              "https://youtu.be/U2i_IuAB6wo?si=PGmsmA4eZ_6wSFUV" ,
              "https://youtu.be/Kt_ZgTS3eJA?si=o8kwtklveK8A5oaH"               
]

import yt_dlp
# ダウンロード先のディレクトリを指定
download_directory = "F:\pc\music"
filename_template = os.path.join(download_directory, '%(title)s.%(ext)s')
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': filename_template,
    'quiet': False, #⃣ 動作ログを表示する
    'noplaylist': True,  # プレイリストではなく単一の動画をダウンロード
    'ignoreerrors': True,  # エラーが発生しても続行
    'no_warnings': False, # 警告を表示する
    'progress_hooks': [],  # 進捗フックを使用しない
    'retries': 10,  # リトライ回数
    'retry_sleep': 5,  # リトライ間隔（秒）
    'socket_timeout': 10,  # ソケットタイムアウト（秒）
    'keepvideo': False,  # 変換後に元動画(webm等)を削除
}

# 各動画をMP3に変換
for url in video_urls:
    print(f"ダウンロード中: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # ダウンロードが成功した場合のファイルパスを推測（正確なパスはyt-dlpがログに出力）
            final_filepath = ydl.prepare_filename(info_dict)
            final_filepath = os.path.splitext(final_filepath)[0] + '.mp3'
            print(f"'{os.path.basename(final_filepath)}' が '{download_directory}' に正常に作成されました。")
    except Exception as e:
        print(f"音声のダウンロード中にエラーが発生しました: {e}")

print("すべての動画のダウンロードと変換が完了しました。")