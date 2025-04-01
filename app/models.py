import database
from sqlalchemy import Column, Date,Integer, String, Text

class Diario(database.base):
    __tablename__='escritura diario'
    __table_args__ = {'sqlite_autoincrement':True}
    
    id = Column(Integer,primary_key=True)
    frase=Column(Text,nullable=False)
    emocion= Column(String(50),nullable=True)
    fecha = Column(Date,nullable=True)
    
    def __init__(self,frase,emocion,fecha):
        self.frase = frase
        self.emocion = emocion
        self.fecha = fecha
    def __str__(self):
        return f'{self.id} -> {self.frase} -> {self.emocion}'