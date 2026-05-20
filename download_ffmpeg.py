import pathlib
import shutil
import urllib.request
import zipfile

url = "https://github.com/GyanD/codexffmpeg/releases/download/8.1.1/ffmpeg-8.1.1-full_build-shared.zip"
zip_path = pathlib.Path(r"g:\python\youtube-mp3-converter\ffmpeg.zip")
out_dir = pathlib.Path(r"g:\python\youtube-mp3-converter\ffmpeg")
zip_path.parent.mkdir(parents=True, exist_ok=True)
urllib.request.urlretrieve(url, zip_path)
shutil.rmtree(out_dir, ignore_errors=True)
with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(out_dir)
print(next(out_dir.rglob("ffmpeg.exe")))
