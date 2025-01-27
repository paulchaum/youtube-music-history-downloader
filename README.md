# Youtube Music History Downloader

This script downloads your YouTube Music history and saves the result on your local disk.

This script uses the following packages :
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) to get the history
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download the musics

# Install

## Init credentials

Before installing the script, you need to create a Google API key:
1. Go to the [Google API Console](https://console.developers.google.com/).
2. Create a new project or select an existing one.
3. Enable the "YouTube Data API v3" for your project.
4. Go to "Credentials" and create an OAuth 2.0 Client ID.
5. Download the client secret JSON file and save it as `client_secret.json` in the `config/` directory of this project.

## Without docker

1. Install the required packages:
    ```bash
    poetry install
    ```

2. Install ffmpeg:
    ```bash
    sudo apt install ffmpeg
    ```

3. Init the credentials (see [Init credentials](#init-credentials))
   then run the command `ytmusicapi oauth --file config/oauth.json` and follow the instructions (client ID and secret are in the `client_secret.json` file).

4. Start the script with the following command:
    ```bash
    poetry run python youtube_music_history_downloader/download_history.py
    ```

## With docker


1. Init the credentials (see [Init credentials](#init-credentials))

2. Build the image:
    ```bash
    docker build -t youtube-music-history-downloader .
    ```

3. Run the container:
    ```bash
   docker run -it \
   -v "$(pwd)/config:/app/config" \
   -v "$(pwd)/output:/app/output" \
   -e SLEEP_MINUTES=240 \
   youtube-music-history-downloader
   ```
   On first use, a message will appear to activate your Google account.
   
   
## Docker compose

1. Init the credentials (see [Init credentials](#init-credentials))

2. Copy this to your `docker-compose.yml` file:
   ```yaml
   services:
     youtube-music-history-downloader:
       image: youtube-music-history-downloader
       container_name: youtube-music-history-downloader
       environment:
         SLEEP_MINUTES: "240"
       volumes:
         - ./config:/app/config
         - ./output:/app/output
       stdin_open: true
       tty: true
   ```

3. Then run:
   ```bash
   docker-compose up
   ```
   On first use, a message will appear to activate your Google account.

# Config

By default, the script download musics in `m4a` format with the best quality available, with thumbnail and metadata.
You can update the config by copying the file `config/ydl_options.default.json` to `config/ydl_options.custom.json`.
Keep in mind that the output directory (attribute `outtmpl`) is handled by the script itself.

The script keeps in memory the downloaded musics to avoid downloading them again, in the file [config/download_history.jsonl](config/download_history.jsonl).