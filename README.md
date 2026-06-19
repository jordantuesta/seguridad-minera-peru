# ⛏ Seguridad Minera Perú · Análisis 2002–2021

![Pipeline](https://img.shields.io/badge/Pipeline-Python%20→%20Power%20BI%20→%20Alerta-1A3A5C?style=flat-square)
![Datos](https://img.shields.io/badge/Datos-MINEM%20Perú-D85A30?style=flat-square)
![Registros](https://img.shields.io/badge/Registros-901%20accidentes-EF9F27?style=flat-square)
![Estado](https://img.shields.io/badge/Estado-Publicado-1D9E75?style=flat-square)

> Pipeline end-to-end de análisis y automatización sobre 901 accidentes mortales en la minería peruana (2002–2021) usando datos reales del Ministerio de Energía y Minas (MINEM).

---

## 🎯 Objetivo del proyecto

Demostrar un pipeline completo de **análisis de datos + automatización** aplicado a seguridad industrial:

1. **Python** — limpieza de datos crudos, corrección de errores y feature engineering
2. **Power BI** — dashboard interactivo con objetos visuales de IA integrados
3. **Python (alerta)** — sistema automático que detecta períodos de alto riesgo y envía email HTML al responsable de seguridad

---

## 📊 Hallazgos principales

| Métrica | Valor |
|---|---|
| Total accidentes mortales | **901** |
| Período analizado | **2002 – 2021 (20 años)** |
| Causa principal | **Desprendimiento de rocas · 247 casos (27%)** |
| Departamento más afectado | **Junín · 124 casos** |
| Fallecidos en el acto | **89%** |
| Promedio mensual histórico | **4.82 accidentes/mes** |
| Gap de datos detectado | **2017–2019 · solo 10 registros vs. ~60 esperados** |

> 💡 La Región Centro concentra el 57% de los casos. Una intervención focalizada en Desprendimiento de rocas reduciría el 27% de las muertes históricas.

---

## 🔄 Pipeline completo

```
Datos crudos MINEM (CSV)
        ↓
┌─────────────────────────┐
│  01 · Python            │  limpieza_datos.ipynb
│  · 19 fechas corregidas │  · Diagnóstico de calidad
│  · 68 nulos tratados    │  · Feature engineering (6 vars)
│  · Gap documentado      │  · 5 gráficos exploratorios
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  02 · Power BI          │  Dashboard interactivo
│  · 15 medidas DAX       │  · Filtros por período y región
│  · Mapa de calor        │  · Elementos influyentes (IA)
│  · Efecto delta barras  │  · Narrativa inteligente (IA)
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│  03 · Alerta automática │  alerta_mineria.py
│  · Detecta anomalías    │  · Compara vs. promedio histórico
│  · Email HTML           │  · Excluye gap 2017-2019
│  · Ejecutable en Colab  │  · Diseño profesional
└─────────────────────────┘
```

---

## 📁 Estructura del repositorio

```
seguridad-minera-peru/
├── 📁 01_python/
│   ├── limpieza_datos.ipynb     # Notebook completo de limpieza y EDA
│   └── alerta_mineria.py        # Script de alerta automática por email
├── 📁 02_dashboard/
│   └── tema_mineria_jordan.json # Tema personalizado Power BI
├── 📁 03_datos/
│   └── README_datos.md          # Instrucciones para obtener datos MINEM
└── README.md
```

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.12 | Limpieza, feature engineering, sistema de alerta |
| Pandas | Manipulación y análisis de datos |
| Matplotlib / Seaborn | Visualización exploratoria |
| smtplib | Envío de email HTML automatizado |
| Power BI Desktop | Dashboard interactivo |
| DAX | 15 medidas calculadas |
| Google Colab | Entorno de ejecución |

---

## ⚡ Feature Engineering (Python)

Variables creadas desde los datos crudos:

| Variable nueva | Descripción |
|---|---|
| `CAUSA_AGRUPADA` | 11 grupos de causas desde texto libre |
| `REGION_MACRO` | Norte / Centro / Sur / Oriente |
| `FALLECIÓ_EN_ACTO` | Booleano: fallecimiento inmediato |
| `DIAS_SOBREVIVENCIA` | Días entre accidente y fallecimiento |
| `TRIMESTRE` | Q1 / Q2 / Q3 / Q4 |
| `NOTA_GAP` | Etiqueta para años con datos incompletos |

---

## 🔴 Sistema de alerta automática

El script `alerta_mineria.py` implementa la siguiente lógica:

```python
# Lógica central del sistema
promedio_historico = 4.82  # accidentes/mes (excluye gap 2017-2019)

if accidentes_mes_actual > promedio_historico:
    enviar_email(tipo="ALERTA", color="#D85A30")
else:
    enviar_email(tipo="NORMAL", color="#1D9E75")
```

**El email generado incluye:**
- Estado del período (ALERTA / NORMAL)
- Comparación vs. promedio histórico
- Causa principal y departamento más afectado
- Hallazgo clave con recomendación de intervención
- Firma del pipeline completo

---

## 📈 Medidas DAX principales

```dax
-- Promedio histórico excluyendo gap
Promedio Historico Anual =
CALCULATE(
    AVERAGEX(VALUES('accidentes'[AÑO]),
    CALCULATE(COUNTROWS('accidentes'))),
    NOT('accidentes'[AÑO] IN {2017, 2018, 2019})
)

-- Efecto visual delta para barras comparativas
Delta para barras =
MAXX(ALL('accidentes'[CAUSA_AGRUPADA]),
    CALCULATE(COUNTROWS('accidentes')))
- COUNTROWS('accidentes')
```

---

## 🚀 Cómo reproducir el proyecto

**1. Obtener los datos**

Los datos son públicos del MINEM. Ver instrucciones en `03_datos/README_datos.md`.

**2. Ejecutar la limpieza**

Abre `01_python/limpieza_datos.ipynb` en Google Colab y ejecuta todas las celdas.

**3. Abrir el dashboard**

Importa el CSV limpio en Power BI Desktop. Aplica el tema desde `02_dashboard/tema_mineria_jordan.json`.

**4. Ejecutar el sistema de alerta**

```bash
# Configura tus credenciales en alerta_mineria.py
# Ejecuta en Colab o localmente:
python alerta_mineria.py
```

---

## 📬 Contacto

**Jordan Tuesta** · Ingeniero Químico · Especialista en automatización de procesos

[![LinkedIn](https://img.shields.io/badge/LinkedIn-jordan--tuesta-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/jordan-tuesta-farfan/)
[![Gmail](https://img.shields.io/badge/Gmail-jordantuesta@gmail.com-D14836?style=flat-square&logo=gmail)](mailto:jordantuesta@gmail.com)

---

*Datos fuente: Ministerio de Energía y Minas del Perú (MINEM) · 901 registros · 2002–2021*
