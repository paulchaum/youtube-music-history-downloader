# Install without docker

1. Install the required packages:
    ```bash
    poetry install
    ```

2. Install ffmpeg:
    ```bash
    sudo apt install ffmpeg
    ```

3. Init credentials:
   1. Go to the [Google API Console](https://console.developers.google.com/).
   2. Create a new project or select an existing one.
   3. Enable the "YouTube Data API v3" for your project.
   4. Go to "Credentials" and create an OAuth 2.0 Client ID.
   5. Download the client secret JSON file and save it as `client_secret.json` in the `config/` directory of this project.
   6. Run the command `ytmusicapi oauth --file config/oauth.json` and follow the instructions (client ID and secret are in the `client_secret.json` file).

# Install with docker

1. Build the image:
    ```bash
    docker build -t youtube-music-history-downloader .
    ```
   
2. Run the container:
    ```bash
   docker run -it \
   -v "$(pwd)/config:/app/config" \
   -v "$(pwd)/output:/app/output" \
   youtube-music-history-downloader
   ```
   
# Docker compose

Copy this to your `docker-compose.yml` file:
```yaml
services:
  youtube-music-history-downloader:
    image: youtube-music-history-downloader
    container_name: youtube-music-history-downloader
    volumes:
      - ./config:/app/config
      - ./output:/app/output
    stdin_open: true
    tty: true
```

And run:
```bash
docker-compose up
```