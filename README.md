# Spotify Data Analysis
Repository to get an analysis of your streams since creating your account

# Getting the data
The folder that you have should contain your entire streaming history data for the life of your account. This can be obtained by pressing the `Request data` button in [this website](https://www.spotify.com/us/account/privacy/) if you are logged in to your account. 

After some weeks, you will get an email with the extended streaming history. After downloading it, you will have a zip file called `my_spotify_data.zip` and when opened the directory is `MyData`. This directory will contain a pdf file which details the contents of the other files in the directory. The files we care about are the ones with the following two fromats: `Streaming_History_Audio_YEAR1_NUMBER` and `Streaming_History_Audio_YEAR1-YEAR2_NUMBER.json` where `YEAR1` and `YEAR2` are the years in which the data of the json file were streamed and `NUMBER` is the number of the file, making the file with the oldest data be `0` and the most recent data being `len(amount_of_json_files_of_audio) - 1`.
 
# main.py 



