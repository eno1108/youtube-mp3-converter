import os
import sys
from downloader import download_youtube_audio
from utils import check_dependencies

def main():
    # Check if required dependencies are installed
    check_dependencies()

    for url in youtube_urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        if url:
            download_youtube_audio(url)

if __name__ == "__main__":
    main()
    # Get user input for multiple YouTube URLs
    youtube_urls =input("https://youtu.be/ojZaWERcbaI?si=CLg6tNHGXhviMntW"，"https://youtu.be/VPhLXeU25KA?si=_5zhMDQETI446WPG”，”https://youtu.be/UpEPkPg8YP4?si=wgZyTsI-4n7x-vPX").split(',')