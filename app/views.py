
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

import get_ufv_data as ufv

import datetime

#from flask.ext.sqlalchemy import get_debug_queries

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql
from models import UFV_model, DepreciacionLRecta, Base

###########################################################
#Para hacer upload de files
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/ubuntu/workspace/app/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'xlsx', 'xls', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

############################################################

############################################################

#Conexion a la base de datos
engine = create_engine('postgresql://postgres:postgres@localhost/activos')
cnx = engine.raw_connection()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
############################################################
@app.route('/')
@app.route('/index')
def index():
    ufvLastVal = session.query(UFV_model).order_by(desc(UFV_model.fecha)).first()
    fechaUltimoRegistro = ufvLastVal.fecha
    fechaSiguiente = fechaUltimoRegistro + datetime.timedelta(days=1)
    fechaHoy = datetime.datetime.today()
    newData = ufv.get_ufv_data(fechaSiguiente, fechaHoy)
    if type(newData) != bool :
        header = newData.columns.values.tolist()
        fechas = newData['Fecha'].tolist()
        valores =  newData['Valor de la UFV'].tolist()
        for i in range(len(fechas)):
            temp = UFV_model(fecha = fechas[i] , valor = valores[i])
            session.add(temp)
            session.commit()
    firstDeprVal = session.query(DepreciacionLRecta).first()
    boolean = firstDeprVal is None
    if boolean:
        deprDF = ufv.depreciacion_data()
        headers = deprDF.columns.tolist()
        bienesU = deprDF["BIENES DE USO"].tolist()
        vidaU =  deprDF["Vida Util"].tolist()
        coefU = deprDF["Coeficiente"].tolist()
        for i in xrange(len(bienesU)):
            temp2 = DepreciacionLRecta(categoria = str(bienesU[i]), vida_util = int(vidaU[i]), coeficiente = float(coefU[i]))
            session.add(temp2)
            session.commit()
        print "import successful"
    DeprTable = session.query(DepreciacionLRecta)
    ufvData = session.query(UFV_model).filter(UFV_model.fecha >= '2015-01-01') 
    dfDepr = ufv.pd.read_sql(ufv.query2sql(DeprTable), cnx)
    dfUfv = ufv.pd.read_sql(ufv.query2sql(ufvData), cnx)
    HTMLDepr = dfDepr.to_html(index = False)
    HTMLUfv = dfUfv.to_html(index = False)
    union = HTMLUfv + HTMLDepr
    #return render_template("index.html")
    return union 
    #return [j.categoria for j in allData]
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Subir Archivo</title>
    <h1>Subir nuevo archivo</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    extension = filename.rsplit('.', 1)[1]
    if extension == "csv":
        df = ufv.pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return df.to_html()
        
    if extension == "xlsx" or extension == "xls":
        df = ufv.pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'Sheet1')
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return df.to_html()
      
        
    
            
    #open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return "filename uploaded successfully" + extension
                               

app.run(host=os.getenv('IP', '0.0.0.0'),debug=True, port=int(os.getenv('PORT', 8080)))