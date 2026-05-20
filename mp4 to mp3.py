import os
from pydub import AudioSegment

def mp4_to_mp3(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="mp4")
    audio.export(output_path, format="mp3")

# 例: フォルダ内の全.mp4ファイルをmp3に変換
input_folder = "F:\\pc\\music\\にじさんじ"
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.splitext(input_file)[0] + ".mp3"
        mp4_to_mp3(input_file, output_file)
        print(f"変換完了: {output_file}")

# pydubを使うにはffmpegが必要です。インストールしてパスを通してください。