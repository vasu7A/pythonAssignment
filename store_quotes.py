import sqlite3
import json


with open("quotes.json", "r") as f:
    data = json.load(f)

sqliteConnection = sqlite3.connect("quotes.db")
cursor = sqliteConnection.cursor()
print('DB initialized')

query = '''Drop table if exists Quotes'''
cursor.execute(query)

cursor.execute('''create table Quotes(
    id Integer not null Primary Key,
    quotes text not null ,
    author text not null,
    tags Integer not null
    );''')

count = 1

for each in (data['quotes']):
    quote = each['quote']
    author = each['author']
    tags = len(each['tags'])
    id = count
    cursor.execute('''insert into  quotes values(?,?,?,?)''',
                   (id, quote, author, tags))
    count += 1


query = '''Drop table if exists Authors'''
cursor.execute(query)


cursor.execute('''create table Authors(
    id Integer not null,
    born text not null,
    author text not null,
    reference text not null,
    FOREIGN KEY (id)
       REFERENCES Quotes (id)
    );''')

Authors_id = 1

for each in (data['authors']):
    id = count
    born = each['born']
    author = each['name']
    reference = each['reference']
    cursor.execute('''insert into  Authors values(?,?,?,?)''',
                   (id, born, author, reference))
    Authors_id += 1


def create_with_table_unique_authors(c, each, quotes_count):
    cursor.execute('''insert into Authors_count values(?,?,?)''',
                   (c, each.decode('utf-8'), quotes_count))


def create_with_unique_authors(unique_authors):
    query = '''Drop table if exists Authors_count'''
    cursor.execute(query)

    cursor.execute('''create table Authors_count(
        id Integer not null,
        author_name text not null,
        count Integer not null,
        FOREIGN KEY (id)
        REFERENCES Quotes (id)
        );''')

    quotes_id = 1

    for each in unique_authors:
        each_str = str(each)
        cursor.execute(''' select count(author) from Quotes where author =?''',
                       (each_str.decode('utf-8'),))
        result = cursor.fetchone()
        quotes_count = result[0]
        create_with_table_unique_authors(quotes_id, each, quotes_count)
        quotes_id += 1


unique_authors = set()


def get_unique_author_names():
    query = (''' select author
             from  Quotes ''')
    cursor.execute(query)
    result = cursor.fetchall()
    utf_result = []
    for each in result:
        utf_result.append(each[0].encode('utf-8'))

    unique_authors = set(utf_result)
    create_with_unique_authors(unique_authors)


get_unique_author_names()


sqliteConnection.commit()


cursor.close()
