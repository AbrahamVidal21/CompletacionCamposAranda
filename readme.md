README - Método de Campos Aranda para Completación de Datos de Lluvia

Descripción

Este programa en Python implementa el método de Campos Aranda para la completación de datos de lluvia en estaciones climatológicas con registros faltantes. Utiliza la correlación entre estaciones cercanas y la normalización de datos para estimar valores faltantes de manera precisa.

Fundamento Teórico

El método de Campos Aranda se basa en la relación entre la precipitación media anual de estaciones cercanas para estimar datos faltantes. La ecuación fundamental utilizada es:

                    Px = (Nx / Nr) * Pr
Donde:

P_x: Precipitación estimada en la estación con datos faltantes.

N_x: Precipitación media anual en la estación con datos faltantes.

N_r: Precipitación media anual en la estación de referencia.

P_r: Precipitación registrada en la estación de referencia en el periodo correspondiente.

Pasos de Implementación

Lectura de datos: El programa lee los datos de lluvia de diferentes estaciones desde archivos CSV.

Ordenamiento de datos: Se organizan los datos de mayor a menor para cada estación.

Selección de estaciones cercanas: Se identifican estaciones con registros completos y características climatológicas similares.

Cálculo de la media anual de precipitación para cada estación.

Aplicación del método de normalización para estimar los valores faltantes.

Validación de resultados mediante análisis estadísticos y revisión de la consistencia de la serie temporal.

Requisitos del Proyecto

Python 3.x

Pandas

NumPy

Para instalar las dependencias, ejecutar:

pip install pandas numpy

Ejemplo de Uso

Para ejecutar el programa, usar el siguiente comando en la terminal:

python camposAranda.py

El programa procesará automáticamente todas las estaciones y generará una salida con los datos completados.

Referencias

Campos-Aranda, D. F. (1998). Hidrología Superficial. Universidad Autónoma de San Luis Potosí.

Chow, V. T., Maidment, D. R., & Mays, L. W. (1988). Applied Hydrology. McGraw-Hill.

Comisión Nacional del Agua (CONAGUA). (2015). Manual de procedimientos hidrometeorológicos. CONAGUA.

Este software está diseñado para apoyar estudios hidrológicos y facilitar la reconstrucción de series de datos de lluvia en estaciones meteorológicas.