#!/bin/bash
set -e

# Check if the OAuth file exists
if [ ! -f config/oauth.json ]; then
  echo "Running OAuth setup..."

  # Parse client_id and client_secret from client_secret.json
  CLIENT_ID=$(jq -r '.installed.client_id' config/client_secret.json)
  CLIENT_SECRET=$(jq -r '.installed.client_secret' config/client_secret.json)

  # Run the OAuth setup with the extracted credentials
  poetry run ytmusicapi oauth --file config/oauth.json --client-id "$CLIENT_ID" --client-secret "$CLIENT_SECRET"
fi

# Run the main script
echo "Starting the main script..."
poetry run python youtube_music_history_downloader/download_history.py