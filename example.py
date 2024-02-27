import sqlsos as ss

fields = [
    ss.IDField(),
    ss.CharField('name')
]

user = ss.Table('user', *fields)
print(user.create())
# CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER NOT NULL, name TEXT NOT NULL, email TEXT);
print(user.drop())
# DROP TABLE user;
print(user.insert(name='box'))
# INSERT INTO user (name, email) VALUES (box, xxxx@gmail.com);
ss.select('User', ['name', 'age', 'email']).where(name='boxbox').order_by(name='desc').to_sql()



