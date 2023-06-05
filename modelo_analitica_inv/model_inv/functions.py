import os
import pandas as pd

from django.conf import settings

from .models import InformacionCliente

from sqlalchemy import create_engine

def cargue_bd():
    '''
    Función para almacenamiento en modelo de BD,
    información de un csv.

    inputs:
    -------
    None

    outputs: 
    -------
    Bool
    '''
    file_name = 'model_output.csv'
    path = os.path.join(settings.BASE_DIR, 'model', file_name)
    with open(path) as f:
        df = pd.read_csv(path)

    engine = create_engine('sqlite:///db.sqlite3')

    df.to_sql(InformacionCliente._meta.db_table, if_exists='replace',con=engine, index=False)
    return True

def consulta_bd(doc):
    '''
    Función para consulta de output modelo. 

    inputs:
    -------
    doc: número documento cliente

    outputs: 
    -------
    info: lista de información del cliente
    '''
    doc = int(doc)
    info = InformacionCliente.objects.filter(ID=doc)
    info = info.values('ID', 'Year_Birth', 'Education', 'Marital_Status', 'Income', 'Kidhome',
       'Teenhome', 'Recency', 'MntWines', 'MntFruits', 'MntMeatProducts',
       'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
       'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases',
       'NumStorePurchases', 'NumWebVisitsMonth', 'Year_Enrolled', 'Age',
       'cluster')
    info = list(info)
    return info

def consulta_tipo_cliente(cluster):
    '''
    Esta función está creada bajo supuestos, para efectos de este 
    mínimo producto viable. La información aquí contenida 
    debe ser validada y estudiada a profundidad para asegurar que 
    se está tratando de forma correcta a cada uno de los clientes.
    Además, requiere de un estudio de mayor profundidad sobre las
    características de los clúster.
    '''
    descripcion_cliente= ''
    if cluster == '0':
        descripcion_cliente= "Este tipo de cliente es tipo 0. La segmentación de estos clientes sugiere que se debe comenzar por un lenguaje poco técnico, donde encuentren cercanía y acompañamiento constante. Preferiblmente, motivarlo a conocer más sobre el mundo del mercado de capitales, comaprtile noticias como (www.noticiaimportante.com.co/mercado-capitales) donde podrá conocer de primera manos términos como 'tesoros', 'tasas de interés'..."
    elif cluster == '1':
        descripcion_cliente= "Este es un cliente tipo 1. Además de ser parte del segmento X, es un cliente que posee conocimiento del mercado. Por su historial educativo y movimientos dentro del portafolio recurrentes se infiere que se interese por las llamadas. Se sugiere utilizar un lenguaje técnico con esta perosna, ya que demuestra bastante interés en sus inversiones basados en los datos del último mes, es posible que sea reactivo hacia la última noticia de la FED..."
    elif cluster == '2':
        descripcion_cliente= "Este es un cliente tipo 2. La caracterítica principal de este cliente es que posee mayor conocimiento de herramientas virtuales, su preferencia se asocia al uso de la app y visitas significativamente bajas a sucursales y/o llamadas a su gerente comercial[...]. Para este cliente se recomiendan piezas comerciales vía correo electrónico. Se recomienda que al momento de entablar la conversación con este cliente se puntualice sobre: A,B C..."
    elif cluster == '3':
        descripcion_cliente= "Este tipo de cliente se clasifica como de tipo 3. Esto significa que este cliente desearía tener mayor libertad en las decisiones que toma, se recomiendan estrategia de acercamiento menos directas como piezas comerciales pequeñas en redes sociales[...]. En vista al comportamiento de sus canales en el último mes, sería conveniente  sostener la relación comercial por vía telefónica..."
    elif cluster == '4':
        descripcion_cliente= "Este tipo de cliente se clasifica como de tipo 4, tiene una tendencia significativa a invertir en el producto 3. Debido a su nivel de ingresos, es posible que este cliente disponga de una cantidad pequeña de su portafolio que podría ser invertida en productos del tipo X. Adicionalmente, por la disposición de tendencia de estos clientes, es posible que sea necesaria una reunión presencial y/o telefónica, ya que prieferen sentirse seguros y acompañados en la toma de decisiones..."

    return descripcion_cliente


