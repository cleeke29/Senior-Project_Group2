import psycopg2
import csv
import pandas as pd




if __name__ == '__main__':
    mydata = pd.read_csv('my_data.csv')
    print(mydata.head())

    conn2 = psycopg2.connect("host=localhost dbname=livetestdb user=liveuser password=simran")
    cur2 = conn2.cursor()
    with open('my_data.csv', 'r') as f:
        reader = csv.reader(f, quotechar='"')
        next(reader)
        for row in reader:
            cur2.execute(
                "INSERT INTO recommender_musicdata VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
    conn2.commit()
