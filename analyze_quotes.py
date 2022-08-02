import sqlite3


sqliteConnection = sqlite3.connect("quotes.db")
cursor = sqliteConnection.cursor()
print('DB initialized')


def get_total_no_of_quotes():
    cursor.execute(''' select count(quotes) from Quotes ''')

    result = cursor.fetchall()
    count = result[0][0]
    print(('Total number quotes in site is ') + str(count))


def get_author_quotes():
    cursor.execute(
        ''' select quotes from Quotes where author=?''', ("Albert Einstein",))
    result = cursor.fetchall()

    for each in result:
        print(each[0].encode('utf-8'))


def get_tag_counts():
    cursor.execute(''' select min(tags) from Quotes''')
    tages_min_count = cursor.fetchall()
    print('minimum tags count ' + str(tages_min_count[0][0]))

    cursor.execute(''' select max(tags) from Quotes''')
    tages_max_count = cursor.fetchall()
    print('maximum tags count ' + str(tages_max_count[0][0]))

    cursor.execute(''' select avg(tags) from Quotes''')
    tages_avg_count = cursor.fetchall()
    print('Average tags count ' + str(tages_avg_count[0][0]))


get_total_no_of_quotes()

get_author_quotes()

get_tag_counts()

sqliteConnection.commit()


cursor.close()
