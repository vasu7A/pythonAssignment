import sqlite3
import json


with open("quotes.json", "r") as f:
    data = json.load(f)

sqliteConnection = sqlite3.connect("quotes.db")
cursor = sqliteConnection.cursor()
print('DB initialized')


def create_table_quotes():
    query = '''Drop table if exists Quotes'''
    cursor.execute(query)

    cursor.execute('''create table Quotes(
        id Integer not null,
        quotes text not null ,
        author text not null Primary Key,
        tags varchar(250) not null,
        tags_count Integer not null
        );''')

    quotes_table_id = 1

    for each in (data['quotes']):
        id = quotes_table_id
        quote = each['quote']
        author = each['author']
        tags = ",".join(each['tags'])
        tags_count = len(each['tags'])
        cursor.execute('''insert into  quotes values(?,?,?,?,?)''',
                       (id, quote, author, tags, tags_count))
        quotes_table_id += 1


def create_table_authors():
    query = '''Drop table if exists Authors'''
    cursor.execute(query)

    cursor.execute('''create table Authors(
        id Integer not null,
        born text not null,
        author text not null,
        reference text not null,
        FOREIGN KEY (author)
        REFERENCES Quotes (author)
        );''')

    Authors_table_id = 1

    for each in (data['authors']):
        id = Authors_table_id
        born = each['born']
        author = each['name']
        reference = each['reference']
        cursor.execute('''insert into  Authors values(?,?,?,?)''',
                       (id, born, author, reference))
        Authors_table_id += 1


def alter_table_with_quotes_count(authors_list):
    query = '''alter table Authors add quotes_count int'''
    cursor.execute(query)

    for each in authors_list:
        each_str = str(each)
        cursor.execute(''' select count(author) from Quotes where author 
                       =?''', (each_str.decode('utf-8'),))
        result = cursor.fetchone()
        quotes_count = result[0]

        cursor.execute('''update Authors set quotes_count = ? where author
                       =?''', (quotes_count, each_str.decode('utf-8')))


def get_unique_author_names():
    query = (''' select author
             from  Quotes ''')
    cursor.execute(query)
    result = cursor.fetchall()
    authors_list = []
    for each in result:
        authors_list.append(each[0].encode('utf-8'))

    alter_table_with_quotes_count(authors_list)


create_table_quotes()

create_table_authors()

get_unique_author_names()

sqliteConnection.commit()
cursor.close()
