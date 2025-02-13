import pandas as pd
import numpy as np
import scipy.stats as stats
from lmoments3 import distr
import lmoments3 as lm


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
    "GAMMA II": stats.gamma.fit(precipitaciones, floc=0),
    "GUMBEL": stats.gumbel_r.fit(precipitaciones),
    "L-Moments Normal": distr.nor.lmom_fit(precipitaciones),
    "L-Moments Exponential": distr.exp.lmom_fit(precipitaciones),
    "L-Moments EV1 (Gumbel) Max": distr.gum.lmom_fit(precipitaciones),
    "L-Moments EV2-Max": distr.wei.lmom_fit(precipitaciones),  # Weibull para EV2-Max
    "L-Moments EV3-Min": distr.wei.lmom_fit(-precipitaciones),  # Weibull para EV3-Min (valores negativos)
    "L-Moments GEV Max": distr.gev.lmom_fit(precipitaciones),
    "L-Moments GEV Min": distr.gev.lmom_fit(-precipitaciones),  # GEV para mínimos (valores negativos)
    "L-Moments Pareto": distr.gpa.lmom_fit(precipitaciones),
    "GEV-Max (k spec.)": {"c": 0.1},  # Especificar parámetro de forma (k) manualmente
    "GEV-Min (k spec.)": {"c": -0.1},  # Especificar parámetro de forma (k) manualmente
    "L-Moments GEV-Max (k spec.)": distr.gev.lmom_fit(precipitaciones, c=0.1),  # GEV con k especificado
    "L-Moments GEV-Min (k spec.)": distr.gev.lmom_fit(-precipitaciones, c=-0.1),  # GEV para mínimos con k especificado
    "LogNormal": stats.lognorm.fit(precipitaciones, floc=0),
    "Log-Pearson": stats.pearson3.fit(precipitaciones),
    "GAMMA": stats.gamma.fit(precipitaciones, floc=0),
    "WEIBULL": stats.weibull_min.fit(precipitaciones, floc=0),
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
    elif dist.startswith("GUMBEL"):
        valores = stats.gumbel_r.ppf(1 - probabilidad_excedencia, *params)
    elif dist.startswith("L-Moments"):
        if "GEV" in dist:
            if "k spec." in dist:
                valores = distr.gev.ppf(1 - probabilidad_excedencia, **params)
            else:
                valores = distr.gev.ppf(1 - probabilidad_excedencia, **params)
        elif "EV1" in dist:
            valores = distr.gum.ppf(1 - probabilidad_excedencia, **params)
        elif "EV2" in dist:
            valores = distr.wei.ppf(1 - probabilidad_excedencia, **params)
        elif "EV3" in dist:
            valores = -distr.wei.ppf(probabilidad_excedencia, **params)  # Invertir para mínimos
        elif "Pareto" in dist:
            valores = distr.gpa.ppf(1 - probabilidad_excedencia, **params)
        elif "Normal" in dist:
            valores = distr.nor.ppf(1 - probabilidad_excedencia, **params)
        elif "Exponential" in dist:
            valores = distr.exp.ppf(1 - probabilidad_excedencia, **params)
    elif dist == "Log-Pearson":
        valores = stats.pearson3.ppf(1 - probabilidad_excedencia, *params)
    elif dist == "WEIBULL":
        valores = stats.weibull_min.ppf(1 - probabilidad_excedencia, *params)
    
    resultados[dist] = valores

# 📌 Convertir a DataFrame
df_resultados = pd.DataFrame(resultados)

# 📌 Cálculo del Error Estándar Ajustado (EEA)
eea = {dist: np.std(df_resultados[dist]) for dist in ajustes.keys()}
df_eea = pd.DataFrame([eea], index=["EEA"])

# 📌 Mostrar resultados
print("Valores ajustados para cada Tr:")
print(df_resultados)
print("\nError Estándar Ajustado (EEA) para cada distribución:")
print(df_eea)