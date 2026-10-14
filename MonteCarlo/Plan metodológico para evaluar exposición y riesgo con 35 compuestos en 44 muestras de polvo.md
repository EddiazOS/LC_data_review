# Plan metodológico para evaluar exposición y riesgo con 35 compuestos en 44 muestras de polvo

## Decisión metodológica central

La matriz de concentraciones individuales de 35 compuestos por 44 muestras debe conservarse completa durante la modelación. No conviene reemplazar cada compuesto por su media antes de la simulación, porque ello eliminaría la variabilidad entre muestras y la coocurrencia real de la mezcla. El diseño recomendado combina: análisis descriptivo con datos censurados; evaluación determinista de tendencia central y exposición alta; evaluación probabilística de Monte Carlo; y caracterización de riesgo por compuesto, ruta, grupo etario y mezcla.

La evaluación primaria debe cubrir ingestión incidental de polvo y contacto dérmico. La inhalación sólo debe incorporarse si existen datos de concentración en aire o una fracción respirable del polvo y un modelo de resuspensión justificable; una concentración en polvo total, por sí sola, no equivale a una concentración inhalada. La literatura de polvo doméstico indica además que la ingestión suele dominar sobre el contacto dérmico para PBDE y otros retardantes, particularmente en niños pequeños.[^1][^2][^3]

## Alcance y receptores

Se deben definir a priori el microambiente representado por las 44 muestras —vivienda, automóvil, escuela, oficina u otro—, la fracción granulométrica analizada, la unidad final de concentración y si cada muestra representa un sitio independiente. La fracción de polvo importa: la literatura advierte que seleccionar arbitrariamente el tamaño de partícula puede cambiar las concentraciones y las estimaciones de exposición hasta en un orden de magnitud, y recomienda prestar especial atención a partículas menores de 100 µm para contacto humano.[^4]

El análisis principal puede usar cinco etapas de vida para comparabilidad con Olivero-Verbel et al.: infante, niño pequeño, niño, adolescente y adulto. Sin embargo, para una implementación regulatoria más sólida conviene armonizar los cortes etarios con EPA: <6 meses, 6–<12 meses, 1–<2 años, 2–<6 años, 6–<12 años, 12 años–adulto. EPA publica factores específicos por edad para ingestión de polvo y peso corporal, por lo que no se deben mezclar factores de grupos etarios incompatibles.[^5][^6][^7]

## Preparación de datos

### Identidad y unidades

Se construirá un diccionario con nombre, acrónimo, CAS, familia química, estándar interno, unidad original, LOD, LOQ, recuperación, precisión, frecuencia de detección y valor toxicológico disponible para cada compuesto. Todas las concentraciones se convertirán a ng/g de peso seco y, antes de entrar a ecuaciones de dosis, a mg/kg; numéricamente, 1 ng/g equivale a 0.001 mg/kg. Deben documentarse recuperación, blancos, duplicados y cualquier corrección aplicada, sin volver a corregir concentraciones ya reportadas por recuperación.

Como control del método LC–MS/MS, se reportarán para cada analito las transiciones cuantificadora y confirmatoria, tiempo de retención, curva de calibración, rango lineal, coeficiente de determinación, LOD, LOQ, recuperación, precisión intra/interdía, blancos y criterios de aceptación. El estudio colombiano que sirve de precedente publicó recuperaciones, RSD, LOD y LOQ por analito, además de parámetros SRM, como parte integral de la trazabilidad analítica.[^8]

### Datos censurados

Los valores <LOD o <LOQ se tratarán como observaciones censuradas, no como ceros. Para frecuencia de censura baja puede presentarse LOD/2 o LOQ/2 únicamente como análisis de sensibilidad; para el análisis principal se recomienda regresión robusta sobre estadísticos de orden (ROS), máxima verosimilitud censurada o imputación múltiple truncada entre cero y el límite analítico. La sustitución constante puede sesgar medias, varianzas y asociaciones; MLE y ROS suelen presentar menor sesgo, y la imputación múltiple distribucional funciona mejor bajo censura moderada o alta.[^9][^10][^11][^12]

