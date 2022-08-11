import sqlite3


sqliteConnection = sqlite3.connect("quotes.db")
cursor = sqliteConnection.cursor()
print('DB initialized')


def get_total_no_of_quotes():
    cursor.execute(''' select count(quotes) from Quotes''')

    result = cursor.fetchall()
    count = result[0][0]
    print(('Total number of unique quotes in site is : ') + str(count))


def get_author_quotes_count():
    cursor.execute(
        ''' select quotes 
        from Quotes where author=?''', ('Albert Einstein',))
    result = cursor.fetchall()
    print("Albert Einstein Quotes count is : " + str(len(result)))


def get_tag_counts():
    cursor.execute(''' select min(tags),max(tags),avg(tags) from Quotes''')
    tages_count = cursor.fetchall()
    print('minimum tags count - ' + str(tages_count[0][0]))
    print('maximum tags count - ' + str(tages_count[0][1]))
    print('Average tags count - ' + str(tages_count[0][2]))


def get_top_author_quotes():
    cursor.execute(
        ''' select author from Authors order by quotes_count DESC''')
    result = cursor.fetchmany(5)
    print("The top five Authors with maximum number of quotations: ")
    for each in result:
        print(each[0])


get_total_no_of_quotes()

get_author_quotes_count()

get_tag_counts()

get_top_author_quotes()

sqliteConnection.commit()


cursor.close()
