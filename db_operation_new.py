'''
This file is to use sqlite3 to calculate the 10-minute average of
information in tweets.db and import them into tweet_output.csv file containing
“time”, “counts of tweets”, “favorite average”, “quote average”, “retweet average”,
“compound sentiment score”, for further analysis of
correlation between Bitcoin price change and twitter information.
'''

import sqlite3
import pandas as pd
import csv

'''
Avaliable Columns: id, created_at, favorite_count, quote_count, retweet_count,
          pos, neg, neu, compound, text, clean_text

More SQL syntax: https://www.w3schools.com/sql/
'''

# df = pd.read_csv('tweet_output.csv')

def addFirstCol() :
    addFirstCol = []
    for i in range(1, 31):
        for j in range(0, 24):
            for k in range(6):
                timeStr = ("10/{} {:0>2}:{}0:00 ~ 10/{} {:0>2}:{}9:59".format(i, j, k, i, j, k))
                addFirstCol.append(timeStr)
        # print(timeStr)

    # The process results are imported in to tweet_output.csv
    with open('tweet_output.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Time'])
        for i in addFirstCol:
            writer.writerow([i])
    # df.insert(0, 'Time', addFirstCol)
    # df = pd.DataFrame(addFirstCol)
    # df.to_csv('tweet_output.csv', index=False)
    print(len(addFirstCol))

df = pd.read_csv('tweet_output.csv')


def october_distribution(db_name):
    tmp = []
    check = 0
    with sqlite3.connect(db_name) as conn:
        for i in range(1, 31):
            for j in range(24):
                for k in range(6):
                # print("10/1 {:0>2}:{:0>2}:00 ".format(i,j), end='')
                    # print(i, j, k)
                    cursor = conn.cursor()

                    stmt = '''SELECT COUNT(id) FROM Tweets
                    WHERE "2021-10-{:0>2} {:0>2}:{}0:00" <= created_at AND created_at <= "2021-10-{:0>2} {:0>2}:{}9:59"
                    '''.format(i, j,k, i, j,k)

                    cursor.execute(stmt)
                    # print(type(cursor.fetchone()[0]))
                    tmp.append(cursor.fetchone()[0])
                    check +=1
                    print(check)

    # print(tmp)

    # df['count_ID'] = tmp
    df.insert(1, 'count_ID', tmp)
    print(df)
    df.to_csv('tweet_output.csv', index=False)

    return

def october_distribution_Fav_AVG(db_name):
    tmp = []
    check = 0
    with sqlite3.connect(db_name) as conn:
        for i in range(1, 31):
            for j in range(24):
                for k in range(6):
                # print("10/1 {:0>2}:{:0>2}:00 ".format(i,j), end='')
                    # print(i, j, k)
                    cursor = conn.cursor()

                    stmt = '''SELECT AVG(favorite_count) FROM Tweets
                    WHERE "2021-10-{:0>2} {:0>2}:{}0:00" <= created_at AND created_at <= "2021-10-{:0>2} {:0>2}:{}9:59"
                    '''.format(i, j,k, i, j,k)

                    cursor.execute(stmt)
                    # print(type(cursor.fetchone()[0]))
                    tmp.append(cursor.fetchone()[0])
                    check +=1
                    print(check)

    # print(tmp)

    # df['Fav_AVG'] = tmp
    # print(df)
    df.insert(2, 'favorite_AVG', tmp)
    print(df)
    df.to_csv('tweet_output.csv', index=False)

    return

