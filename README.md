# Auditoría y Análisis Reproducible de Contaminantes en Polvo de Interiores (LC-MS/MS)

Repositorio de auditoría analítica, recompilación de datos brutos y reproducción computacional de resultados para el estudio de **35 contaminantes emergentes (retardantes de llama organofosforados [PFRs], plastificantes alternativos [APs] y ésteres de ftalato [PHs]) en polvo de interiores en Colombia**.

---

## 🚀 Ejecutar en Google Colab

Cada cuaderno cuenta con auto-detección de entorno. Al abrirlo en Colab, clona automáticamente este repositorio y configura las rutas de datos para una ejecución inmediata y sin errores de ruta.

| Nivel / Sección | Cuaderno Jupyter | Enlace Directo |
| :--- | :--- | :---: |
| **00. Curación** | Extracción, trazabilidad y saneamiento de datos brutos a CSV | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/00_extraccion_y_curacion_csv.ipynb) |
| **01. Nivel 1** | Ocurrencia, frecuencias de detección y estadística descriptiva dual (LOQ vs LOQ/2) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/01_nivel_1_ocurrencia_y_descriptiva.ipynb) |
| **02. Nivel 2** | Variabilidad microambiental (Casas, Autos, Oficinas) y espacial (Bogotá, Medellín, Cartagena) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/02_nivel_2_variabilidad_espacial.ipynb) |
| **03. Nivel 3** | Análisis multivariado: Matriz de correlación de Spearman (32×32) y PCA con elipses al 95% | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/03_nivel_3_analisis_multivariado.ipynb) |
| **04. Nivel 4** | Comparación y síntesis de literatura internacional (Mini-Review) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/04_nivel_4_sintesis_mini_review.ipynb) |
| **05. Nivel 5** | Evaluación probabilística de riesgo a la salud (Simulaciones Monte Carlo $N=10{,}000$, EDI, HQ e ILCR) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EddiazOS/LC_data_review/blob/main/05_Analisis_Reproducible/notebooks/05_nivel_5_evaluacion_riesgo_salud.ipynb) |

---

## 📁 Estructura del Repositorio

```text
LC_data_review/
├── README.md
├── .gitignore
└── 05_Analisis_Reproducible/
    ├── build_all_notebooks.py      # Script de generación del scaffold de cuadernos
    ├── datos_curados/              # Datos tabulares saneados (formato CSV)
    │   ├── concentraciones_ng_g.csv      # Matriz 44x35 continua (ng/g)
    │   ├── estado_deteccion.csv          # Matriz 44x35 booleana (1: >= LOQ, 0: < LOQ)
    │   ├── limites_cuantificacion.csv    # LOQs nominales y LOQs de corte por muestra
    │   ├── muestras_metadata.csv         # Metadatos de las 44 muestras (Ciudad, Microambiente)
    │   └── compuestos_metadata.csv       # Metadatos de los 35 compuestos (CAS, MW, log Kow, Familia)
    ├── notebooks/                  # Cuadernos interactivos para Colab y Local
    │   ├── 00_extraccion_y_curacion_csv.ipynb
    │   ├── 01_nivel_1_ocurrencia_y_descriptiva.ipynb
    │   ├── 02_nivel_2_variabilidad_espacial.ipynb
    │   ├── 03_nivel_3_analisis_multivariado.ipynb
    │   ├── 04_nivel_4_sintesis_mini_review.ipynb
    │   └── 05_nivel_5_evaluacion_riesgo_salud.ipynb
    └── outputs/                    # Gráficos (300 DPI) y tablas estadísticas generadas
        ├── figuras/
        └── tablas/
```

---

## 🔬 Metodología de Tratamiento de Censura Analítica

En los cuadernos se implementa una evaluación comparativa en paralelo:
1. **Método A (Sustitución por LOQ):** Enfoque conservador histórico del borrador previo.
2. **Método B (Sustitución por LOQ/2):** Estándar internacional riguroso (EPA / literatura en ciencias ambientales).

Ambos métodos se computan simultáneamente para verificar la robustez estadística y la sensibilidad de las conclusiones frente al tratamiento de datos no detectados.