Se crearán al menos tres juegos de resultados: lower bound, con no detectados en cero; middle bound, con LOD/2 o LOQ/2; y upper bound, con el límite completo. El análisis probabilístico principal usará imputación múltiple censurada, y la amplitud entre escenarios se informará como incertidumbre analítica.

### Descripción estadística

Para cada compuesto se calcularán frecuencia de detección, mediana, media geométrica, percentiles 25, 75, 90 y 95, rango, desviación geométrica e intervalo de confianza por bootstrap. Las concentraciones ambientales suelen ser asimétricas, multimodales y con colas pesadas, de modo que no se asumirá automáticamente una única lognormal. Se compararán lognormal, gamma y Weibull mediante AIC/BIC y pruebas de ajuste; cuando ninguna distribución sea adecuada, se empleará la distribución empírica.[^13]

La matriz de 44 muestras se analizará con correlación de Spearman sobre datos imputados múltiples, perfiles relativos, análisis de agrupamiento y, sólo si la adecuación muestral lo permite, PCA. Con 44 observaciones y 35 variables, PCA y análisis de fuentes serán exploratorios; se deberá informar KMO, prueba de Bartlett, cargas, varianza explicada y estabilidad por bootstrap. PMF sólo se recomienda si existen incertidumbres analíticas por observación y un número suficiente de muestras; no debe presentarse como resultado confirmatorio con una relación muestra/variable tan limitada.

## Modelo de exposición

### Ingestión incidental

Para el compuesto i, muestra j y grupo etario g, la dosis diaria promedio por ingestión se estimará como:

\[
ADD_{ing,i,j,g}=\frac{C_{i,j}\times IR_g\times F_{micro,g}\times EF_g\times ED_g\times CF}{BW_g\times AT_{nc,g}}
\]

Aquí, C es concentración en polvo; IR es la tasa de ingestión de polvo; Fmicro es la fracción del día o de la ingestión asignada al microambiente; EF es frecuencia de exposición; ED es duración; BW es peso corporal; ATnc es el tiempo de promediación no cancerígeno; y CF asegura la conversión de unidades. Si C está en ng/g e IR en g/día, CF = 10^-6 mg/ng.

Para exposición crónica no cancerígena se usará ATnc = ED × 365 días, lo que simplifica la dosis a una media diaria durante el periodo expuesto. Para cáncer se usará ATc = LT × 365 días, con LT igual a la vida de referencia seleccionada y explícitamente citada. No se debe usar un AT de 70 años en una dosis no cancerígena ni multiplicar simultáneamente por una fracción diaria y por una frecuencia anual que ya represente el mismo patrón, pues ambas prácticas reducen artificialmente la dosis.

### Contacto dérmico

La dosis absorbida por contacto dérmico se calculará como:

\[
ADD_{derm,i,j,g}=\frac{C_{i,j}\times SA_g\times AF_{dust,g}\times ABS_{d,i}\times EF_g\times ED_g\times CF_d}{BW_g\times AT_g}
\]

SA es el área de piel descubierta en contacto; AFdust es la adherencia de polvo en mg/cm² por evento; ABSd es la fracción absorbida específica del compuesto; y CFd convierte mg de polvo y ng/g a mg de compuesto. Debe distinguirse estrictamente AFdust, masa de polvo adherida, de ABSd, fracción química absorbida. Cuando no exista ABSd específica, se hará un análisis de sensibilidad con un valor conservador claramente rotulado como supuesto, en vez de asignar absorción de un compuesto análogo sin justificación.

La dosis dérmica absorbida debe compararse con un valor toxicológico expresado en base absorbida. EPA señala que los RfD y factores de pendiente orales suelen basarse en dosis administrada; para contacto dérmico se ajustan mediante la absorción gastrointestinal: RfDabs = RfDoral × ABSGI y SFabs = SForal / ABSGI. Si no hay información, puede asumirse ABSGI = 1, pero el supuesto debe declararse.[^14][^15][^16]

