
import tables
import os
import pandas as pd

def main():
    directory = 'MillionSongSubset/data'

    dictionary_artists = []
    dictionary_songs = []
    dictionary_similarartists = []
    i = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filename = subdir + os.sep + file
            if filename.endswith(".h5"):
                h5 = open_h5_file_read(filename)

                artist_id = get_artist_id(h5)
                artist_name = get_artist_name(h5)
                artist_location = get_artist_location(h5)
                artist_latitude = get_artist_latitude(h5)
                artist_longitude = get_artist_longitude(h5)
                artist_hotness = get_artist_hotttnesss(h5)
                artist_familiarity = get_artist_familiarity(h5)

                artists = {
                         'key_id': 0,
                         'artist_id': artist_id,
                         'name': artist_name,
                         'location': artist_location,
                         'latitude': artist_latitude,
                         'longitude': artist_longitude,
                         'hotness': artist_hotness,
                         'familiarity': artist_familiarity
                         }

                duplicateartist = False
                for d_artists in dictionary_artists:
                    if  artist_id in d_artists.values():
                        duplicateartist = True
                        break
                if not duplicateartist:
                    dictionary_artists.append(artists)

                song_id = get_song_id(h5)
                song_title = get_title(h5)
                song_year = get_year(h5)
                song_duration = get_duration(h5)
                song_danceability = get_danceability(h5)
                song_energy = get_energy(h5)
                song_hotness = get_song_hotttnesss(h5)
                song_mode = get_mode(h5)
                song_tempo = get_tempo(h5)

                if song_title != "":
                    songs = {
                            'key_id': 0,
                            'song_id': song_id,
                            'title': song_title,
                            'artist_id': artist_id,
                            'artist_key_id': 0,
                            'year': song_year,
                            'duration': song_duration,
                            'danceability': song_danceability,
                            'energy': song_energy,
                            'hotness': song_hotness,
                            'mode': song_mode,
                            'tempo': song_tempo
                            }
                    dictionary_songs.append(songs)

                artist_similarartists = get_similar_artists(h5)

                for similarartist_id in artist_similarartists:
                    similarartists = {
                               'key_id': 0,
                               'artist_key_id': 0,
                               'similarartist_key_id': 0,
                               'artist_id': artist_id,
                               'similarartist_id': str(similarartist_id).replace("b'", "").replace("'", "")
                               }

                    if not duplicateartist:
                        dictionary_similarartists.append(similarartists)

                h5.close()
                i = i + 1
                print(i)

    i = 0
    artist_key_id = 1
    for val in dictionary_artists:
        val['key_id'] = artist_key_id
        artist_key_id += 1
        i = i + 1
        print(i)

    i = 0
    song_key_id = 1
    for val in dictionary_songs:
        val['key_id'] = song_key_id
        song_key_id += 1
        i = i + 1
        print(i)

    i = 0
    similarartist_key_id = 1
    for val in dictionary_similarartists:
        val['key_id'] = similarartist_key_id
        similarartist_key_id += 1
        i = i + 1
        print(i)

    dataset_artists = pd.DataFrame.from_dict(dictionary_artists)
    dataset_songs = pd.DataFrame.from_dict(dictionary_songs)
    dataset_similarartists = pd.DataFrame.from_dict(dictionary_similarartists)

    dataset_artists['latitude'].fillna(0, inplace=True)
    dataset_artists['longitude'].fillna(0, inplace=True)
    dataset_artists['hotness'].fillna(0, inplace=True)
    dataset_artists['familiarity'].fillna(0, inplace=True)

    dataset_songs['danceability'].fillna(0, inplace=True)
    dataset_songs['energy'].fillna(0, inplace=True)
    dataset_songs['hotness'].fillna(0, inplace=True)
    dataset_songs['mode'].fillna(0, inplace=True)

    dataset_artists.to_csv('MillionSongSubset/csv/artists.csv',index=False)
    dataset_songs.to_csv('MillionSongSubset/csv/songs.csv',index=False)
    dataset_similarartists.to_csv('MillionSongSubset/csv/similarartists.csv',index=False)

