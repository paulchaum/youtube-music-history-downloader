# Init credentials

1. Go to the [Google API Console](https://console.developers.google.com/).
2. Create a new project or select an existing one.
3. Enable the "YouTube Data API v3" for your project.
4. Go to "Credentials" and create an OAuth 2.0 Client ID.
5. Download the client secret JSON file and save it as `client_secret.json` in the `.local/` directory of this project.
6. Run the command `ytmusicapi oauth --file .local/oauth.json` and follow the instructions (client ID and secret are in the `client_secret.json` file).