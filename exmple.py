import sqlsos as ss

fields = [
    ss.IDField(),
    ss.IntegerField('age'),
    ss.TextField('name'),
    ss.TextField('email', null=True)
]

user = ss.Table('user', *fields)
print(user.create())
# CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER NOT NULL, name TEXT NOT NULL, email TEXT);
print(user.drop())
# DROP TABLE user;
print(user.insert(name='box', email='xxxx@gmail.com', age=14))
# INSERT INTO user (name, email) VALUES (box, xxxx@gmail.com);
