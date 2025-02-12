import pandas as pd
import numpy as np

# Cargar los datos
ruta = r"C:\Users\User\Desktop\Analisis de Socavacion\Miraflores\Python\CompletacionLluviaCamposArnada\datos.csv"

# Intenta leer con encoding='latin1'
try:
    df = pd.read_csv(ruta, encoding='latin1')
except UnicodeDecodeError:
    df = pd.read_csv(ruta, encoding='ISO-8859-1')

print(df.head())  # Muestra las primeras filas para verificar la lectura correcta

# Convertir "ND" a NaN para manejar datos faltantes
df.replace("ND", np.nan, inplace=True)
df = df.astype(float)  # Asegurar que los datos sean numéricos

# Iterar sobre cada estación con datos faltantes
for estacion in df.columns:
    if df[estacion].isna().sum() > 0:  # Si hay datos faltantes
        print(f"Procesando estación: {estacion}")
        
        # Seleccionar estaciones de referencia (las que tienen datos completos)
        estaciones_ref = df.dropna(axis=1, how='any')  # Columnas sin NaN
        if estaciones_ref.empty:
            print(f"No hay estaciones de referencia para {estacion}")
            continue
        
        # Calcular coeficientes de ajuste
        suma_PR_PM = estaciones_ref.mul(df[estacion], axis=0).sum()
        suma_PR2 = estaciones_ref.pow(2).sum()
        coeficientes = suma_PR_PM / suma_PR2
        
        # Estimar los valores faltantes
        for i, valor in df[estacion].items():
            if pd.isna(valor):
                PR = estaciones_ref.loc[i].dropna()
                if not PR.empty:
                    df.at[i, estacion] = (coeficientes[PR.index] * PR).sum() / coeficientes[PR.index].sum()

# Guardar los datos completados
df.to_csv("datos_completados.csv", index=False)
print("Proceso completado. Datos guardados en 'datos_completados.csv'")