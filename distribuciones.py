import pandas as pd
import numpy as np
import subprocess
import sys

try:
    import scipy.stats as stats
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy"])
    import scipy.stats as stats

# 📌 Definir los períodos de retorno
Tr = np.array([2, 5, 10, 25, 50, 100, 200, 500, 1000, 2000])

# 📌 Cargar la tabla de precipitación desde un CSV
ruta_csv = "precipitacion_media_ponderada.csv"
df = pd.read_csv(ruta_csv, encoding='latin1')

# 📌 Extraer los valores de precipitación
precipitaciones = df["Precipitacion (mm)"].dropna()

# 📌 Probabilidad de excedencia
probabilidad_excedencia = 1 - (1 / Tr)

# 📌 Ajustar distribuciones
ajustes = {
    "NORMAL": stats.norm.fit(precipitaciones),
    "LOG. NORMAL II": stats.lognorm.fit(precipitaciones, floc=0),
    "LOG. NORMAL III": stats.lognorm.fit(precipitaciones, floc=0),  # Puede ajustarse con otra variante si es necesario
    "GAMMA II": stats.gamma.fit(precipitaciones, floc=0),
    "GAMMA III": stats.gamma.fit(precipitaciones, floc=0),
    "GUMBEL": stats.gumbel_r.fit(precipitaciones),
    "DOBLE GUMBEL": stats.gumbel_r.fit(precipitaciones)  # Puedes modificar la metodología si es diferente
}

# 📌 Cálculo de precipitación ajustada para cada Tr
resultados = {"Tr": Tr}

for dist, params in ajustes.items():
    if dist.startswith("NORMAL"):
        valores = stats.norm.ppf(1 - probabilidad_excedencia, *params)
    elif dist.startswith("LOG. NORMAL"):
        valores = stats.lognorm.ppf(1 - probabilidad_excedencia, *params)
    elif dist.startswith("GAMMA"):
        valores = stats.gamma.ppf(1 - probabilidad_excedencia, *params)
    elif "GUMBEL" in dist:
        valores = stats.gumbel_r.ppf(1 - probabilidad_excedencia, *params)
    
    resultados[dist] = valores

# 📌 Convertir a DataFrame
df_resultados = pd.DataFrame(resultados)


# 📌 Cálculo del Error Estándar Ajustado (EEA)
eea = {dist: np.std(df_resultados[dist]) for dist in ajustes.keys()}
df_eea = pd.DataFrame([eea], index=["EEA"])

# 📌 Agregar EEA a la tabla final
df_resultados = pd.concat([df_resultados, df_eea])
print(df_resultados)
