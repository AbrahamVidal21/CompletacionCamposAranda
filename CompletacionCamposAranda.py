import pandas as pd
import numpy as np

# 📌 Cargar los datos desde el CSV
ruta = "datos.csv"
try:
    df = pd.read_csv(ruta, encoding='latin1')
except UnicodeDecodeError:
    df = pd.read_csv(ruta, encoding='ISO-8859-1')

# 📌 Convertir valores 'ND' a NaN y asegurar tipo numérico
df.replace("ND", np.nan, inplace=True)
df = df.astype(float)

# 📌 Aplicar el método de Campos-Aranda para la completación
def campos_aranda(df):
    for estacion in df.columns:
        if df[estacion].isna().sum() > 0:
            print(f"Procesando estación: {estacion} con método Campos-Aranda")
            estaciones_ref = df.drop(columns=[estacion]).dropna(axis=1, how='any')
            if estaciones_ref.empty:
                print(f"No hay estaciones de referencia para {estacion}")
                continue
            
            # Calcular promedios de cada estación
            promedio_estacion = df[estacion].mean(skipna=True)
            promedio_ref = estaciones_ref.mean()

            for i, valor in df[estacion].items():
                if pd.isna(valor):
                    PR = estaciones_ref.loc[i].dropna()
                    if not PR.empty:
                        # Método Campos-Aranda: ajuste proporcional
                        df.at[i, estacion] = promedio_estacion * (PR / promedio_ref[PR.index]).mean()

    return df

# 📌 Ejecutar método y guardar resultados
df = campos_aranda(df)
df.to_csv("datos_completados_campos_aranda.csv", index=False)
print("Proceso completado con el método de Campos-Aranda. Resultados guardados en 'datos_completados_campos_aranda.csv'")