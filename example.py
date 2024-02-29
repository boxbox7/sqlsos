import sqlsos as ss

fields = [
    ss.IDField(),
    ss.CharField('name', max_length=20)
]
user = ss.Table('user', *fields)
print(user.create())
# CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER NOT NULL, name TEXT NOT NULL, email TEXT);
print(user.drop())
# DROP TABLE user;
print(user.insert(name='box'))
# INSERT INTO user (name, email) VALUES (box, xxxx@gmail.com);
print(user.select('name').where(name='box', id=1).dump())



