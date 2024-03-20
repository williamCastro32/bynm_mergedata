# En este scrip iran todas las funciones para simplificar el archivo .ipynb
import pandas as pd
import re
import numpy as np


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
        return 'Revisar caso # vehiculo'
    elif pd.notna(row['Número de Vehículo']) and pd.isna(row['Número de secuencia de carro']):
        return 'Se reemplaza por el del k2 por nan'
    elif row['Número de Vehículo'] != row['Número de secuencia de carro']:
        return 'Se reemplaza por el del k2 # diferente'
    else: 
        return 'Numero ok'

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
        return row['Número de secuencia de carro']
    elif pd.notna(row['Número de Vehículo']) and pd.isna(row['Número de secuencia de carro']):
        return row['Número de Vehículo']
    elif row['Número de Vehículo'] != row['Número de secuencia de carro']:
        return row['Número de Vehículo']
    else:
        return row['Número de secuencia de carro']
    
# Funcion replica de la funcion de Excel para el calculo de incumpliminetos, pero la siguiente funcion la anula, revisar si es necesaria
def col_calificaciones_funtion(row, df):
    """
    Calcula el valor del incumplimiento según las condiciones especificadas.

    Parámetros:
    row (pandas.Series): Una fila del DataFrame que contiene los datos de la bitácora.
    df (pandas.DataFrame): DataFrame que contiene los datos de la bitácora.

    Retorna:
    int or float or np.nan: El valor del incumplimiento calculado según las condiciones.
    """
    
    # Obtener el índice de la fila actual
    index = row.name
    
    # Calcular el índice de la fila siguiente
    next_index = index + 1
    next_index_next = index + 2
    
    # Obtener la fila siguiente si el índice es válido, de lo contrario, establecerla como None
    next_row = df.iloc[next_index] if next_index < len(df) else None
    next_row_next = df.iloc[next_index_next] if next_index_next < len(df) else None

    
    if row['Tipo Kilómetros'] == "Kms en Servicio" and pd.isna(row['Número de secuencia de carro']):
        if row['Tipo de viaje corto_x'] == "Viaje comercial":
            return 2
        elif row['Tipo de viaje corto_x'] in ["Viaje de punto operacional", "Viaje de posicionamiento"]:
            if next_row is not None and pd.isna(next_row['Número de secuencia de carro']):
                if (next_row['Incumplidos_y'] == 2) and (row['Largo_y'] in [0, 1]):
                    return 1
                elif (row['Largo_y'] not in [0, 1]) or (next_row['Largo_y']  in [0, 1]):
                    if pd.notna(next_row_next['Incumplidos_y']):
                        return next_row_next['Incumplidos_y'] 
                    else:
                        return 2
                else:
                    return next_row['Incumplidos_y']
            else:
                if row is not None and row['Largo_y'] in [0, 1]:
                    return 1
                else:
                    return 2
        else:
            return np.nan
    elif (row['Número de secuencia de carro'] in ["CAMBIO", "CANCELADA"]) and row['Tipo Kilómetros'] == "Kms en Vacio":
        return 0
    else:
        return np.nan

def col_calificaciones(row, df):
    """
    Calcula el valor del incumplimiento según las condiciones especificadas.

    Parámetros:
    row (pandas.Series): Una fila del DataFrame que contiene los datos de la bitácora.
    df (pandas.DataFrame): DataFrame que contiene los datos de la bitácora.

    Retorna:
    int or float or np.nan: El valor del incumplimiento calculado según las condiciones.
    """
   
    if pd.isna(row['Incumplidos_x']) and pd.notna(row['Incumplidos_y']):
        return np.nan
    elif row['Incumplidos_x'] in [2,3] and row['CALIFICACION'] == 1:
        return row['CALIFICACION']
    elif row['Incumplidos_x'] == 3:
        return row['Incumplidos_x']
    elif row['Incumplidos_x'] in [0,1,3] and row['Incumplidos_y']== 2:
        return row['Incumplidos_x'] 
    elif row['Incumplidos_x']== 2 and  row['Incumplidos_y']== 2:
        return row['Incumplidos_x'] 
    else:
        np.nan




