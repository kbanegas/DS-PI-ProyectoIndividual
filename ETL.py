#Procesamiento
import pandas as pd
import numpy as np
import datetime as dt
import missingno as msno
 
#Visualización
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

import io
import glob

import nltk

# Esto sirve para configurar NLTK. La primera vez puede tardar un poco
nltk.download('punkt')
nltk.download('stopwords')

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Esta función calcula la distancia de Levenshtein entre dos cadenas de caracteres
        Si ratio_calc = True, la función computa la distancia de Levenshtein o similaridad entre dos cadenas de caracteres
        Para todas las 'i' y 'j', distance[i,j] contendrá la distancia de Levenshtein entre los primeros 'i' caracteres de 's'
        y el primer 'j' de 't'
        Fuente: https://www.datacamp.com/community/tutorials/fuzzy-string-python
    """
    import numpy as np
    # Initialize matrix of zeros
    s = str(s)
    t = str(t)
    rows = len(s)+1
    cols = len(t)+1
    if (rows == 1 | cols == 1):
        return 0
    col = 0
    row = 0
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "Las cadenas de caracteres están a {} ediciones de distancia".format(distance[row][col])

 #lectura y concatenacion de archivos del cliente en la carpeta Datasets   
df_Ucliente =[]
for csv in sorted(glob.glob('Datasets/Cli*.csv')):
    #print(csv)
    df= pd.read_csv(csv, sep=";", decimal=".",encoding="utf-8")
    df_Ucliente.append(df)
df_Cliente= pd.concat(df_Ucliente)
#df_Cliente.head()
#ordena por ID
df_Cliente.sort_values('ID', inplace= True)
#Elimina columna
df_Cliente.drop(['col10'], axis=1, inplace=True)
#Crea df de valores nulos en nombre e ID y los ordena por ID, concatenandolos
df0= df_Cliente[df_Cliente['ID'].isnull()]
df0.sort_values('ID', inplace= True)
df2= df_Cliente[df_Cliente['Nombre_y_Apellido'].isnull()]
df2.sort_values('ID', inplace= True)
df= pd.concat([df0,df2], axis=0)
#los lleva a un csv auxiliar antes de eliminarlos
df.to_csv("Datasets/AuxiliarClientes.csv")
#Rellena valores personales con Sin dato
df_Cliente.fillna({'Provincia': 'Sin dato'}, inplace=True)
df_Cliente.fillna({'Domicilio': 'Sin dato'}, inplace=True)
df_Cliente.fillna({'Telefono': 'Sin dato'}, inplace=True)
df_Cliente.fillna({'Edad': 0}, inplace=True)
#Remplaza coma por punto en valores de X y Y, elimina espacios en blanco
df_Cliente['X'] = df_Cliente['X'].str.replace(",", ".")#.astype(float)
df_Cliente['X'] = df_Cliente['X'].str.strip(" ")
df_Cliente['Y'] = df_Cliente['Y'].str.replace(",", ".")#.astype(float)
df_Cliente['Y'] = df_Cliente['Y'].str.strip(" ")
#obtengo dataframe valores nulos
dfn=df_Cliente[df_Cliente['Localidad'].isnull()]
dfn.sort_values('ID', inplace= True)
dfn1=df_Cliente[df_Cliente['X'].isnull()]
dfn1.sort_values('ID', inplace= True)
dfn2=df_Cliente[df_Cliente['Y'].isnull()]
dfn2.sort_values('ID', inplace= True)
df= pd.concat([dfn,dfn1,dfn2], axis=0)
#convertirlo en array
arrn = df.to_numpy()
#Variable de comparacion para normalizar 
path_csv4 = 'Datasets\Localidades.csv'
dfL5= pd.read_csv(path_csv4, sep=",", decimal=".") #, on_bad_lines='skip')
arr = dfL5.to_numpy()
lcentroide_lat=arr[0:,1:2]
lcentroide_lon=arr[0:,2:3]
llatitud=arrn[0:,8:]
llongitud=arrn[0:,7:8]
llongitudr=llongitud.flatten().astype(str)
llatitudr= llatitud.flatten().astype(str)
lcentroide_latr=lcentroide_lat.flatten().astype(str)
lcentroide_lonr= lcentroide_lon.flatten().astype(str)
lista1= list(llatitudr)
lista2= list(llongitudr)
lista3= list(lcentroide_latr)
lista4= list(lcentroide_lonr)
import pandas as pd
import Levenshtein as lev
from statistics import mode, multimode
def distancefinder(lista1, lista3):

    Lista_loc=[]
    Lista_pro=[]
    Rdistance=[]
    Rratio=[]
    
    for i  in range(len( lista1)):
        Str1=lista1[i]
        for j in range(len(lista3)):
            Str2=lista3[j]
            Distance = lev.distance(Str1.lower(),Str2.lower()),
            Ratio = lev.ratio(Str1.lower(),Str2.lower())
            if Ratio >= 0.50:    
                Rdistance.append(Distance)
                Rratio.append(Ratio)
                loc=arr[(j-1),11:12]
                locr=loc.astype(str)
                valor1=str(locr)
                valor11=valor1.replace("['"," ")
                valor12=valor11.replace("']"," ")
                valor=valor12.strip()
                Lista_loc.append(valor)
                #Para Provincia
                pro=arr[(j-1),13:]
                pror=pro.astype(str)
                valor2=str(pror)
                valor21=valor2.replace("['"," ")
                valor22=valor21.replace("']"," ")
                valor0=valor22.strip()
                Lista_pro.append(valor0)
        Moda= mode(Lista_loc) 
                
        return Moda#, Lista_loc#, Lista_pro
Moda1=distancefinder(lista1, lista3)
if Moda1 != " ":
    df_Cliente.fillna({'Localidad': Moda1}, inplace=True)
import pandas as pd
import Levenshtein as lev
from statistics import mode, multimode, median

def distancefinder1(lista1, lista3):

    Lista_loc=[]
    Lista_pro=[]
    Rdistance=[]
    Rratio=[]
    lstr1=[]
    lstr2=[]
    
    for i  in range(len( lista1)):
        Str1=lista1[i]
        for j in range(len(lista3)):
            Str2=lista3[j]
            Distance = lev.distance(Str1.lower(),Str2.lower()),
            Ratio = lev.ratio(Str1.lower(),Str2.lower())
            if Ratio >= 0.80:    
                Rdistance.append(Distance)
                Rratio.append(Ratio)
                loc=arr[(j-1),11:12]
                locr=loc.astype(str)
                valor1=str(locr)
                valor11=valor1.replace("['"," ")
                valor12=valor11.replace("']"," ")
                valor=valor12.strip()
                Lista_loc.append(valor)
                #Para Provincia
                pro=arr[(j-1),13:]
                pror=pro.astype(str)
                valor2=str(pror)
                valor21=valor2.replace("['"," ")
                valor22=valor21.replace("']"," ")
                valor0=valor22.strip()
                Lista_pro.append(valor0)
                lstr1.append(Str1)
                lstr2.append(Str2)
        Media1=median(lstr1)
        Media2=median(lstr2)
        Moda= mode(Lista_loc)
        return Media1#Moda, Lista_loc#, Lista_pro
Media1=distancefinder1(lista1, lista3)
if Media1 != " ":
    df_Cliente.fillna({'Y': Media1}, inplace=True)
#Sustituir media de longitud en X para mantener congruencia en la tabla.
import pandas as pd
import Levenshtein as lev
from statistics import mode, multimode, median
def distancefinder1(lista2, lista4):

    Lista_loc=[]
    Lista_pro=[]
    Rdistance=[]
    Rratio=[]
    lstr1=[]
    lstr2=[]
    
    for i  in range(len( lista2)):
        Str1=lista2[i]
        for j in range(len(lista4)):
            Str2=lista4[j]
            Distance = lev.distance(Str1.lower(),Str2.lower()),
            Ratio = lev.ratio(Str1.lower(),Str2.lower())
            if Ratio >= 0.80:    
                Rdistance.append(Distance)
                Rratio.append(Ratio)
                loc=arr[(j-1),11:12]
                locr=loc.astype(str)
                valor1=str(locr)
                valor11=valor1.replace("['"," ")
                valor12=valor11.replace("']"," ")
                valor=valor12.strip()
                Lista_loc.append(valor)
                #Para Provincia
                pro=arr[(j-1),13:]
                pror=pro.astype(str)
                valor2=str(pror)
                valor21=valor2.replace("['"," ")
                valor22=valor21.replace("']"," ")
                valor0=valor22.strip()
                Lista_pro.append(valor0)
                lstr1.append(Str1)
                lstr2.append(Str2)
        Media1=median(lstr1)
        Media2=median(lstr2)
        Moda= mode(Lista_loc)
        return Media2#Moda, Lista_loc#, Lista_pro
Media2=distancefinder1(lista2, lista4)
if Media2 != " ":
    df_Cliente.fillna({'X': Media2}, inplace=True)
df_Cliente.dropna(axis=0, inplace=True)
#Eliminar los registros nulos en nombres del cliente
df_Cliente.dropna(inplace=True)
#Tranformacion de tipo de dato formatos nombres de colummas
pd.to_numeric(df_Cliente['Edad'], downcast='integer')
df_Cliente.columns = ['IdCliente', 'Provincia', 'NombreApellido', 'Domicilio', 'Telefono', 'Edad', 'Localidad','Longitud','Latitud']
df_Cliente['NombreApellido']=df_Cliente['NombreApellido'].str.title()
df_Cliente['Provincia']=df_Cliente['Provincia'].str.title()
df_Cliente['Localidad']=df_Cliente['Localidad'].str.title()
df_Cliente['Domicilio']=df_Cliente['Domicilio'].str.title()
#Modificacion y formato de datos tabla localidades
dfL5.columns = ['Categoria', 'Centroide_Lat', 'Centroide_Lon', 'Departamento_Id ', 'Departamento_Nombre', 'Fuente ', 'IdLocalidad','Localidad_Censal_Id','Localidad_Censal_Nombre', 'Municipio_id','Municipio_Nombre','Localidad_Nombre','Provincia_Id','Provincia_Nombre']
dfL5['Categoria']=dfL5['Categoria'].str.title()
dfL5['Departamento_Nombre']=dfL5['Departamento_Nombre'].str.title()
dfL5['Localidad_Censal_Nombre']=dfL5['Localidad_Censal_Nombre'].str.title()
dfL5['Municipio_Nombre']=dfL5['Municipio_Nombre'].str.title()
dfL5['Localidad_Nombre']=dfL5['Localidad_Nombre'].str.title()
dfL5['Provincia_Nombre']=dfL5['Provincia_Nombre'].str.title()
#Normalizacion nombres de acuerdo a la tabla localidad.
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
localidad = dfL5.Localidad_Nombre.value_counts().index
local_clientes_unique = df_Cliente.Localidad.unique()
normalized = []
def get_matches(query,choices):
    for i in query:
        tuple = process.extractOne(i,choices)
        normalized.append(tuple[0])
    return normalized
local_clientes_correg = get_matches(local_clientes_unique, localidad)
mydict = {local_clientes_unique[i]:local_clientes_correg[i] for i in range(0,367)}
df_Cliente = df_Cliente.convert_dtypes()
df_Cliente["LocalidadN"] = df_Cliente["Localidad"].map(mydict)
#borro localidad no nomalizada y renombro los campos
df_Cliente.drop(['Localidad'], axis=1, inplace=True)
df_Cliente.columns = ['IdCliente', 'Provincia', 'NombreApellido', 'Domicilio', 'Telefono', 'Edad','Longitud','Latitud', 'Localidad']
dfL5.fillna({'Municipio_Nombre': 'Sin dato'}, inplace=True)
dfL5.fillna({'Municipio_id': 'Sin dato'}, inplace=True)
df_Cliente.to_csv("Datasets/NormalizacionCliente.csv")
import re
letters_only = re.sub("[^a-zA-Z]",  
                          " ",          
                          str(dfL5['Departamento_Nombre']))
letters_only = re.sub("[^a-zA-Z]",  # Busca las que no sean letras
                          " ",          # Remplaza con espacios
                          str(dfL5['Municipio_Nombre']))
#Elimina los espacios antes y despues
dfL5['Municipio_Nombre'] = dfL5['Municipio_Nombre'].str.strip(" ")
dfL5['Municipio_Nombre'] = dfL5['Departamento_Nombre'].str.strip(" ")
path_csv2= r'Datasets\Compra.csv'
dfC3= pd.read_csv(path_csv2, sep=",",decimal="."  )
dfC3.drop(['Fecha_Año','Fecha_Mes','Fecha_Periodo'], axis=1, inplace=True)
df=dfC3.groupby(by = ['IdProducto','IdProveedor']).Precio.median()
valor=df.median()
dfC3.fillna({'Precio': valor}, inplace=True)
dfC3['Fecha'] = pd.to_datetime(dfC3['Fecha'])
df = dfC3[(dfC3['Precio'] > 2690) & (dfC3['Precio'] < 30000000)]
df1 = dfC3[(dfC3['Cantidad'] > 24)]
df.to_csv("Datasets/OurliersPrecioCompras.csv")
df1.to_csv("Datasets/OurliersCantidadCompras.csv")
dfC3= dfC3.drop(dfC3[dfC3['Precio']>2690.0 ].index)
dfC3= dfC3.drop(dfC3[dfC3['Cantidad']>24].index)
dfL5.to_csv("Datasets/NormalizacionLocalidad.csv")
dfC3.to_csv("Datasets/NormalizacionCompras.csv")
#normalizción Ventas
df_UVenta =[]
for csv in sorted(glob.glob('Datasets/Vent*.csv')):
    print(csv)
    df= pd.read_csv(csv, sep=",")
    df_UVenta.append(df)
df_Venta= pd.concat(df_UVenta)
df=df_Venta.groupby(by = ['IdProducto']).Precio.median()
valor=df.median()
valor
df_Venta.fillna({'Precio': valor}, inplace=True)
df = df_Venta[(df_Venta['Precio'] > 3764.0) & (df_Venta['Precio'] < 50000000.0)]
df1 = df_Venta[(df_Venta['Cantidad'] > 3)]
df.to_csv("Datasets/OurliersPrecioVenta.csv")
df1.to_csv("Datasets/OurliersCantidadVenta.csv")
df_Venta= df_Venta.drop(df_Venta[df_Venta['Precio']>3764.0 ].index)
df_Venta= df_Venta.drop(df_Venta[df_Venta['Cantidad']>3].index)
df_Venta['Fecha'] = pd.to_datetime(df_Venta['Fecha'])
df_Venta['Fecha_Entrega'] = pd.to_datetime(df_Venta['Fecha_Entrega'])
df_Venta.to_csv("Datasets/NormalizacionVentas.csv")
#normalización gasto
path_csv3 = r'Datasets\Gasto.csv'
dfG4= pd.read_csv(path_csv3, sep=",")
dfG4['Fecha'] = pd.to_datetime(dfG4['Fecha'])
dfG4.to_csv("Datasets/NormalizacionGasto.csv")
#Normalizacion Proveedores
path_csv5 = r'Datasets\Proveedores.csv'
dfP5= pd.read_csv(path_csv5, sep=",", encoding= 'Latin-1')
dfP5.columns = ['IdProveedor', 'Nombre', 'Domicilio', 'Ciudad', 'Provincia', 'Pais','Departamento']
dfP5['Nombre']=dfP5['Nombre'].str.title()
dfP5['Domicilio']=dfP5['Domicilio'].str.title()
dfP5['Ciudad']=dfP5['Ciudad'].str.title()
dfP5['Provincia']=dfP5['Provincia'].str.title()
dfP5['Pais']=dfP5['Pais'].str.title()
dfP5['Departamento']=dfP5['Departamento'].str.title()
localidad = dfL5.Provincia_Nombre.value_counts().index
local_clientes_unique = dfP5.Provincia.unique()
normalized = []
def get_matches(query,choices):
    for i in query:
        tuple = process.extractOne(i,choices)
        normalized.append(tuple[0])
    return normalized
local_clientes_correg = get_matches(local_clientes_unique, localidad)
mydict = {local_clientes_unique[i]:local_clientes_correg[i] for i in range(0,7)}
dfP5= dfP5.convert_dtypes()
dfP5["ProvinciaN"] =dfP5["Provincia"].map(mydict)
dfP5.drop(['Provincia'], axis=1, inplace=True)
localidad = dfL5.Departamento_Nombre.value_counts().index
local_clientes_unique = dfP5.Departamento.unique()
normalized = []
def get_matches(query,choices):
    for i in query:
        tuple = process.extractOne(i,choices)
        normalized.append(tuple[0])
    return normalized
local_clientes_correg = get_matches(local_clientes_unique, localidad)
mydict = {local_clientes_unique[i]:local_clientes_correg[i] for i in range(0,7)}
dfP5= dfP5.convert_dtypes()
dfP5["DepartametoN"] =dfP5["Departamento"].map(mydict)
dfP5.drop(['Departamento'], axis=1, inplace=True)
dfP5.columns = ['IdProveedor', 'Nombre', 'Domicilio', 'Ciudad','Pais','Provincia','Departamento']
dfP5.fillna({'Nombre': 'Sin dato'}, inplace=True)
dfP5.to_csv("Datasets/NormalizacionProveedores.csv")
#Normalización Sucursal
path_csv6 = r'Datasets\Sucursales.csv'
dfS6= pd.read_csv(path_csv6, sep=";") 
dfS6['Sucursal']=dfS6['Sucursal'].str.title()
dfS6['Direccion']=dfS6['Direccion'].str.title()
dfS6['Localidad']=dfS6['Localidad'].str.title()
dfS6['Provincia']=dfS6['Provincia'].str.title()
letters_only = re.sub("[^a-zA-Z]",  
                          " ",          
                          str(dfS6['Localidad']))
letters_only = re.sub("[^a-zA-Z]",  # Busca las que no sean letras
                          " ",          # Remplaza con espacios
                          str(dfS6['Provincia']))
#Elimina los espacios antes y despues
dfS6['Localidad'] = dfS6['Localidad'].str.strip(" ")
dfS6['Provincia'] = dfS6['Provincia'].str.strip(" ")
localidad = dfL5.Localidad_Nombre.value_counts().index
local_clientes_unique =dfS6.Localidad.unique()
normalized = []
def get_matches(query,choices):
    for i in query:
        tuple = process.extractOne(i,choices)
        normalized.append(tuple[0])
    return normalized
local_clientes_correg = get_matches(local_clientes_unique, localidad)
mydict = {local_clientes_unique[i]:local_clientes_correg[i] for i in range(0,26)}
dfS6= dfS6.convert_dtypes()
dfS6["LocalidadN"] =dfS6["Localidad"].map(mydict)
dfS6.drop(['Localidad'], axis=1, inplace=True)
localidad = dfL5.Provincia_Nombre.value_counts().index
local_clientes_unique =dfS6.Provincia.unique()
normalized = []
def get_matches(query,choices):
    for i in query:
        tuple = process.extractOne(i,choices)
        normalized.append(tuple[0])
    return normalized
local_clientes_correg = get_matches(local_clientes_unique, localidad)
mydict = {local_clientes_unique[i]:local_clientes_correg[i] for i in range(0,17)}
dfS6= dfS6.convert_dtypes()
dfS6["ProvinciaN"] =dfS6["Provincia"].map(mydict)
dfS6.drop(['Provincia'], axis=1, inplace=True)
dfS6.columns = ['IdSucursal', 'Sucursal', 'Direccion', 'Latitud','Longitud','Localidad','Provincia']
dfS6['Latitud'] = dfS6['Latitud'].str.replace(",", ".")#.astype(float)
dfS6['Latitud'] = dfS6['Latitud'].str.strip(" ")
dfS6['Longitud'] = dfS6['Longitud'].str.replace(",", ".")#.astype(float)
dfS6['Longitud'] = dfS6['Longitud'].str.strip(" ")
dfS6.to_csv("Datasets/NormalizacionSucursal.csv")
import mysql.connector
conexion1=mysql.connector.connect(host="localhost", user="root", passwd="")#, database="bdproyectofinal")
cursor1=conexion1.cursor()
cursor1.execute("CREATE DATABASE IF NOT EXISTS bdproyectofinal;")
cursor1.execute("USE bdproyectofinal;")
cursor1.execute("USE bdproyectofinal;")
TablaCliente="CREATE TABLE IF NOT EXISTS cliente  (IdCliente INT, NombreApellido VARCHAR(150), Domicilio VARCHAR(250), Telefono VARCHAR(50), Edad INT, RangoEtario VARCHAR (80), IdProvincia INT, IdLocalidad INT, Latitud DOUBLE, Longitud DOUBLE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;"
cursor1.execute(TablaCliente)
conexion1.close()    