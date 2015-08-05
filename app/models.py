
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import get_ufv_data as ufv

Base = declarative_base()


class UFV_model(Base):
    __tablename__ = 'ufv_database'
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    valor = Column(Float)
    def __init__(self, fecha, valor):
        self.fecha = fecha
        self.valor = valor

class DepreciacionLRecta(Base):
    __tablename__ = 'tabla_linea_recta'
    id = id = Column(Integer, primary_key=True)
    categoria = Column(String)
    vida_util = Column(Integer)
    coeficiente = Column(Float)
    def __init__(self, categoria, vida_util, coeficiente):
        self.categoria = categoria
        self.vida_util = vida_util
        self.coeficiente = coeficiente
    
    
        
engine = create_engine('postgresql://postgres:postgres@localhost/activos')
 

Base.metadata.create_all(engine)        
#db.create_all()

