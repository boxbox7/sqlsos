from .models import Field


class IDField(Field):
    def __init__(self,
                 name='id',
                 pk=True,
                 null=False,
                 auto_increment=True
                 ):
        super().__init__(name,
                         self.TYPE.INTEGER,
                         pk=pk,
                         null=null,
                         auto_increment=auto_increment)


class TextField(Field):
    def __init__(self,
                 name,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        super().__init__(name,
                         self.TYPE.TEXT,
                         pk=pk,
                         null=null,
                         auto_increment=auto_increment)


class IntegerField(Field):

    def __init__(self,
                 name,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        super().__init__(name,
                         self.TYPE.INTEGER,
                         pk=pk,
                         null=null,
                         auto_increment=auto_increment)


class REALField(Field):
    def __init__(self,
                 name,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        super().__init__(name,
                         self.TYPE.REAL,
                         pk=pk,
                         null=null,
                         auto_increment=auto_increment)


class BLOBField(Field):
    def __init__(self,
                 name,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        super().__init__(name,
                         self.TYPE.BLOB,
                         pk=pk,
                         null=null,
                         auto_increment=auto_increment)
