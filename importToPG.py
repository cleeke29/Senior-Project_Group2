import psycopg2
import csv
import pandas as pd




if __name__ == '__main__':
    # mydata = pd.read_csv('my_data.csv')
    # print(mydata.head())

    # conn2 = psycopg2.connect("host=localhost dbname=livetest2 user=myuser password=pineapple9")
    # cur2 = conn2.cursor()
    # with open('my_data.csv', 'r') as f:
    #     reader = csv.reader(f, quotechar='"')
    #     next(reader)
    #     for row in reader:
    #         cur2.execute(
    #             "INSERT INTO recommender_musicdata VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #             row
    #         )
    # conn2.commit()


    conn2 = psycopg2.connect("host=localhost dbname=livetest2 user=myuser password=pineapple9")
    cur2 = conn2.cursor()
    with open('artists_w_genres_pop.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO Artist (artist_name, artist_id, artist_popularity, artist_genres) \
                    VALUES (%s, %s, %s, %s)",
                    row
                )
            except:
                continue
    with open('albums.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO Album (artist_name, album_id, album_name) \
                    VALUES (%s, %s, %s)",
                    row
                )
            except:
                continue
    with open('audio_features.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO AudioFeatures \
                        (danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, \
                            liveness, valence, tempo, id, duration_ms) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    row
                )
            except:
                continue
    with open('full_tracks.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO Track \
                        (artists, track_name, track_id, album_name, explicit, track_popularity, year, track_number) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    row
                )
            except:
                continue
    with open('genres.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO Genres \
                        (genre_id) \
                    VALUES (%s)",
                    row
                )
            except:
                continue
    with open('categories.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            try:
                cur2.execute(
                    "INSERT INTO Categories \
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