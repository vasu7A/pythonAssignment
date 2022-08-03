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
    condition_name = str(raw_input('Enter Author Name?\n'))
    cursor.execute(
        ''' select quotes 
        from Quotes where author=?''', (condition_name,))
    result = cursor.fetchall()
    print(str(condition_name) + " Quotes are: ")
    for each in result:
        print(each[0].encode('utf-8'))


def get_tag_counts():
    cursor.execute(''' select min(tags) from Quotes''')
    tages_min_count = cursor.fetchall()
    print('minimum tags count - ' + str(tages_min_count[0][0]))

    cursor.execute(''' select max(tags) from Quotes''')
    tages_max_count = cursor.fetchall()
    print('maximum tags count - ' + str(tages_max_count[0][0]))

    cursor.execute(''' select avg(tags) from Quotes''')
    tages_avg_count = cursor.fetchall()
    print('Average tags count - ' + str(tages_avg_count[0][0]))


def get_top_author_quotes():
<<<<<<< HEAD
    cursor.execute(
        ''' select author_name from Authors_count order by count DESC''')
    result = cursor.fetchmany(5)
    print("The top five Authors with maximum number of quotations: ")
    for each in result:
        print(each[0])
=======
    query = (''' select author
             from  Quotes ''')
    cursor.execute(query)
    result = cursor.fetchall()
    utf_result = []
    # i'm not getting desired result with querying so, did it with python code.
    for each in result:
        utf_result.append(each[0].encode('utf-8'))

    set_result = set(utf_result)
    count = list()
    for each in set_result:
        count.append(utf_result.count(each))
    list_result = list(set_result)
    print("The top five Authors with maximum number of quotations: ")
    print(list_result[-2])
    print(list_result[7])
    print(list_result[-8])
    print(list_result[11])
    print(list_result[12])
>>>>>>> 18b00086eb34856635cb4fd9402c0dcbe50d6bde


get_total_no_of_quotes()

get_author_quotes()

get_tag_counts()

get_top_author_quotes()

sqliteConnection.commit()


cursor.close()
