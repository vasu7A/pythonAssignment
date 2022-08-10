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
    id Integer not null,
    quotes text not null ,
    author text not null Primary Key,
    tags Integer not null
    );''')

quotes_table_id = 1


for each in (data['quotes']):
    id = quotes_table_id
    quote = each['quote']
    author = each['author']
    tags = len(each['tags'])
    cursor.execute('''insert into  quotes values(?,?,?,?)''',
                   (quote, author, tags, id))
    quotes_table_id += 1


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


sqliteConnection.commit()
cursor.close()
