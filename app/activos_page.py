#from app import app, db
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

import get_ufv_data as ufv
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/activos'
db = SQLAlchemy(app)

class UFV_model(db.Model):
    __tablename__ = 'ufv_database'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    valor = db.Column(db.Float)
    def __init__(self, fecha, valor):
        self.fecha = fecha
        self.valor = valor

db.create_all()

ufv_2012 = ufv.get_ufv_data(1,1,2014,31,12,2014)
print "df ready"
fechas = ufv_2012['Fecha'].tolist()
valores =  ufv_2012['Valor de la UFV'].tolist()
for i in range(len(fechas)):
    
    temp = UFV_model(fecha = fechas[i] , valor = valores[i])
    db.session.add(temp)
    db.session.commit()


print 'updated'


