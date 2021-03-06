import psycopg2
import csv
import pandas as pd


def remove_dups(csvfile, col, output=None):
    df = pd.read_csv(csvfile)
    dupfree = df.drop_duplicates(subset=[col], keep='first')
    dups = df.pivot_table(index=[col], aggfunc='size')
    print(f'{dups} unique ids')
    if output:
        outfile = output
    else:
        outfile = csvfile

    dupfree.to_csv(outfile, index=False)
    print(f'{dups} unique ids')



if __name__ == '__main__':
    
    connect_string = "host=localhost dbname=pitch_db user=admin password=admin"

    # remove_dups('albums.csv', 'album_id', output='albums_v2.csv')
    # remove_dups('full_tracks.csv', 'id', output='full_tracks_v2.csv')
    # remove_dups('audio_features.csv', 'id', output='audio_features_v2.csv')
    # remove_dups('audio_features_v2.csv', 'id')



    # Insert artists_w_genres_pop.csv into the postgres database.
    print("starting artists")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    with open('artists_w_genres_pop.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO recommender_artist (artist_name, artist_id, artist_popularity, artist_genres) \
                    VALUES (%s, %s, %s, %s)",
                    row
                )
            except:
                print("issue in ")
                continue
    conn2.commit()



    # Insert albums_v2.csv into the postgres database.
    print("starting albums")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    count = errors = successes = 0
    with open('albums_v2.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            count += 1
            print(f'On row {count}')
            try:
                cur2.execute(
                    "INSERT INTO recommender_album (artist_name, album_name, album_id) \
                    VALUES (%s, %s, %s)",
                    row
                )
                successes += 1
                
            except:
                errors += 1
                print(f'error on row {count}')
                continue
    print(f'{errors} total errors')
    print(f'{successes} total successes')
    conn2.commit()



    # Insert audio_features_v2.csv into the postgres database.
    print("starting audio_features")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    count = successes = failures = 0
    with open('audio_features_v2.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            count += 1
            if count % 1000 == 0:
                print(f'On Row {count}')
            # try:
            cur2.execute(
                "INSERT INTO recommender_audiofeatures \
                    (danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, \
                        liveness, valence, tempo, features_id, duration_ms) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
            successes += 1
            # except:
            #     print(f'failed on row {count}')
            #     failures += 1
            #     continue
    conn2.commit()

    print(f'{count} total rows')
    print(f'{successes} successful rows')

    
    
    # Insert full_tracks_v2.csv into the postgres database.    
    print("starting tracks")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    count = successes = failures = 0
    with open('full_tracks_v2.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            count += 1
            if count % 1000 == 0:
                print(f'On Row {count}')
            # try:
            cur2.execute(
                "INSERT INTO recommender_track \
                    (artists, track_name, track_id, album_name, explicit, track_popularity, year, track_number) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
            successes += 1
            
            # except:
            #     print(f'failed on row {count}')
            #     failures += 1
            #     continue
    conn2.commit()
    print(f'{count} total rows')
    print(f'{successes} successful rows')



    # Insert genres.csv into the postgres database.
    print("starting genres")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    with open('genres.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO recommender_genres \
                        (genre_id) \
                    VALUES (%s)",
                    row
                )
            except:
                continue
    conn2.commit()



    # Insert categories.csv into the postgres database.
    print("starting categories")
    conn2 = psycopg2.connect(connect_string)
    cur2 = conn2.cursor()
    with open('categories.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO recommender_categories \
                        (category_id, category_name) \
                    VALUES (%s, %s)",
                    row
                )
            except:
                continue
    conn2.commit()

# class Genres(models.Model):
#     # genre_table_id = models.AutoField(primary_key=True)
#     genre_id = models.TextField(primary_key=True)
#     # genre_name = models.TextField()

# class Categories(models.Model):
#     # categories_table_id = models.AutoField(primary_key=True)
#     category_id = models.TextField(primary_key=True)
#     category_name = models.TextField()