def open_h5_file_read(h5filename):\
    #Open an existing H5 in read mode.
    #Same function as in hdf5_utils, here so we avoid one import
    return tables.open_file(h5filename, mode='r')

def get_artist_familiarity(h5, songidx=0):
    #Get artist familiarity from a HDF5 song file, by default the first song in it
    return h5.root.metadata.songs.cols.artist_familiarity[songidx]


def get_artist_hotttnesss(h5, songidx=0):
    #Get artist hotttnesss from a HDF5 song file, by default the first song in it
    return h5.root.metadata.songs.cols.artist_hotttnesss[songidx]


def get_artist_id(h5, songidx=0):
    #Get artist id from a HDF5 song file, by default the first song in it
    return str(h5.root.metadata.songs.cols.artist_id[songidx]).replace("b'", "").replace("'", "").replace('"', '')


def get_artist_latitude(h5, songidx=0):
    #Get artist latitude from a HDF5 song file, by default the first song in it
    return h5.root.metadata.songs.cols.artist_latitude[songidx]


def get_artist_longitude(h5, songidx=0):
    #Get artist longitude from a HDF5 song file, by default the first song in it
    return h5.root.metadata.songs.cols.artist_longitude[songidx]


def get_artist_location(h5, songidx=0):
    #Get artist location from a HDF5 song file, by default the first song in it
    return str(h5.root.metadata.songs.cols.artist_location[songidx]).replace("b'", "").replace("'", "").replace('"', '')


def get_artist_name(h5, songidx=0):
    #Get artist name from a HDF5 song file, by default the first song in it
    return str(h5.root.metadata.songs.cols.artist_name[songidx]).replace("b'", "").replace("'", "").replace('"', '')


def get_release(h5, songidx=0):
    """
    Get release from a HDF5 song file, by default the first song in it
    """
    return h5.root.metadata.songs.cols.release[songidx]


def get_song_id(h5, songidx=0):
    """
    Get song id from a HDF5 song file, by default the first song in it
    """
    return str(h5.root.metadata.songs.cols.song_id[songidx]).replace("b'", "").replace("'", "").replace('"', '')


def get_song_hotttnesss(h5, songidx=0):
    """
    Get song hotttnesss from a HDF5 song file, by default the first song in it
    """
    return h5.root.metadata.songs.cols.song_hotttnesss[songidx]


def get_title(h5, songidx=0):
    """
    Get title from a HDF5 song file, by default the first song in it
    """
    return str(h5.root.metadata.songs.cols.title[songidx]).replace("b'", "").replace("'", "").replace('"', '')

def get_tempo(h5,songidx=0):
    """
    Get tempo from a HDF5 song file, by default the first song in it
    """
    return h5.root.analysis.songs.cols.tempo[songidx]

def get_similar_artists(h5, songidx=0):
    """
    Get similar artists array. Takes care of the proper indexing if we are in aggregate
    file. By default, return the array for the first song in the h5 file.
    To get a regular numpy ndarray, cast the result to: numpy.array( )
    """
    return h5.root.metadata.similar_artists[h5.root.metadata.songs.cols.idx_similar_artists[songidx]:]


def get_danceability(h5, songidx=0):
    """
    Get danceability from a HDF5 song file, by default the first song in it
    """
    return h5.root.analysis.songs.cols.danceability[songidx]


def get_duration(h5, songidx=0):
    """
    Get duration from a HDF5 song file, by default the first song in it
    """
    return h5.root.analysis.songs.cols.duration[songidx]


def get_energy(h5, songidx=0):
    """
    Get energy from a HDF5 song file, by default the first song in it
    """
    return h5.root.analysis.songs.cols.energy[songidx]

def get_mode(h5, songidx=0):
    """
    Get mode from a HDF5 song file, by default the first song in it
    """
    return h5.root.analysis.songs.cols.mode[songidx]


def get_year(h5, songidx=0):
    """
    Get release year from a HDF5 song file, by default the first song in it
    """
    return h5.root.musicbrainz.songs.cols.year[songidx]


if __name__ == "__main__":
    main()
