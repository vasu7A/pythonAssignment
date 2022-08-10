import sqlite3


sqliteConnection = sqlite3.connect("quotes.db")
cursor = sqliteConnection.cursor()
print('DB initialized')


def get_total_no_of_quotes():
    cursor.execute(''' select count(quotes) from Quotes ''')

    result = cursor.fetchall()
    count = result[0][0]
    print(('Total number quotes in site is ') + str(count))


def get_author_quotes_count():
    cursor.execute(
        ''' select quotes 
        from Quotes where author=?''', ('Albert Einstein',))
    result = cursor.fetchall()
    print("Albert Einstein Quotes count is : ")
    print(len(result))


def get_tag_counts():
    cursor.execute(''' select min(tags),max(tags),avg(tags) from Quotes''')
    tages_count = cursor.fetchall()
    print('minimum tags count - ' + str(tages_count[0][0]))
    print('maximum tags count - ' + str(tages_count[0][1]))
    print('Average tags count - ' + str(tages_count[0][2]))


get_total_no_of_quotes()

get_author_quotes_count()

get_tag_counts()


sqliteConnection.commit()


cursor.close()
