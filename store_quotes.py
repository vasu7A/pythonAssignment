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
    quotes text not null Primary Key,
    author text not null,
    tags Integer not null
    );''')

for each in (data['quotes']):
    quote = each['quote']
    author = each['author']
    tags = len(each['tags'])
    cursor.execute('''insert into  quotes values(?,?,?)''',
                   (quote, author, tags))


query = '''Drop table if exists Authors'''
cursor.execute(query)

cursor.execute('''create table Authors(
    born text not null,
    author text not null,
    reference text not null
    );''')

for each in (data['authors']):
    born = each['born']
    author = each['name']
    reference = each['reference']
    cursor.execute('''insert into  Authors values(?,?,?)''',
                   (born, author, reference))


sqliteConnection.commit()


cursor.close()
