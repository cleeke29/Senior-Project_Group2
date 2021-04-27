"""
@author: Edward Callihan
Created: 3/3/2021
Last Updated: 4/27/2021 -> comments

"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import re

"""
This method breaks csv files into smaller csv files to avoid timing out in the 
spotify api.
"""
def break_up_csv(input_csv, size_of_chunks=200000):
    lines = []
    with open(input_csv, 'r') as f:
        
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            lines.append(row)
        line_count = len(lines)
        
        print(len(lines))
        file_num = 1
        chunk_size = size_of_chunks
        off_chunk = line_count % chunk_size
        num_chunks = (line_count - off_chunk) // chunk_size

        start = 0
        end = off_chunk
        count = 1
        print('end: ', end)
        while end <= line_count:
            print(f'chunks left: {num_chunks - count}')
            count = count + 1
            with open(f'{input_csv[:-4]}{file_num}{input_csv[-4:]}', 'w') as wf:
                file_num = file_num + 1
                writer = csv.writer(wf)
                writer.writerow(header)
                writer.writerows(lines[start:end])
                start = end
                end = end + chunk_size


class SpotipyDataMaker:
    def __init__(self, client_id, client_secret):
        self.client_credentials_manager = SpotifyClientCredentials(client_id='71c78c8e5cca415cbdbbbda0454407b6',
                                                                   client_secret='e207718d7a034b838f38dc445225f8a7')
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager, requests_timeout=20)
        self.scope = "user-library-read"

        #####################################################################################
        # This method takes a csv file with the track ids and returns a list with column information
        #####################################################################################

    def list_from_csv_rows(self, csv_input='tracks.csv', id_col="track_id"):
        my_ids = []
        with open(csv_input, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                my_ids.append(row[id_col])
        return my_ids

#####################################################################################
        # This section scrapes genres
        #####################################################################################      
        #
    def get_genres_from_spotify(self):

        seeds = self.sp.recommendation_genre_seeds()
        with open('genres.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['genres'])
            genres = seeds['genres']
            for i in range(len(genres)):
                writer.writerow([genres[i]])

        #####################################################################################
        # This section scrapes the categories
        #####################################################################################
    def get_categories_from_spotify(self):

        my_rows = []
        category = self.sp.categories(country='US', limit=50)
        print(category['categories']['items'])
        print(len(category['categories']['items']))
        items = category['categories']['items']
        for i in range(len(items)):
            print(f'{items[i]["name"]} : {items[i]["id"]}')
            my_rows.append([items[i]['name'], items[i]['id']])

        with open('categories.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['category', 'category_id'])
            writer.writerows(my_rows)
        #####################################################################################

        #####################################################################################
        # This pulls the first artist in artist, adds it to a set, then creates a csv file with the artists' names and 
        # spotify ids
        #####################################################################################
    def get_first_listed_artists(self, input_csv='data.csv', output_csv='artists.csv', artist_col='artists'):

        my_set = set()
        with open(input_csv, 'r') as f:
            reader = csv.DictReader(f, quotechar='"')
            
            for row in reader:
                artists = row[artist_col]
                artists = re.match('^\[\'.*?\'[\,\]]', artists)
                try:
                    artist = artists.group(0)
                    my_set.add(artist[2:-2])

                except:
                    pass    
        my_list = list(my_set)
        my_rows = []
        for i in range(len(my_list)):
            try:
                result = self.sp.search(my_list[i])

                print(f'ids left: {len(my_list) - i}')
                seek_artist = my_list[i]
                find_artist = result['tracks']['items'][0]['artists'][0]['name']
                id_artist = result['tracks']['items'][0]['artists'][0]['id']
                if find_artist == seek_artist:
                    my_rows.append([find_artist, id_artist])
            except IndexError:
                continue

        with open(output_csv, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['artist', 'id'])
            writer.writerows(my_rows)
            
        #####################################################################################


        #####################################################################################
        # This function pulls the album ids from all the artists in artists.csv
    #####################################################################################
    def get_album_ids_from_artists_csv(self, input_csv='artists.csv', output_csv='albums.csv', id_col='id'):

        my_rows = []
        my_set = self.list_from_csv_rows(csv_input=input_csv, id_col=id_col)
        
        for j in range(len(my_set)):
            print(len(my_set) - j)
            result = self.sp.artist_albums(my_set[j], limit=50, album_type='album')

        # print(len(result['items']))
            for i in range(len(result['items'])):
                print(len(result['items']) - i)
                artist = result['items'][i]['artists'][0]['name']
                album = result['items'][i]['name']
                album_id = result['items'][i]['id']
                my_rows.append([artist, album, album_id])

        with open(output_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['artist', 'album', 'album_id'])
            writer.writerows(my_rows)
        ######################################################################################################


        ######################################################################################################
        # This furnction updates the artists data to include their name, id, popularity and genres
        ######################################################################################################
    def get_artist_info_from_csv(self, input_csv='artists.csv', output_csv='artists_w_genres_pop.csv', id_col='id'):

        my_rows = []
        my_ids = self.list_from_csv_rows(csv_input=input_csv, id_col='id')

        for i in range(len(my_ids)):
            print(len(my_ids) - i)
            artist = self.sp.artist(my_ids[i])
            name = artist['name']
            id = artist['id']
            popularity = artist['popularity']
            genres = artist['genres']
            my_rows.append([name, id, popularity, genres])

        with open(output_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'id', 'popularity', 'genres'])
            writer.writerows(my_rows)


        #############################################################################################################
        # this function pulls track data from every album in albums.csv
        #############################################################################################################
    def get_tracks_from_album_csv(self, input_csv='albums.csv', output_csv='tracks.csv', id_col='album_id'):

        my_rows = []
        my_list = self.list_from_csv_rows(csv_input=input_csv, id_col=id_col)

        for i in range(len(my_list)):
            result = self.sp.album(my_list[i])
            print(f'albums left: {len(my_list) - i}')
            for j in range(len(result['tracks']['items'])):
                
                artist = result['artists'][0]['name']
                album = result['name']
                track = result['tracks']['items'][j]['name']
                track_no = result['tracks']['items'][j]['track_number']
                track_id = result['tracks']['items'][j]['id']
                print(track_no)
                my_rows.append([artist, album, track, track_no, track_id])

        with open(output_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['artist', 'album', 'track', 'track_no', 'track_id'])
            writer.writerows(my_rows)
        #####################################################################################################

        ######################################################################################################
        # This method takes a file with the track ids and creates a csv with track information
        ######################################################################################################

    def get_track_info_from_tracks_csv(self, csv_input='tracks.csv', csv_output='full_tracks.csv', id_col='track_id'):

        my_ids = self.list_from_csv_rows(csv_input=csv_input, id_col=id_col)

        chunk_size = 50
        off_chunk = len(my_ids) % chunk_size
        chunks = (len(my_ids) - off_chunk) / chunk_size

        my_rows = []
        tracks = self.sp.tracks(my_ids[:off_chunk])['tracks']
        for i in range(len(tracks)):
            artists = tracks[i]['artists']
            artist_list = set()
            for j in range(len(artists)):
                artist_list.add(artists[j]['name'])
            artist_list = list(artist_list)
            name = tracks[i]['name']
            id = tracks[i]['id']
            album = tracks[i]['album']['name']
            explicit = tracks[i]['explicit']
            popularity = tracks[i]['popularity']
            year_released = tracks[i]['album']['release_date'][:4]
            track_no = tracks[i]['track_number']
            my_rows.append([artist_list, name, id, album, explicit, popularity, year_released, track_no])

        print('first chunk done')

        with open(csv_output, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['artists', 'name', 'id', 'album', 'explicit', 'popularity', 'year_released', 'track_no'])
            writer.writerows(my_rows)

        end = off_chunk + chunk_size
        start = off_chunk
        count = 0
        while end <= len(my_ids):
            print(f'Chunks left: {chunks - count}')
            count = count + 1
            my_rows = []
            tracks = self.sp.tracks(my_ids[start: end])['tracks']
            for i in range(len(tracks)):
                artists = tracks[i]['artists']
                artist_list = set()
                for j in range(len(artists)):
                    artist_list.add(artists[j]['name'])
                artist_list = list(artist_list)
                name = tracks[i]['name']
                id = tracks[i]['id']
                album = tracks[i]['album']['name']
                explicit = tracks[i]['explicit']
                popularity = tracks[i]['popularity']
                year_released = tracks[i]['album']['release_date'][:4]
                track_no = tracks[i]['track_number']
                my_rows.append([artist_list, name, id, album, explicit, popularity, year_released, track_no])

            with open(csv_output, 'a') as f:
                writer = csv.writer(f)
                writer.writerows(my_rows)


            start += chunk_size
            end += chunk_size

        #############################################################################################################
        # This function scrapes all relevant song data for songs with spotify ids 
        # id_col: header for column with spotify song ids 
        # size_of_chunks: number of ids to process at a time. max=default=50
        #############################################################################################################
    def get_audio_features_from_tracks_csv(self, input_csv='tracks.csv', output_csv='audio_features.csv', id_col='track_id', size_of_chunks=50, append=False):
        
        my_ids = self.list_from_csv_rows(csv_input=input_csv, id_col=id_col)
        print(f'count: {len(my_ids)}')
        # setting up to process slices of the id list
        chunk_size = size_of_chunks
        off_chunk = len(my_ids) % chunk_size
        chunks = (len(my_ids) - off_chunk) / chunk_size

        my_rows = []
        if off_chunk == 0:
            off_chunk = chunk_size
        tracks = self.sp.audio_features(my_ids[:off_chunk]) # Spotipy API
        print(tracks[0])
        for i in range(len(tracks)):
            if tracks[i]:
                danceability = tracks[i]['danceability']
                energy = tracks[i]['energy']
                key = tracks[i]['key']
                loudness = tracks[i]['loudness']
                mode = tracks[i]['mode']
                speechiness = tracks[i]['speechiness']
                acousticness = tracks[i]['acousticness']
                instrumentalness = tracks[i]['instrumentalness']
                liveness = tracks[i]['liveness']
                valence = tracks[i]['valence']
                tempo = tracks[i]['tempo']
                id = tracks[i]['id']
                duration_ms = tracks[i]['duration_ms']
                my_rows.append([danceability, energy, key, loudness, mode, 
                                speechiness, acousticness, instrumentalness,
                                liveness, valence, tempo, id, duration_ms])


        features = ['danceability', 'energy', 'key', 'loudness', 'mode', 
            'speechiness', 'acousticness', 'instrumentalness', 'liveness',
            'valence', 'tempo', 'id', 'duration_ms']
        mode = 'a' if append else 'w'
        with open(output_csv, mode) as f:
            writer = csv.writer(f)
            if not append:
                writer.writerow(features) 
            writer.writerows(my_rows)

        # Adjusting array slice indices
        end = off_chunk + chunk_size
        start = off_chunk
        count = 0
        
        while end <= len(my_ids):
            print(f'Chunks left: {chunks - count}')
            count = count + 1
            my_rows = []
            tracks = self.sp.audio_features(my_ids[start:end])
            for i in range(len(tracks)):
                if tracks[i]:
                    danceability = tracks[i]['danceability']
                    energy = tracks[i]['energy']
                    key = tracks[i]['key']
                    loudness = tracks[i]['loudness']
                    mode = tracks[i]['mode']
                    speechiness = tracks[i]['speechiness']
                    acousticness = tracks[i]['acousticness']
                    instrumentalness = tracks[i]['instrumentalness']
                    liveness = tracks[i]['liveness']
                    valence = tracks[i]['valence']
                    tempo = tracks[i]['tempo']
                    id = tracks[i]['id']
                    duration_ms = tracks[i]['duration_ms']
                    my_rows.append([danceability, energy, key, loudness, mode, 
                                    speechiness, acousticness, instrumentalness,
                                    liveness, valence, tempo, id, duration_ms])

            with open(output_csv, 'a') as f:
                writer = csv.writer(f)
                writer.writerows(my_rows)

            start += chunk_size
            end += chunk_size

    def get_big_data(self, input_csv='data.csv', artists_col='artists'):
        self.get_genres_from_spotify()
        self.get_categories_from_spotify()
        self.get_first_listed_artists()
        self.get_artist_info_from_csv()
        self.get_album_ids_from_artists_csv()
        self.get_tracks_from_album_csv()
        self.get_track_info_from_tracks_csv()
        self.get_audio_features_from_tracks_csv()

if __name__ == '__main__':
    dm = SpotipyDataMaker(client_id='71c78c8e5cca415cbdbbbda0454407b6', client_secret='e207718d7a034b838f38dc445225f8a7')
    # chunk_size = len(dm.list_from_csv_rows(csv_input='full_tracks_v2.csv', id_col='id'))  // 5

    # print(f'chunk size: {chunk_size}')
    # break_up_csv('full_tracks_v2.csv', size_of_chunks=chunk_size)
    dm.get_audio_features_from_tracks_csv(input_csv='full_tracks_v26.csv', id_col='id', output_csv='audio_features.csv', append=True)



# client_credentials_manager = SpotifyClientCredentials(client_id='71c78c8e5cca415cbdbbbda0454407b6',
#                                                       client_secret='e207718d7a034b838f38dc445225f8a7')