### Inhalación opcional

La inhalación sólo se modelará en un análisis separado si se dispone de Cair (ng/m³) o de una estimación validada de polvo resuspendido. En ese caso:

\[
ADD_{inh,i,g}=\frac{C_{air,i}\times InhR_g\times ET_g\times EF_g\times ED_g\times CF}{BW_g\times AT_g}
\]

InhR es la tasa de inhalación y ET el tiempo diario en el microambiente. Los factores deben corresponder a edad y actividad; EPA recomienda seleccionar tasas de inhalación y patrones de actividad específicos para etapa vital y nivel de actividad.[^17]

## Parámetros operativos

### Valores por edad

La tabla siguiente propone los valores centrales de arranque. Los valores de ingestión y peso corporal provienen de tablas EPA actualizadas; el modelo probabilístico debe usar percentiles o microdatos publicados, no inventar desviaciones estándar a partir de una media.[^7][^5]

| Grupo | Ingestión de polvo central (mg/día) | Ingestión alta (mg/día) | Peso corporal central (kg) |
|---|---:|---:|---:|
| <6 meses | 20 | 60 | usar subgrupo: 4.8–7.4 |
| 6–<12 meses | 40 | 100 | 9.2 |
| 1–<2 años | 50 | 100 | 11.4 |
| 2–<6 años | 30 | 100 | 13.8–18.6 |
| 6–<12 años | 30 | 100 | 31.8 |
| 12 años–adulto | 20 | 60 | 56.8, 71.6 o 80 según edad |

EPA define polvo como polvo sedimentado interior y recomienda seleccionar el factor de ingestión por medio, etapa vital y categoría de exposición. Si se desea replicar el esquema de Olivero-Verbel, sus tasas lognormales fueron 25 ± 24, 61 ± 55, 47 ± 48, 3.2 ± 2.5 y 3.7 ± 2.9 mg/día para infante, niño pequeño, niño, adolescente y adulto, respectivamente; deben tratarse como un escenario de comparabilidad, no como el único conjunto válido.[^18][^19][^8]

El estudio citado utilizó pesos normales de 9.1, 15.4, 30.7, 58.2 y 71.6 kg y áreas cutáneas expuestas de 906, 1,567, 2,825, 4,213 y 4,807 cm², con desviaciones publicadas. Para el análisis principal se aconseja actualizar peso con EPA y calcular el área expuesta según ropa, clima y escenario; el conjunto histórico puede mantenerse como análisis de sensibilidad.[^8]

### Tiempo y frecuencia

La fracción de tiempo en el microambiente debe derivarse del cuestionario de las 44 ubicaciones o de diarios de actividad locales. Si no existe información, se usarán distribuciones de EPA para tiempo interior y se realizará sensibilidad; EPA expresa estos patrones en minutos/día y publica medias y percentiles por edad. No se aplicará automáticamente “tiempo en casa” a muestras de automóvil, escuela u oficina.[^20][^21]

Como referencia de comparabilidad, Olivero-Verbel et al. usaron fracción de tiempo en vivienda de 0.875, 0.792, 0.792, 0.875 y 0.875, y fracción de viaje en automóvil de 0.065 ± 0.063, 0.044 ± 0.039, 0.045 ± 0.050, 0.048 ± 0.050 y 0.065 ± 0.064 para los cinco grupos. También emplearon EF = 319.4 días/año y duración de exposición de 1, 5, 11, 19 y 50 años. Estos parámetros se usarán sólo cuando representen realmente el microambiente estudiado.[^8]

### Absorción dérmica publicada

