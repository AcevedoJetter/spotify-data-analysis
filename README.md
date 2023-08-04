# Spotify Data Analysis

Repository to get an analysis of your streams since creating your account. **This is a work in progress, more functions will be added.**

# Getting the data

The folder that you have should contain your entire streaming history data for the life of your account. This can be obtained by pressing the `Request data` button in [this website](https://www.spotify.com/us/account/privacy/) if you are logged in to your account.

After some weeks, you will get an email with the extended streaming history. After downloading it, you will have a zip file called `my_spotify_data.zip` and when opened the directory is `MyData`.

# MyData

This directory will contain a pdf file which details the contents of the other files in the directory. The files we care about are the ones that start with `Streaming_History_Audio` and are json files.

The following is from the [Understanding my Data page](https://support.spotify.com/us/article/understanding-my-data/):

A list of items (e.g. songs, videos, and podcasts) listened to or watched during the lifetime of your account, including the following details:

- `ts` - Date and time of when the stream ended in UTC format (Coordinated Universal Time zone).
- `username` - Your Spotify username.
- `platform` - Platform used when streaming the track (e.g. Android OS, Google Chromecast).
- `ms_played` - For how many milliseconds the track was played.
- `conn_country` - Country code of the country where the stream was played.
- `ip_addr_decrypted` - IP address used when streaming the track.
- `user_agent_decrypted` - User agent used when streaming the track (e.g. a browser).
- `master_metadata_track_name` - Name of the track.
- `master_metadata_album_artist_name` - Name of the artist, band or podcast.
- `master_metadata_album_album_name` - Name of the album of the track.
- `spotify_track_uri` - A Spotify Track URI, that is identifying the unique music track.
- `episode_name` - Name of the episode of the podcast.
- `episode_show_name` - Name of the show of the podcast.
- `spotify_episode_uri` - A Spotify Episode URI, that is identifying the unique podcast episode.
- `reason_start` - Reason why the track started (e.g. previous track finished or you picked it from the playlist).
- `reason_end` - Reason why the track ended (e.g. the track finished playing or you hit the next button).
- `shuffle` - Whether shuffle mode was used when playing the track.
- `skipped` - Information whether the user skipped to the next song.
- `offline` - Information whether the track was played in offline mode.
- `offline_timestamp` - Timestamp of when offline mode was used, if it was used.
- `incognito_mode` - Information whether the track was played during a private session.

Example of the streaming data of one song:

```json
{
    "ts" : "YYY-MM-DD 13:30:30",
    "username" : "_________",
    "platform" : "_________",
    "ms_played" : "_________",
    "conn_country" : "_________",
    "ip_addr_decrypted" : "___.___.___.___",
    "user_agent_decrypted" : "_________",
    "master_metadata_track_name" : "_________",
    "master_metadata_album_artist_name" : "_________",
    "master_metadata_album_album_name" : "_________",
    "spotify_track_uri" : "_________",
    "episode_name" : "_________",
    "episode_show_name" : "_________",
    "spotify_episode_uri" : "_________",
    "reason_start" : "_________",
    "reason_end" : "_________",
    "shuffle" : null|true|false,
    "skipped" : null|true|false,
    "offline" : null|true|false,
    "offline_timestamp" : "_________",
    "incognito_mode" : null|true|false,
}
```

# main.py

All the functions in `main.py` have docstrings which contains the parameters of the function and it also contains what is returned by the function.

Note that the columns of the pandas DataFrame returned by `get_all_data()` can be found [here](https://github.com/AcevedoJetter/spotify-data-analysis#mydata).

# How to run main.py in the terminal

First, make sure that the `MyData` directory is in the same directory as `main.py`. After this, you should run `python3 main.py` and it will create a txt file called `analysis.txt` which will contain the analyzed data after running the functions of `main.py` using the data from the `MyData` directory.
