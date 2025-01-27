# Use Python 3.12 as the base image
FROM python:3.12-slim

# Install jq for JSON parsing and ffmpeg for yt-dlp
RUN apt-get update && apt-get install -y jq ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy necessary files for dependency installation
COPY pyproject.toml poetry.lock README.md ./

# Copy the package directory containing the project code
COPY youtube_music_history_downloader/ youtube_music_history_downloader/

# Install dependencies and the root package
RUN poetry install

# Copy the rest of the application code (if any remaining files)
COPY . .

# Create config and output directories (if they don't exist)
RUN mkdir -p config output

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]