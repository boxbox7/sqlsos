# Sqlsos

sos! i don`t want to write f**king sql. sqlsos is a better sql-hepler for you.

### quick start

``` python
>>> from sqlsos import Field, Table
>>> name = Field('name', Field.TYPE.TEXT, pk=True)
>>> User = Table('User', name)
>>> User.create()

```