El precedente colombiano modeló ABSd como lognormal: TCEP 0.283 ± 0.023; TPPO 0.139 ± 0.015; TCIPP 0.247 ± 0.014; TDCIPP, TMCP y TEHP 0.139 ± 0.015. La tabla suplementaria los rotula como porcentajes, pero los valores se comportan como fracciones; antes de programarlos se debe verificar la fuente primaria y ejecutar dos escenarios interpretativos para evitar un error de factor 100. No se extrapolarán automáticamente estos valores a los otros 29 compuestos.[^8]

### Valores toxicológicos

Se construirá una tabla maestra por CAS con RfD oral crónica, RfC inhalatoria, factor de pendiente oral, unidad, fecha, fuente, endpoint crítico, órgano diana, duración y nivel de confianza. La jerarquía será: EPA IRIS; EPA PPRTV o evaluación de riesgo vigente; ATSDR; EFSA u otra agencia autorizada; y sólo después valores publicados revisados por pares. “Sin valor disponible” no significa riesgo cero: el compuesto quedará como brecha toxicológica y podrá priorizarse mediante cociente de margen de exposición si existe un punto de partida.

Para PBDE, EPA informa RfD orales de 1 × 10^-4 mg/kg-día para BDE-47 y BDE-99, 2 × 10^-4 para BDE-153 y 7 × 10^-3 para BDE-209; para BDE-209 también informa un factor de pendiente oral de 7 × 10^-4 (mg/kg-día)^-1. Para OPE, la tabla del estudio colombiano usó RfD en µg/kg-día de 100 para TEHP, 20 para TPPO, 7 para TCEP, 10 para TCIPP y 20 para TDCIPP y TMCP, junto con SF de 0.0032 para TEHP y 0.02 para TCEP. Estos valores deben revalidarse por CAS y fecha antes de congelar el análisis, porque las evaluaciones regulatorias pueden actualizarse.[^22][^23][^24][^8]

## Riesgo no cancerígeno

Para cada compuesto, ruta y grupo se calculará:

\[
HQ_{i,r,g}=\frac{ADD_{i,r,g}}{RfD_{i,r}}
\]

Después se obtendrá HQ agregado por compuesto sumando rutas compatibles y un HI de cribado para la mezcla. HQ o HI ≤1 indica que no se espera un riesgo no cancerígeno apreciable bajo los supuestos; >1 no predice enfermedad, sino que activa una evaluación refinada.[^25]

El HI principal no debe sumar indiscriminadamente los 35 HQ. La suma se estratificará por órgano diana o endpoint compatible —por ejemplo, neurodesarrollo, hígado, riñón, tiroides, reproducción— y por duración equivalente. EPA y la literatura metodológica recomiendan la adición de dosis para sustancias con mecanismo o órgano diana común; si el HI total de cribado supera 1, debe segregarse por sistema diana.[^26][^27][^28]

## Riesgo cancerígeno

Para compuestos con factor de pendiente aplicable:

\[
CR_{i,r,g}=LADD_{i,r,g}\times SF_{i,r}
\]

El riesgo total se sumará entre rutas y carcinógenos solamente cuando las dosis y los factores sean compatibles. El SF es una estimación superior plausible de probabilidad por unidad de ingesta vitalicia y se expresa normalmente en (mg/kg-día)^-1. Los resultados se presentarán como riesgo incremental individual y de mezcla, sin asignar riesgo cancerígeno cuantitativo a compuestos carentes de SF.[^29]

## Monte Carlo

### Estructura de simulación

Se ejecutarán como mínimo 100,000 iteraciones por grupo etario y escenario, con semilla reproducible. La convergencia se verificará comparando percentiles P50, P90, P95 y P99 en bloques sucesivos; el criterio será un cambio <1% en P50 y P95. La literatura precedente utilizó 10,000 iteraciones y reportó P10, P50 y P90, pero el mayor número propuesto reduce error Monte Carlo con bajo costo computacional.[^30]

