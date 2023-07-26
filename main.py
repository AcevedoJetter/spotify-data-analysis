##########################################
###  Analysis on Spotify account data  ### 
##########################################

import os
import json
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


#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    data = get_all_data()
    print(get_time_playing_songs(data))
