import json
import os
import time
from datetime import datetime
from pathlib import Path

import schedule
from yt_dlp import YoutubeDL

from youtube_music_history_downloader import config
from youtube_music_history_downloader.config import ROOT_DIR
from youtube_music_history_downloader.fetch_history import get_history

def download_history():
    history = get_history()

    output_dir = ROOT_DIR / "output"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Configuration
    def yt_dlp_monitor(d):
        if d.get("status") == "finished":
            # Get file path
            final_filename = d.get("info_dict").get("_filename")
            final_filename = Path(final_filename).with_suffix(".m4a")

            # Get video ID
            video_id = d.get("info_dict").get("id")

            # Save it in download_history.jsonl
            with open(config.ROOT_DIR / "config/download_history.jsonl", "a") as f:
                new_download_history = {
                    "video_id": video_id,
                    "file_path": final_filename.as_posix(),
                    "created_at": datetime.now().isoformat(),
                }
                f.write(f"{json.dumps(new_download_history, ensure_ascii=False)}\n")


    output_template = output_dir / "%(title)s.%(ext)s"
    if (config.ROOT_DIR / "config/ydl_options.custom.json").exists():
        with open(config.ROOT_DIR / "config/ydl_options.custom.json", "a") as f:
            local_options = json.load(f)
    else:
        with open(config.ROOT_DIR / "config/ydl_options.default.json", "a") as f:
            local_options = json.load(f)
    ydl_opts = {
        "outtmpl": output_template.as_posix(),
        "progress_hooks": [yt_dlp_monitor],
        **local_options,
    }

    # Get already downloaded songs
    already_downloaded_videos_ids = []
    if (config.ROOT_DIR / "config/download_history.jsonl").exists():
        with open(config.ROOT_DIR / "config/download_history.jsonl", "r") as f:
            for line in f:
                download_history_data = json.loads(line)
                already_downloaded_videos_ids.append(download_history_data["video_id"])

    # Deduplicate on videoId and removed already downloaded songs while preserving order
    seen = set()
    urls_to_download = []
    for song in history:
        if song["videoId"] not in seen and song["videoId"] not in already_downloaded_videos_ids:
            urls_to_download.append(f"https://www.youtube.com/watch?v={song['videoId']}")
            seen.add(song["videoId"])

    # Download songs
    print(f"Downloading {len(urls_to_download)} songs...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls_to_download)

def main():
    download_history()

if __name__ == "__main__":
    # Schedule the download_history function to run every N minutes
    schedule.every(int(os.environ.get("SLEEP_MINUTES", "240"))).minutes.do(main)

    # Run main() at the start
    main()

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)