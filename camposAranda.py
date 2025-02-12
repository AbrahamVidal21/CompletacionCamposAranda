import pandas as pd

# Cargar la tabla desde un archivo CSV (suponiendo que se llama "datos.csv")
# Asegúrate de que la primera fila contenga los encabezados correctos
#df = pd.read_csv("datos.csv")

ruta = r"C:\Users\User\Desktop\Analisis de Socavacion\Miraflores\Python\CompletacionLluviaCamposArnada\datos.csv"

# Intenta leer con encoding='latin1'
try:
    df = pd.read_csv(ruta, encoding='latin1')
except UnicodeDecodeError:
    df = pd.read_csv(ruta, encoding='ISO-8859-1')

print(df.head())  # Muestra las primeras filas para verificar la lectura correcta


# Reemplazar "ND" por NaN para manejar valores faltantes
df.replace("ND", pd.NA, inplace=True)

# Convertir todas las columnas (excepto "AÑO") a valores numéricos
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)

# Ordenar cada columna de mayor a menor, excluyendo la columna "AÑO"
columnas_numericas = df.columns[1:]
df_ordenado = df.copy()
df_ordenado[columnas_numericas] = df[columnas_numericas].apply(lambda x: x.sort_values(ascending=False).values)

# Guardar el resultado en un nuevo archivo CSV
df_ordenado.to_csv("datos_ordenados.csv", index=False)

# Mostrar las primeras filas del DataFrame ordenado
print(df_ordenado.head())