En cada iteración se seleccionará una fila completa entre las 44 muestras, no 35 concentraciones independientes. Así se preservan correlaciones y perfiles reales entre compuestos. Para incorporar incertidumbre por tamaño muestral se usará bootstrap por muestra: remuestrear una de las 44 filas con reemplazo y, dentro de cada fila, extraer valores imputados para los no detectados y una distribución de error analítico basada en precisión/recuperación.

Luego se muestrearán conjuntamente los factores fisiológicos y de conducta. Peso y superficie corporal deben estar correlacionados; edad, peso, ingestión de polvo y tiempo de actividad tampoco deben tratarse como completamente independientes. Se emplearán vectores empíricos conjuntos cuando existan o una cópula con correlaciones documentadas. Las distribuciones se truncarán en cero y en límites fisiológicamente plausibles.

### Variabilidad e incertidumbre

Se recomienda un Monte Carlo bidimensional. El bucle externo representará incertidumbre epistémica —imputación de censurados, error analítico, distribución seleccionada, ABSd, RfD/SF y bootstrap de 44 muestras—; el bucle interno representará variabilidad interindividual —peso, ingestión, tiempo, área cutánea y frecuencia. Este diseño permite informar, por ejemplo, la distribución poblacional P95 y el intervalo de incertidumbre de ese P95, en vez de combinar ambos conceptos en una sola curva.

Los RfD y SF no deben modelarse automáticamente como uniformes. Son puntos de referencia regulatorios, no parámetros poblacionales observados; se mantendrán fijos en el análisis principal y se variarán por escenarios de fuente toxicológica. El estudio de referencia los etiquetó como uniformes, pero sin límites publicados esa distribución no se puede reproducir de manera transparente.[^8]

### Sensibilidad

Se calcularán coeficientes de correlación parcial por rangos (PRCC) para salidas monotónicas y Sobol de primer orden/total para no linealidad e interacciones. La sensibilidad se reportará para concentración, muestra, IR, BW, tiempo, EF, ED, SA, AFdust y ABSd. La literatura de vehículos halló que concentración, tiempo dentro del vehículo, frecuencia y duración contribuían de manera importante, lo que respalda su inclusión explícita.[^30]

## Análisis determinista

Antes del Monte Carlo se ejecutará un escenario de tendencia central y uno de exposición razonable alta. El central combinará mediana de concentración y factores centrales; el alto combinará P95 de concentración con factores superiores compatibles, evitando multiplicar simultáneamente todos los máximos. Los resultados deterministas funcionarán como control de calidad del código y facilitarán comparación con la literatura.

Para cada compuesto se presentarán ADD por ingestión y dérmica, HQ por ruta, HQ total, contribución porcentual al HI por órgano y CR cuando corresponda. Para la mezcla se presentarán P50, P90, P95 y P99, probabilidad de HQ/HI >1 y probabilidad de CR sobre los niveles de gestión seleccionados.

## Validación y controles

Se verificará manualmente una iteración con unidades desplegadas y se crearán pruebas automáticas para: concentraciones y dosis no negativas; dosis infantil generalmente superior a la adulta cuando IR/BW sea mayor; igualdad entre cálculo vectorizado y manual; cancelación correcta de ED en ADD no cancerígena; y conservación de correlaciones al remuestrear filas. Se realizará una auditoría de factores 1,000 y 1,000,000, principales fuentes de error al convertir ng/g, µg/kg y mg/kg.

Se repetirán los resultados bajo: lower/middle/upper bound de censura; distribución paramétrica frente a empírica; parámetros EPA frente a Olivero-Verbel; ABSd mínimo, central y máximo; exclusión uno-a-uno de muestras extremas; y concentración con/sin corrección por recuperación. Las conclusiones sólo se considerarán robustas si la categoría de riesgo no cambia materialmente entre escenarios.

## Flujo ejecutable

