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
    

# Esta funcion marcara en una columna los cambios que se hagan a la columna Largo_y
def rev_amarillos_rosa_text(row):
    """
    Esta función se aplica a cada fila del DataFrame para evaluar si se cumplen ciertas condiciones
    basadas en las columnas 'Número de Vehículo', 'Descripción Novedad_x' y 'PARADAS PLANEADAS'.
    Según las condiciones cumplidas, devuelve un texto descriptivo correspondiente.

    Parámetros:
    row (pandas.Series): Una fila del DataFrame que contiene los datos de la bitácora.

    Retorna:
    str: Un texto descriptivo basado en las condiciones especificadas.

    Detalles de la lógica:
    - Si 'Número de Vehículo' no es NaN y 'Descripción Novedad_x' no es NaN, se evalúan las condiciones.
    - Si 'Descripción Novedad_x' contiene al menos uno de los elementos de la lista 'amarillos',
      se procede a realizar búsquedas específicas en 'Descripción Novedad_x'.
    - Se utilizan expresiones regulares para buscar patrones relacionados con 'INGRESO', 'SALIDAS' y 'CANCELACION'
      seguidos del número de parada en 'Descripción Novedad_x'.
    - Dependiendo de los resultados de las búsquedas y de los valores en 'PARADAS PLANEADAS', se devuelve un texto
      descriptivo que indica cómo se debe manejar el valor de 'Largo' en esa fila.

    """
    if pd.notna(row['Número de Vehículo_x']):
        if pd.notna(row['Descripción Novedad_x']): 
            # Casos rosa
            if isinstance(row['Descripción Novedad_x'], str) and 'Nro. Caso Desvio:' in row['Descripción Novedad_x']:
                    if row['Largo_y'] == row['Kilometros Programados Plan']:
                        return 'Se cambia Largo por el k2_if_8'
                    elif row['Largo_y'] != row['Kilometros Programados Plan']:
                        if row['Largo_y'] != row['Kilometros Programados-Desvios']:
                            if row['Largo_y'] < row['Largo_x']:
                                return 'Se cambia Largo por el k2__9'
                        else:
                            'Se mantiene largo_if_10'
            # Casos Amarillos                
            elif isinstance(amarillos, list) and any(isinstance(amarillo, str) and amarillo in row['Descripción Novedad_x'] for amarillo in amarillos):
                ingreso_match = re.search(r'INGRESO.*?Nro\. Parada:\s*(\d{1,3})', row['Descripción Novedad_x'])
                salida_match = re.search(r'SALIDAS.*?Nro\. Parada:\s*(\d{1,3})', row['Descripción Novedad_x'])
                cancelacion_match = re.search(r'CANCELACION.*?Nro\. Parada:\s*(\d{1,3})', row['Descripción Novedad_x'])       
                if ingreso_match and int(ingreso_match.group(1)) == 1 and int(row['PARADAS PLANEADAS']) != 1:
                    return 'Se cambia Largo por el k2_if1'
                elif ingreso_match and int(ingreso_match.group(1)) != 1:
                    return 'Se cambia Largo por el k2_if2'
                elif salida_match and int(salida_match.group(1)) != int(row['PARADAS PLANEADAS']):
                    return 'Se cambia Largo por el k2_if3'
                elif salida_match and int(salida_match.group(1)) == int(row['PARADAS PLANEADAS']):
                    return 'Se mantiene largo_if4'
                elif cancelacion_match and int(cancelacion_match.group(1)) != int(row['PARADAS PLANEADAS']):
                    return 'Se cambia Largo por el k2_if5'
                elif cancelacion_match and int(cancelacion_match.group(1)) == int(row['PARADAS PLANEADAS']):
                    return 'Se mantiene largo_if_6'
                else:
                    return 'Se mantiene largo_if7'                       
            else:
                return 'Se mantiene largo_if_11'
        else:
            return 'Se mantiene largo_if_12' 
    else:
        if pd.notna(row['Desde_y']):
            return  'casos verde'


