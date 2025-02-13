# Método de Campos Aranda para Completación de Series Hidrometeorológicas

## 📌 Descripción
El **Método de Campos Aranda** es una técnica avanzada para la completación de datos faltantes en series hidrometeorológicas, especialmente en registros de precipitaciones. Este método mejora la precisión al utilizar mínimos cuadrados ponderados y considerar la relación entre estaciones auxiliares y la estación en estudio.

### ✅ **Ventajas del Método:**
- **Alta precisión:** Ajuste basado en correlaciones entre estaciones.
- **Eficiente para diferencias grandes:** Útil cuando las precipitaciones medias difieren en más del 10%.
- **Ampliamente utilizado:** Recomendado en manuales técnicos como CONAGUA, IMTA y MAPAS.

---
## 📝 Descripción del Código en Python
El script realiza la completación de precipitaciones faltantes mediante el método de Campos Aranda. A continuación se explican las secciones principales:

### **1️⃣ Carga de Datos:**
- Carga el archivo CSV.
- Convierte valores no definidos ('ND') en `NaN`.
- Asegura que todos los datos sean numéricos.

### **2️⃣ Selección de Estaciones Auxiliares:**
- Identifica estaciones con datos completos para usarlas como referencia.

### **3️⃣ Cálculo de Coeficientes (Mínimos Cuadrados):**
- Aplica el método de **Campos Aranda**:  
  \[ Px = \frac{\sum (PR \times PM)}{\sum PM^2} \]
  Donde:
  - **Px:** Precipitación faltante.
  - **PR:** Precipitación registrada en estaciones auxiliares.
  - **PM:** Precipitación media anual.

### **4️⃣ Completación de Datos:**
- Rellena los valores faltantes mediante la ecuación anterior.

### **5️⃣ Exportación de Resultados:**
- Guarda el archivo `datos_completados.csv` con los valores completados.

---
## 🛠️ **Ejecución del Script:**
1. Instala dependencias: `pip install pandas numpy`
2. Coloca tu archivo `datos.csv` en la carpeta del script.
3. Ejecuta: `python completacion_campos_aranda.py`
4. Verifica el archivo `datos_completados.csv`.

---
## 📚 **Referencias:**
- Campos-Aranda, D. F. (2002). *Completación de series hidrometeorológicas*. IMTA.
- CONAGUA. (2014). *Manual de Prácticas Hidrológicas* (MAPAS #19).