1. Congelar la matriz maestra 44 × 35, metadatos, LOD/LOQ y control de calidad.
2. Verificar identidad CAS, unidades y familias químicas.
3. Cuantificar censura y generar imputaciones múltiples.
4. Describir distribuciones y perfiles de mezcla por muestra.
5. Construir la tabla maestra de factores de exposición por edad y microambiente.
6. Construir la tabla toxicológica con fuente y endpoint.
7. Ejecutar escenarios deterministas central y alto.
8. Programar Monte Carlo por remuestreo de filas completas.
9. Separar variabilidad e incertidumbre en dos dimensiones.
10. Calcular ADD/LADD, HQ, HI por órgano y CR.
11. Evaluar convergencia, sensibilidad y escenarios alternativos.
12. Exportar tablas reproducibles, distribuciones, contribuciones y registro de decisiones.

## Productos mínimos

El manuscrito debe incluir una tabla de los 35 compuestos y su desempeño analítico; una tabla de factores por etapa vital; una tabla toxicológica por CAS; ecuaciones y unidades; reglas para censura; descripción exacta de distribuciones y truncamientos; iteraciones, semilla y software; y criterios para sumar riesgos. Los anexos deben contener la matriz anonimizada, código versionado, diccionario de variables, resultados de ajuste distribucional, diagnóstico de convergencia y todas las evaluaciones de sensibilidad.

El software recomendado es R o Python, por reproducibilidad. En R pueden emplearse `NADA2`/`survival` para censura, `fitdistrplus` para ajuste, `copula` para dependencias, `sensitivity` para PRCC/Sobol y `targets` para el flujo; en Python, `pandas`, `scipy`, `statsmodels`, `lifelines`, `SALib` y `numpy.random.Generator`. Las versiones, semilla, sistema operativo y hash de los archivos de entrada deben conservarse en el registro del proyecto.

---

## References

