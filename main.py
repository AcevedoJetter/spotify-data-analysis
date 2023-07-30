################################################################
###             Analysis on Spotify account data             ### 
###                                                          ###
###  https://github.com/AcevedoJetter/spotify-data-analysis  ###
################################################################

import os
import pandas as pd

def get_all_data():
    """
    Returns:
        df: pandas DataFrame with columns specified in the README.md
    """
    df = pd.DataFrame()

    for file in os.listdir("MyData"):
        if file.startswith("Streaming_History_Audio") and file.endswith(".json"):
            df = pd.concat([df, pd.read_json(f"MyData/{file}")])

    return df


def save_data_csv():
    """
    Saves the data in the json files to a big csv file
    """
    return get_all_data().to_csv("data.csv", index=False)


def get_time_playing_songs(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        times: list with time in seconds, minutes, hours, and days
    """
    milliseconds_series = data["ms_played"]
    milliseconds = milliseconds_series.sum()
    seconds = milliseconds/1000
    minutes = seconds/60
    hours = minutes/60
    days = hours/24

    return [seconds.round(2), minutes.round(2), hours.round(2), days.round(2)]


def get_different_artist(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        list: list of the different artists the account has played
    """
    return list(data["master_metadata_album_artist_name"].unique())


def get_amount_different_artist(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        list: amount of different artists the account has played
    """
    return len(get_amount_different_artist(data))


#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    data = get_all_data()
    print(get_amount_different_artist(data))
