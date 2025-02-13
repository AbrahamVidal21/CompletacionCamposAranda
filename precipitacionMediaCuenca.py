import pandas as pd
import numpy as np

import os
ruta = os.path.join(os.path.dirname(__file__), "datos_completados_campos_aranda.csv")

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
    "7177": 0.0712,
    "7195": 329.59,
    "27042": 20.18,
    "27070": 93.38,
}

# 📌 Cálculo de la lluvia promedio según Campos-Aranda (con ajuste de estaciones y áreas)
def lluvia_promedio_campos_aranda(df, areas):
    resultados = []
    for _, row in df.iterrows():
        year = row["AÑO"]
        total_prec_area = 0
        total_area = 0
        for estacion, area in areas.items():
            if estacion in row and not pd.isna(row[estacion]):
                if row[estacion] >= 0:  # ✅ Ajuste: solo valores válidos
                    total_prec_area += row[estacion] * area
                    total_area += area
        promedio = total_prec_area / total_area if total_area > 0 else np.nan
        resultados.append([year, promedio])
    return pd.DataFrame(resultados, columns=["AÑO", "Precipitacion (mm)"])

# 📌 Generar el DataFrame de resultados
resultados_df = lluvia_promedio_campos_aranda(df, areas_thiessen)

# 📌 Guardar el archivo
resultados_df.to_csv("precipitacion_media_ponderada.csv", index=False)
print("✅ Cálculo completado con el método de Campos-Aranda.")