1. [Levels, distribution, childhood exposure assessment, and influencing factors of polybrominated diphenyl ethers (PBDEs) in household dust from nine cities in China.](https://linkinghub.elsevier.com/retrieve/pii/S0048969723012287) - Household dust is an important source of premature exposure to polybrominated diphenyl ethers (PBDEs...

2. [Factors impacting human exposure to legacy and emerging contaminants in residential dust in Beijing, China: Characteristics of indoor microenvironment.](https://linkinghub.elsevier.com/retrieve/pii/S0045653524009883) - Exposure to indoor dust is of concern since dust may be contaminated by various toxic chemicals and ...

3. [Polybrominated diphenyl ethers (PBDEs) in household dust: A systematic review on spatio-temporal distribution, sources, and health risk assessment](https://www.sciencedirect.com/science/article/abs/pii/S0045653522041340) - Much attention has been paid on polybrominated diphenyl ethers (PBDEs) in household dust due to thei...

4. [Particle size: A missing factor in risk assessment of human exposure to toxic chemicals in settled indoor dust](https://www.sciencedirect.com/science/article/abs/pii/S0160412012001845) - For researches on toxic chemicals in settled indoor dust, selection of dust fraction is a critical i...

5. [[PDF] Exposure Factors Handbook - Chapter 8: Body Weight Studies](https://www.epa.gov/system/files/documents/2025-01/efh-chapter08_508.pdf)

6. [[PDF] Chapter 5 (Soil and Dust Ingestion) 2017 update - EPA](https://www.epa.gov/sites/default/files/2018-01/documents/efh-chapter05_2017.pdf)

7. [chapter_5_tables.xlsx](https://www.epa.gov/sites/default/files/2018-01/chapter_5_tables.xlsx)

8. [Journal of Environmental Exposure Assessment](https://oaepublishstorage.blob.core.windows.net/494122b9-88d4-4167-bf68-91bb266047ac/4671-SupplementaryMaterials.pdf) - DOI: 10.20517/jeea.2021.08. Journal of Environmental. Exposure ... Supplementary Table 5. Parameters...

9. [Censoring trace-level environmental data: statistical analysis ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8224532/) - Trace-level environmental data typically include values near or below detection and quantitation thr...

10. [Handling of dioxin measurement data in the presence of non ...](https://pure.psu.edu/en/publications/handling-of-dioxin-measurement-data-in-the-presence-of-non-detect/)

11. [Much Ado About Next to Nothing: Incorporating Nondetects in ...](https://academic.oup.com/annweh/article/54/3/257/223531) - Abstract. A great many papers and one textbook have been published on the topic of how to incorporat...

12. [Multiple-Imputation Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6182903/) - This study evaluates methods for handling data with low (10%) to severe (90%) left-censoring within ...

13. [Addressing extrema and censoring in pollutant ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC3857711/) - Volatile organic compounds (VOC), which include many hazardous chemicals, have been used extensively...

14. [[PDF] FINAL DRAFT RISK ASSESSMENT (RA) GUIDANCE FOR ... - EPA](https://semspub.epa.gov/work/02/68741.pdf)

15. [Risk Assessment Guidance for Superfund Volume I](https://semspub.epa.gov/work/06/217326.pdf)

16. [Exposure Dose Guidance for Soil/Sediment Dermal Absorption](https://www.atsdr.cdc.gov/pha-guidance/resources/ATSDR-EDG-Soil-Sediment-Dermal-Absorption-508.pdf) - EPA recommends adjusting health guidelines, such as RfDs, MRLs, and oral slope factors, from an admi...

17. [Exposure Assessment Tools by Media - Air | US EPA](https://www.epa.gov/expobox/exposure-assessment-tools-media-air) - EPA ExpoBox is a toolbox for exposure assessors. Its purpose is to provide a compendium of exposure ...

18. [Highlights of the Exposure Factors Handbook (2011 Final Report) - Chapter 5](https://www.epa.gov/sites/default/files/2015-06/documents/efh_highlights_chap5.pdf)

19. [Exposure Assessment Tools by Media - Soil and Dust | US EPA](https://www.epa.gov/expobox/exposure-assessment-tools-media-soil-and-dust) - EPA ExpoBox is a toolbox for exposure assessors. Its purpose is to provide a compendium of exposure ...

20. [Exposure Factors Handbook - Chapter 16](https://www.epa.gov/sites/default/files/2015-09/documents/efh-chapter16.pdf) - These variables can be dependent on human activity patterns and time spent at each activity and/or l...

21. [Exposure Factors Handbook - Chapter 16: Activity Factors](https://www.epa.gov/system/files/documents/2025-01/efh-chapter16_508.pdf)

22. [tetrabromodiphenyl ether (bde-47)](https://iris.epa.gov/static/pdfs/1010tr.pdf)

23. [Technical Fact Sheet Polybrominated Diphenyl Ethers (PBDEs)](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P100TLNI.txt)

24. [Technical Fact Sheet Polybrominated Diphenyl Ethers (PBDEs ...](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P100LTGN.txt)

25. [RCRA DTSD Chapter 4 – Risk and Hazard Assessment](https://www.epa.gov/sites/default/files/2020-09/documents/chap4.pdf)

26. [If Cumulative Risk Assessment Is the Answer, What Is ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1867996/) - Cumulative risk refers to the combined threats from exposure via all relevant routes to multiple str...

27. [Implementation of the basic hazard index screening for health risks associated with simultaneous exposure to multiple chemicals using a standardized target organ and systems framework](https://academic.oup.com/ieam/article/13/5/852/7732701?guestAccessKey=) - Abstract . Environmental health risk assessments often involve assessing the potential health effect...

28. [[PDF] Framework for Assessing Health Impacts of Multiple Chemicals and ...](https://www.atsdr.cdc.gov/interaction-profiles/media/pdfs/ipga-a.pdf)

29. [Regional Screening Levels (RSLs) - User's Guide | US EPA](https://www.epa.gov/risk/regional-screening-levels-rsls-users-guide) - Regional Screening Level RSL user guide provides extensive guidance for risk assessors doing Chemica...

30. [Exposure Factors Handbook 1997](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1003FLQ.TXT)

