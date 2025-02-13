import pandas as pd
import numpy as np

import os
ruta = os.path.join(os.path.dirname(__file__), "datos_completados.csv")

# Intenta leer con encoding='latin1'
try:
    df = pd.read_csv(ruta, encoding='latin1')
except UnicodeDecodeError:
    df = pd.read_csv(ruta, encoding='ISO-8859-1')

print(df.head())  # Muestra las primeras filas para verificar la lectura correcta

# Definir las áreas de los polígonos de Thiessen (en km²) para cada estación
areas_thiessen = {
    "7160": 0,
    "7169": 0,
    "7177": 0.71,
    "7195": 3295.9295,
    "27042": 201.38445,
    "27070": 923.82,
}

# Calcular la precipitación media ponderada por año
precipitacion_media = []

for index, row in df.iterrows():
    if row["AÑO"] == "AÑO":  # Saltar la fila de encabezados
        continue
    
    year = row["AÑO"]
    total_prec = 0
    total_area = 0
    
    for estacion, area in areas_thiessen.items():
        if estacion in df.columns:
            total_prec += row[estacion] * area
            #print( total_prec )
            total_area += area
            print( total_area )
    
    promedio_ponderado = total_prec / total_area if total_area > 0 else 0
    precipitacion_media.append([year, promedio_ponderado])

# Crear un DataFrame con los resultados
resultados_df = pd.DataFrame(precipitacion_media, columns=["AÑO", "Precipitación Media Ponderada (mm)"])

# Guardar los resultados en un nuevo archivo
resultados_df.to_csv("precipitacion_media_ponderada.csv", index=False)
print("Cálculo completado. Archivo generado: precipitacion_media_ponderada.csv")
