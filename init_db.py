'''
This file is to create a database (tweets.db) to store tweets information.
The database contains the following columns: “id”, “time”,
tweets information (“favorite count”, “quote count”, “retweet count”),
sentiment score (“pos”, “neg”, “neu”, “compound”), “text”, and “clean text”
'''

import sqlite3

def create_table(db_name, table_name):
    stmt = '''
    CREATE TABLE IF NOT EXISTS {} (
      'id'              INT UNIQUE,
      'created_at'      TEXT,
      'favorite_count'  INT,
      'quote_count'     INT,
      'retweet_count'   INT,
      'pos'             REAL,
      'neg'             REAL,
      'neu'             REAL,
      'compound'        REAL,
      'text'            TEXT,
      'clean_text'      TEXT
      );'''
            
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(stmt.format(table_name))
        print("Create Table {}".format(table_name))

    return

def delete_table(db_name, table_name):
    stmt = "DROP TABLE IF EXISTS {}"

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(stmt.format(table_name))
        print("Delete Table {}".format(table_name))

    return

if __name__ == '__main__':
    db_name, table_name = 'tweets.db', 'Tweets'

    while True:
        ans = input('Create or Delete Table (c or d): ')

        if ans.startswith('c'):
            create_table(db_name, table_name)
            break
        elif ans.startswith('d'):
            delete_table(db_name, table_name)
            break

