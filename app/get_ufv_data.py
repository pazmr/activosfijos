import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def get_ufv_data(desde, hasta):
    
    if desde >= hasta or not isinstance(desde, datetime.datetime):
        return False
    try:
        url = 'https://www.bcb.gob.bo/librerias/indicadores/ufv/gestion.php?sdd='+str(desde.day)+'&smm='+str(desde.month)+'&saa='+str(desde.year)+'&Button=++Ver++&reporte_pdf=1*1*2015**1*1*2015*&edd='+str(hasta.day)+'&emm='+str(hasta.month)+'&eaa='+str(hasta.year)+'&qlist=1'
        
        functions = [int, str, float]
        
        response = requests.get(url)
        # Getting the text of the page from the response data       
        page = BeautifulSoup(response.text)
        table = page.find("table", { "class" : "tablaborde" })
        
        allrows = table.findAll('tr')
        rawColumnsName = allrows[0]
        
        allrows = allrows[1:]
        data = []
        for row in allrows:
            allcols = row.findAll('td')
            tempList = []
            counter = 0
            for col in allcols:
                val = functions[counter](col.text.strip(' \t\n\r').replace(",","."))
                tempList.append(val)
                counter += 1
            data.append(tempList) 
        allColsName = rawColumnsName.findAll('td')
        columnsName = []
        for name in allColsName:
            
            val2 = str(name.text.strip(' \t\n\r'))
            columnsName.append(val2)
        df = pd.DataFrame(data, columns=columnsName)
        df = df.set_index('Nro.')
        df= df.replace(regex={'Fecha': {r'\b de\b': '', r'\bEnero\b': '1', r'\bFebrero\b': '2', r'\bMarzo\b': '3'\
                                            , r'\bAbril\b': '4', r'\bMayo\b': '5', r'\bJunio\b': '6', r'\bJulio\b': '7', r'\bAgosto\b': '8'\
                                            , r'\bSeptiembre\b': '9', r'\bOctubre\b': '10', r'\bNoviembre\b': '11', r'\bDiciembre\b': '12', r'\b \b': '/'}})
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
        return df
    except:
        return False


def query2sql(query):
    """convert query object into non-prepared sql string in SQLAlchemy and psycopg2"""
    compiler = query.statement.compile()
    params = compiler.params
    prepared_sql = compiler.string  # or str(compiler)
    psycopg2_cursor = query.session.connection().connection.cursor()
    sql = psycopg2_cursor.mogrify(prepared_sql, params)
    return sql    
def depreciacion_data():
    df = pd.read_csv('tabla_linea_recta.csv', sep=";")
    df['Coeficiente'] = df['Coeficiente']/100.0
    return df    

