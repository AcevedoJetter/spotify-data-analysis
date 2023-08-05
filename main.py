################################################################
###         Analysis on Spotify account extended data        ### 
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


def most_streamed_artist_time(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with artist and decending order of time played in ms
    """
    data = data[["master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False)["ms_played"].sum()
    new_data = new_data.sort_values(["ms_played", "master_metadata_album_artist_name"], ascending=[False, True])
    return new_data


def most_streamed_artist_amount(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with artist and decending order of amount of songs played
    """
    data = data[["master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False).count()
    new_data = new_data.rename(columns={"ms_played" : "times_played"})
    new_data = new_data.sort_values(["times_played", "master_metadata_album_artist_name"], ascending=[False, True])
    return new_data


def most_streamed_song_time(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with song, artist, and decending order of time played in ms
    """
    data = data[["master_metadata_track_name", "master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False)["ms_played"].sum()
    new_data = new_data.sort_values(["ms_played", "master_metadata_track_name", "master_metadata_album_artist_name"], ascending=[False, True, True])
    return new_data


def most_streamed_song_amount(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with song, artist and decending order of amount played
    """
    data = data[["master_metadata_track_name", "master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False).count()
    new_data = new_data.rename(columns={"ms_played" : "times_played"})
    new_data = new_data.sort_values(["times_played", "master_metadata_track_name", "master_metadata_album_artist_name"], ascending=[False, True, True])
    return new_data


def shuffle_ratio(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        list: list with the percent of shuffled to non shuffled songs
    """
    df_shuffle = data.groupby(data["shuffle"])["shuffle"].count()
    true = df_shuffle[True]
    false = df_shuffle[False]
    total = true + false

    return [(true/total*100).round(2), (false/total*100).round(2)]


def offline_ratio(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        list: list with the percent of offline to online songs
    """
    df_offline = data.groupby(data["offline"])["offline"].count()
    true = df_offline[True]
    false = df_offline[False]
    total = true + false

    return [(true/total*100).round(2), (false/total*100).round(2)]

    




#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    data = get_all_data()
    print(offline_ratio(data))