def october_distribution_quote_AVG(db_name):
    tmp = []
    check = 0
    with sqlite3.connect(db_name) as conn:
        for i in range(1, 31):
            for j in range(24):
                for k in range(6):
                # print("10/1 {:0>2}:{:0>2}:00 ".format(i,j), end='')
                    # print(i, j, k)
                    cursor = conn.cursor()

                    stmt = '''SELECT AVG(quote_count) FROM Tweets
                    WHERE "2021-10-{:0>2} {:0>2}:{}0:00" <= created_at AND created_at <= "2021-10-{:0>2} {:0>2}:{}9:59"
                    '''.format(i, j,k, i, j,k)

                    cursor.execute(stmt)
                    # print(type(cursor.fetchone()[0]))
                    tmp.append(cursor.fetchone()[0])
                    check +=1
                    print(check)

    # print(tmp)

    # df['quote_AVG'] = tmp
    # print(df)

    df.insert(3, 'quote_AVG', tmp)
    print(df)
    df.to_csv('tweet_output.csv', index=False)
    return


def october_distribution_retweet_AVG(db_name):
    tmp = []
    check = 0
    with sqlite3.connect(db_name) as conn:
        for i in range(1, 31):
            for j in range(24):
                for k in range(6):
                # print("10/1 {:0>2}:{:0>2}:00 ".format(i,j), end='')
                    # print(i, j, k)
                    cursor = conn.cursor()

                    stmt = '''SELECT AVG(retweet_count) FROM Tweets
                    WHERE "2021-10-{:0>2} {:0>2}:{}0:00" <= created_at AND created_at <= "2021-10-{:0>2} {:0>2}:{}9:59"
                    '''.format(i, j,k, i, j,k)

                    cursor.execute(stmt)
                    # print(type(cursor.fetchone()[0]))
                    tmp.append(cursor.fetchone()[0])
                    check +=1
                    print(check)

    # print(tmp)

    # df['retweet_AVG'] = tmp
    # print(df)
    df.insert(4, 'retweets_AVG', tmp)
    print(df)
    df.to_csv('tweet_output.csv', index=False)

    return


def october_distribution_compound_AVG(db_name):
    tmp = []
    check = 0
    with sqlite3.connect(db_name) as conn:
        for i in range(1, 31):
            for j in range(24):
                for k in range(6):
                # print("10/1 {:0>2}:{:0>2}:00 ".format(i,j), end='')
                    # print(i, j, k)
                    cursor = conn.cursor()

                    stmt = '''SELECT AVG(compound) FROM Tweets
                    WHERE "2021-10-{:0>2} {:0>2}:{}0:00" <= created_at AND created_at <= "2021-10-{:0>2} {:0>2}:{}9:59"
                    '''.format(i, j,k, i, j,k)

                    cursor.execute(stmt)
                    # print(type(cursor.fetchone()[0]))
                    tmp.append(cursor.fetchone()[0])
                    check +=1
                    print(check)

    # print(tmp)

    # df['compound_AVG'] = tmp
    # print(df)
    df.insert(5, 'compound_AVG', tmp)
    print(df)
    df.to_csv('tweet_output.csv', index=False)

    return


if __name__ == '__main__':
    db_name, table_name = 'tweets.db', 'Tweets'

    # select specific elements with specific time range and oreber by specific element
    select_stmt = '''
    SELECT created_at,favorite_count FROM Tweets 
    WHERE "2021-10-01 00:00:00" < created_at AND created_at < "2021-10-01 00:15:00" 
    ORDER BY created_at;'''

    # find the maximun and minimum value of specific element
    maxmin_stmt = "SELECT MAX(created_at),MIN(created_at) FROM Tweets;"

    # Sum, Count and Average
    ## Count is to calculate the total numbers of the element so sum/count = avg
    sum_stmt = "SELECT SUM(pos),COUNT(pos),AVG(pos) FROM Tweets;"

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
#        cursor.execute(select_stmt)
#        cursor.execute(maxmin_stmt) # ('2021-11-03 01:18:53', '2007-10-09 19:56:57')
#        cursor.execute(sum_stmt)

        '''
        # data type is tuple even if there is only one element
        for data in cursor.fetchall():
            print(data)
            break
        '''

    addFirstCol()
    # october_distribution(db_name)
    # october_distribution_Fav_AVG(db_name)
    october_distribution_quote_AVG(db_name)
    october_distribution_retweet_AVG(db_name)
    october_distribution_compound_AVG(db_name)
