# En este scrip iran todas las funciones para simplificar el archivo .ipynb
import pandas as pd
import re
import numpy as np
import datetime



def extraer_hora_regex(desde):
    """
    Esta funcion trata las columnas desde y hasta para verificar que las fechas esten iguales.
    Extrae la hora en formato hh:mm:ss de una cadena utilizando expresiones regulares.

    Parameters:
    desde (str): Cadena que contiene la hora en formato hh:mm:ss.

    Returns:
    str or None: La hora extraída en formato hh:mm:ss si se encuentra en la cadena, None si no se encuentra.
    """
    # Expresión regular para encontrar el patrón de hora (hh:mm:ss)
    patron_hora = r'(\d{2}):(\d{2}):(\d{2})'
    # Buscar el patrón en la cadena
    resultado = re.search(patron_hora, str(desde))
    # Si se encontró el patrón
    if resultado:
        # Extraer la hora, minutos y segundos encontrados
        hora = int(resultado.group(1))
        minutos = int(resultado.group(2))
        segundos = int(resultado.group(3))
        # Si la hora es 0, cambiarla a 24
        if hora == 0:
            hora = 24
        # Si la hora es 1, cambiarla a 25
        elif hora == 1:
            hora = 25
        # Devolver la hora modificada en formato hh:mm:ss
        return f"{hora:02d}:{minutos:02d}:{segundos:02d}"
    # Si no se encontró el patrón, devolver None
    return None

def vehiculos_xy_texto(row):
    """
    Asigna un texto descriptivo según las condiciones especificadas sobre los números de vehículo y secuencia de carro.

    Parámetros:
    row (pandas.Series): Una fila del DataFrame que contiene los datos de la bitácora.

    Retorna:
    str: Un texto descriptivo que indica el resultado de las comparaciones entre los números de vehículo y secuencia de carro.

    Detalles de la lógica:
    - Si el número de vehículo es nulo y el número de secuencia de carro no lo es, devuelve 'Revisar caso'.
    - Si el número de vehículo no es nulo y el número de secuencia de carro sí lo es, devuelve 'Se reemplaza por el del k2 por nan'.
    - Si el número de vehículo es diferente del número de secuencia de carro, devuelve 'Se reemplaza por el del k2 # diferente'.
    - En cualquier otro caso, devuelve 'Numero ok'.
    """
    if pd.isna(row['Número de Vehículo']) and pd.notna(row['Número de secuencia de carro']): 
        return 'x=nan vihiculo_y no Nan'
    elif pd.notna(row['Número de Vehículo']) and pd.isna(row['Número de secuencia de carro']):
        return 'vehiculo_y Nan repl k2'
    elif row['Número de Vehículo'] != row['Número de secuencia de carro']:
        return 'vehiculo_x != vehiculo_y'
    elif row['Número de Vehículo'] == row['Número de secuencia de carro']:
        return 'Numero ok'
    else: 
        return 'revisar'
    
    
def vehiculo_xy(row):
    """
    Retorna el valor adecuado para el número de vehículo según las condiciones especificadas respecto al número de secuencia de carro.

    Parámetros:
    row (pandas.Series): Una fila del DataFrame que contiene los datos de la bitácora.

    Retorna:
    int or float or np.nan: El valor del número de vehículo seleccionado según las condiciones.

    Detalles de la lógica:
    - Si el número de vehículo es nulo y el número de secuencia de carro no lo es, devuelve el número de secuencia de carro.
    - Si el número de vehículo no es nulo y el número de secuencia de carro sí lo es, devuelve el número de vehículo.
    - Si el número de vehículo es diferente del número de secuencia de carro, devuelve el número de vehículo.
    - En cualquier otro caso, devuelve el mismo valor de número de secuencia de carro.
    """
    
    if pd.isna(row['Número de Vehículo']) and pd.notna(row['Número de secuencia de carro']): 
        return  row['Número de secuencia de carro']
    elif pd.notna(row['Número de Vehículo']) and pd.isna(row['Número de secuencia de carro']):
        return row['Número de Vehículo']
    elif row['Número de Vehículo'] != row['Número de secuencia de carro']:
        return row['Número de Vehículo']
    elif row['Número de Vehículo'] == row['Número de secuencia de carro']:
        return row['Número de secuencia de carro']
    else:
        return 'No condicionado'
    

