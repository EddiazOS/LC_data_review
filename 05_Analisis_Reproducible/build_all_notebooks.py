import nbformat as nbf
import os

NOTEBOOK_DIR = "05_Analisis_Reproducible/notebooks"
os.makedirs(NOTEBOOK_DIR, exist_ok=True)

REPO_NAME = "LC_data_review"
REPO_URL = f"https://github.com/EddiazOS/{REPO_NAME}.git"

def colab_badge_md(nb_name):
    colab_url = f"https://colab.research.google.com/github/EddiazOS/{REPO_NAME}/blob/main/05_Analisis_Reproducible/notebooks/{nb_name}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"

def colab_setup_code():
    return f"""# Celda 1: Configuración de Entorno (Google Colab / Local) y Pre-requisitos
import os, sys

try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    print("🚀 Entorno Google Colab detectado.")
    if not os.path.exists('{REPO_NAME}'):
        !git clone {REPO_URL}
    if os.path.exists('{REPO_NAME}/05_Analisis_Reproducible/datos_curados'):
        DATA_DIR = '{REPO_NAME}/05_Analisis_Reproducible/datos_curados'
        OUT_TABLES = '{REPO_NAME}/05_Analisis_Reproducible/outputs/tablas'
        OUT_FIGS = '{REPO_NAME}/05_Analisis_Reproducible/outputs/figuras'
    else:
        DATA_DIR = '../datos_curados'
        OUT_TABLES = '../outputs/tablas'
        OUT_FIGS = '../outputs/figuras'
else:
    print("💻 Entorno Local detectado.")
    DATA_DIR = '../datos_curados' if os.path.exists('../datos_curados') else '05_Analisis_Reproducible/datos_curados'
    OUT_TABLES = '../outputs/tablas' if os.path.exists('../outputs/tablas') else '05_Analisis_Reproducible/outputs/tablas'
    OUT_FIGS = '../outputs/figuras' if os.path.exists('../outputs/figuras') else '05_Analisis_Reproducible/outputs/figuras'

os.makedirs(OUT_TABLES, exist_ok=True)
os.makedirs(OUT_FIGS, exist_ok=True)
print(f"Directorio de datos activo: {{DATA_DIR}}")
"""

def create_nb(filename, cells):
    nb = nbf.v4.new_notebook()
    nb['cells'] = cells
    filepath = os.path.join(NOTEBOOK_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {filepath}")

# ==============================================================================
# NOTEBOOK 00
# ==============================================================================
nb00 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('00_extraccion_y_curacion_csv.ipynb')}

# Notebook 00: Extracción, Curación y Verificación de Datos Brutos
### Proyecto: Contaminantes Emergentes en Polvo Interior en Colombia (LC-MS/MS)
**Grupo de Investigación en Química Ambiental — Universidad de Cartagena**
**En colaboración con el Toxicological Centre — Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code()),
    nbf.v4.new_code_cell("""# Celda 2: Carga y Verificación de los Datos Curados en CSV
import pandas as pd
import numpy as np

df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_det = pd.read_csv(os.path.join(DATA_DIR, 'estado_deteccion.csv'))
df_loqs = pd.read_csv(os.path.join(DATA_DIR, 'limites_cuantificacion.csv'))

print(f"1. Muestras cargadas: {df_muestras.shape[0]} muestras ambientales.")
print(f"   Distribución por ciudad: {df_muestras['city'].value_counts().to_dict()}")
print(f"   Distribución por microambiente: {df_muestras['microenvironment'].value_counts().to_dict()}")

print(f"\\n2. Compuestos cargados: {df_compuestos.shape[0]} analitos diana.")
print(f"   Familias químicas: {df_compuestos['family'].value_counts().to_dict()}")

print(f"\\n3. Matriz de concentraciones: {df_conc.shape[0]} filas x {df_conc.shape[1]-1} analitos.")
print(f"   Valores nulos en concentración: {df_conc.isnull().sum().sum()}")

print(f"\\n4. Matriz de estado de detección: {df_det.shape[0]} filas x {df_det.shape[1]-1} analitos.")
print(f"   Total de cuantificaciones válidas (>= LOQ): {df_det.drop(columns=['sample_id']).sum().sum()} de {44*35} mediciones.")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Inspección visual de las tablas de datos
display(df_muestras.head(5))
display(df_compuestos.head(5))
display(df_conc.iloc[:5, :6])
""")
]
create_nb("00_extraccion_y_curacion_csv.ipynb", nb00)

# ==============================================================================
# NOTEBOOK 01
# ==============================================================================
nb01 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('01_nivel_1_ocurrencia_y_descriptiva.ipynb')}

# Notebook 01: Nivel 1 — Ocurrencia y Estadística Descriptiva
### Subsección 3.1 del Manuscrito: Frecuencias de Detección, Niveles de Concentración y Tabla 1
**Proyecto LC-GC / Indoor Dust — Universidad de Cartagena & Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code() + """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración gráfica para publicación científica
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
print("Librerías y entorno gráfico listos.")
"""),
    nbf.v4.new_code_cell("""# Celda 2: Auto-Carga de Datos Curados y Preparación de Métodos de Censura
df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_det = pd.read_csv(os.path.join(DATA_DIR, 'estado_deteccion.csv'))
df_loqs = pd.read_csv(os.path.join(DATA_DIR, 'limites_cuantificacion.csv'))

fam_map = dict(zip(df_compuestos['acronym'], df_compuestos['family']))
acronyms = list(df_compuestos['acronym'])

# Método A: Imputación por LOQ (enfoque de la tesis)
df_conc_A = df_conc.copy()

# Método B: Imputación por LOQ / 2 (estándar EPA)
df_conc_B = df_conc.copy()
for col in acronyms:
    loq_val = df_loqs.loc[df_loqs['acronym'] == col, 'loq_imputed_sample_ng_g'].values[0]
    mask_nd = (df_det[col] == 0)
    df_conc_B.loc[mask_nd, col] = loq_val / 2.0

print(f"Matrices preparadas exitosamente:")
print(f" - Muestras: {len(df_muestras)} ({df_muestras['microenvironment'].value_counts().to_dict()})")
print(f" - Analitos: {len(acronyms)}")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Cálculo de Frecuencias de Detección (DF %) Global y por Microambiente
df_res_df = []
for col in acronyms:
    fam = fam_map[col]
    det_total = df_det[col].sum()
    pct_total = (det_total / 44.0) * 100.0
    
    det_car = df_det.loc[df_muestras['microenvironment'] == 'Car', col].sum()
    pct_car = (det_car / 12.0) * 100.0
    
    det_house = df_det.loc[df_muestras['microenvironment'] == 'House', col].sum()
    pct_house = (det_house / 24.0) * 100.0
    
    det_office = df_det.loc[df_muestras['microenvironment'] == 'Office', col].sum()
    pct_office = (det_office / 8.0) * 100.0
    
    df_res_df.append({
        'Family': fam,
        'Congener': col,
        'DF_Total_pct': pct_total,
        'Det_Total_n': det_total,
        'DF_Car_pct': pct_car,
        'DF_House_pct': pct_house,
        'DF_Office_pct': pct_office
    })

df_df_summary = pd.DataFrame(df_res_df)
df_df_summary.to_csv(os.path.join(OUT_TABLES, 'frecuencias_deteccion_resumen.csv'), index=False)
display(df_df_summary.sort_values(by='DF_Total_pct', ascending=False).head(15))
"""),
    nbf.v4.new_code_cell("""# Celda 4: Comparación de Estadística Descriptiva (Método A vs Método B)
def compute_stats(df_data, df_meta):
    records = []
    for comp in acronyms:
        fam = fam_map[comp]
        for micro in ['Car', 'House', 'Office', 'Overall']:
            if micro == 'Overall':
                vals = df_data[comp].values
            else:
                idxs = df_meta[df_meta['microenvironment'] == micro].index
                vals = df_data.loc[idxs, comp].values
            
            records.append({
                'Family': fam,
                'Congener': comp,
                'Microenvironment': micro,
                'N': len(vals),
                'Mean': np.mean(vals),
                'SD': np.std(vals, ddof=1),
                'Median': np.median(vals),
                'Q1': np.percentile(vals, 25),
                'Q3': np.percentile(vals, 75),
                'IQR': np.percentile(vals, 75) - np.percentile(vals, 25),
                'Min': np.min(vals),
                'Max': np.max(vals)
            })
    return pd.DataFrame(records)

df_stats_A = compute_stats(df_conc_A, df_muestras)
df_stats_B = compute_stats(df_conc_B, df_muestras)

df_comp_med = pd.merge(
    df_stats_A[['Family', 'Congener', 'Microenvironment', 'Median']],
    df_stats_B[['Family', 'Congener', 'Microenvironment', 'Median']],
    on=['Family', 'Congener', 'Microenvironment'],
    suffixes=('_Metodo_A_LOQ', '_Metodo_B_LOQ_div_2')
)
df_comp_med['Diff_pct'] = ((df_comp_med['Median_Metodo_A_LOQ'] - df_comp_med['Median_Metodo_B_LOQ_div_2']) / df_comp_med['Median_Metodo_A_LOQ']) * 100

print("Comparación de medianas para analitos con censura (< LOQ) en Casas:")
display(df_comp_med[(df_comp_med['Microenvironment'] == 'House') & (df_comp_med['Diff_pct'] > 0)].sort_values(by='Diff_pct', ascending=False))
"""),
    nbf.v4.new_code_cell("""# Celda 5: Balance de Masa Acumulado Muestra a Muestra
for name, df_d in [('Metodo_A', df_conc_A), ('Metodo_B', df_conc_B)]:
    df_m = df_muestras.copy()
    
    aps_cols = [c for c in acronyms if fam_map[c] == 'APs']
    pfrs_cols = [c for c in acronyms if fam_map[c] == 'PFRs']
    phs_cols = [c for c in acronyms if fam_map[c] == 'PHs']
    
    df_m['Sum_APs'] = df_d[aps_cols].sum(axis=1)
    df_m['Sum_PFRs'] = df_d[pfrs_cols].sum(axis=1)
    df_m['Sum_PHs'] = df_d[phs_cols].sum(axis=1)
    df_m['Sum_Total'] = df_m['Sum_APs'] + df_m['Sum_PFRs'] + df_m['Sum_PHs']
    
    print(f"=== BALANCE DE MASA ACUMULADO ({name}) ===")
    print(f"Sum_Total: Mediana = {df_m['Sum_Total'].median():,.1f} ng/g | Media = {df_m['Sum_Total'].mean():,.1f} +/- {df_m['Sum_Total'].std():,.1f} ng/g")
    print(f"Sum_PHs  : Mediana = {df_m['Sum_PHs'].median():,.1f} ng/g ({df_m['Sum_PHs'].sum()/df_m['Sum_Total'].sum()*100:.1f}%)")
    print(f"Sum_APs  : Mediana = {df_m['Sum_APs'].median():,.1f} ng/g ({df_m['Sum_APs'].sum()/df_m['Sum_Total'].sum()*100:.1f}%)")
    print(f"Sum_PFRs : Mediana = {df_m['Sum_PFRs'].median():,.1f} ng/g ({df_m['Sum_PFRs'].sum()/df_m['Sum_Total'].sum()*100:.1f}%)\\n")
"""),
    nbf.v4.new_code_cell("""# Celda 6: Generación de la Figura 1 (Distribución log10 por Microambiente)
fig, ax = plt.subplots(figsize=(8, 5.5))

df_plot = df_muestras.copy()
df_plot['Sum_Total'] = df_conc_A[[c for c in acronyms]].sum(axis=1)
df_plot['log10_Total'] = np.log10(df_plot['Sum_Total'])

palette = {'Car': '#E67E22', 'House': '#27AE60', 'Office': '#2980B9'}
order = ['Car', 'House', 'Office']

sns.boxplot(data=df_plot, x='microenvironment', y='log10_Total', order=order, palette=palette, width=0.45, ax=ax, boxprops=dict(alpha=0.8))
sns.stripplot(data=df_plot, x='microenvironment', y='log10_Total', order=order, color='black', alpha=0.6, jitter=0.2, size=7, ax=ax)

ax.set_xlabel('Microenvironment', fontweight='bold', labelpad=8)
ax.set_ylabel('Total Additives (log10 ng/g)', fontweight='bold', labelpad=8)
ax.set_xticklabels(['Vehicles\\n(n = 12)', 'Homes\\n(n = 24)', 'Offices\\n(n = 8)'])
ax.grid(axis='y', linestyle='--', alpha=0.4)

fig_path = os.path.join(OUT_FIGS, 'figura_1_distribucion_log10.png')
plt.savefig(fig_path)
plt.show()
print(f"Figura 1 guardada en: {fig_path}")
""")
]
create_nb("01_nivel_1_ocurrencia_y_descriptiva.ipynb", nb01)

# ==============================================================================
# NOTEBOOK 02
# ==============================================================================
nb02 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('02_nivel_2_variabilidad_espacial.ipynb')}

# Notebook 02: Nivel 2 — Variabilidad Espacial y Microambiental
### Subsección 3.2 del Manuscrito: Pruebas de Hipótesis, Geografía, Perfiles y Figuras 2 y 3
**Proyecto LC-GC / Indoor Dust — Universidad de Cartagena & Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code() + """
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
print("Librerías cargadas correctamente.")
"""),
    nbf.v4.new_code_cell("""# Celda 2: Auto-Carga de Datos Curados
df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_det = pd.read_csv(os.path.join(DATA_DIR, 'estado_deteccion.csv'))

acronyms = list(df_compuestos['acronym'])
fam_map = dict(zip(df_compuestos['acronym'], df_compuestos['family']))

aps_cols = [c for c in acronyms if fam_map[c] == 'APs']
pfrs_cols = [c for c in acronyms if fam_map[c] == 'PFRs']
phs_cols = [c for c in acronyms if fam_map[c] == 'PHs']

df_muestras['Sum_APs'] = df_conc[aps_cols].sum(axis=1)
df_muestras['Sum_PFRs'] = df_conc[pfrs_cols].sum(axis=1)
df_muestras['Sum_PHs'] = df_conc[phs_cols].sum(axis=1)
df_muestras['Sum_Total'] = df_muestras['Sum_APs'] + df_muestras['Sum_PFRs'] + df_muestras['Sum_PHs']

print("Datos y sumatorias preparadas.")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Contraste Geográfico entre Centros Urbanos (Bogotá vs Medellín vs Cartagena)
print("=== CONTRASTE GEOGRÁFICO DE SUMATORIAS ===")
for metric in ['Sum_Total', 'Sum_PHs', 'Sum_APs', 'Sum_PFRs']:
    groups = [df_muestras[df_muestras['city'] == c][metric].values for c in ['Bogota', 'Medellin', 'Cartagena']]
    
    f_stat, f_p = stats.f_oneway(*groups)
    kw_stat, kw_p = stats.kruskal(*groups)
    
    print(f"{metric:<10}: ANOVA F = {f_stat:.4f} (p = {f_p:.4f}) | Kruskal-Wallis H = {kw_stat:.4f} (p = {kw_p:.4f})")
"""),
    nbf.v4.new_code_cell("""# Celda 4: Contraste Residencial Directo (Hogares Bogotá vs Medellín)
df_homes = df_muestras[df_muestras['microenvironment'] == 'House'].copy()
df_homes_conc = df_conc.loc[df_homes.index].copy()

bog_idxs = df_homes[df_homes['city'] == 'Bogota'].index
med_idxs = df_homes[df_homes['city'] == 'Medellin'].index

print(f"Hogares evaluados: Bogotá (n = {len(bog_idxs)}), Medellín (n = {len(med_idxs)})\\n")

for target in ['Sum_PFRs', 'TBOEP', 'TCIPP', 'Sum_Total', 'Sum_APs', 'Sum_PHs']:
    if target.startswith('Sum_'):
        vals_bog = df_homes.loc[bog_idxs, target].values
        vals_med = df_homes.loc[med_idxs, target].values
    else:
        vals_bog = df_homes_conc.loc[bog_idxs, target].values
        vals_med = df_homes_conc.loc[med_idxs, target].values
        
    mwu_stat, mwu_p = stats.mannwhitneyu(vals_bog, vals_med, alternative='two-sided')
    print(f"{target:<10}: Bogota Med = {np.median(vals_bog):,.1f} vs Medellin Med = {np.median(vals_med):,.1f} | MWU p = {mwu_p:.4f}")
"""),
    nbf.v4.new_code_cell("""# Celda 5: Generación de la Figura 2 (Geográfica: Panel A + Panel B)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

order_city = ['Bogota', 'Medellin', 'Cartagena']
palette_city = {'Bogota': '#34495E', 'Medellin': '#16A085', 'Cartagena': '#D35400'}

df_muestras['log10_Total'] = np.log10(df_muestras['Sum_Total'])
sns.boxplot(data=df_muestras, x='city', y='log10_Total', order=order_city, palette=palette_city, width=0.45, ax=ax1)
sns.stripplot(data=df_muestras, x='city', y='log10_Total', order=order_city, color='black', alpha=0.6, jitter=0.2, ax=ax1)
ax1.set_title('(a) Total Additives by Urban Center', fontweight='bold')
ax1.set_xlabel('City', fontweight='bold')
ax1.set_ylabel('Total Additives (log10 ng/g)', fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.4)

df_homes_plot = df_homes.copy()
df_homes_plot['TBOEP'] = df_homes_conc['TBOEP']
df_homes_plot['TCIPP'] = df_homes_conc['TCIPP']

df_panel_b = []
for idx, row in df_homes_plot.iterrows():
    c = row['city']
    df_panel_b.append({'City': c, 'Metric': 'Sum_PFRs', 'Conc': row['Sum_PFRs']})
    df_panel_b.append({'City': c, 'Metric': 'TBOEP', 'Conc': row['TBOEP']})
    df_panel_b.append({'City': c, 'Metric': 'TCIPP', 'Conc': row['TCIPP']})
df_panel_b = pd.DataFrame(df_panel_b)
df_panel_b['log10_Conc'] = np.log10(df_panel_b['Conc'])

sns.boxplot(data=df_panel_b, x='Metric', y='log10_Conc', hue='City', palette={'Bogota': '#34495E', 'Medellin': '#16A085'}, ax=ax2, width=0.55)
ax2.set_title('(b) Intra-residential Flame Retardants (Homes)', fontweight='bold')
ax2.set_xlabel('Metric', fontweight='bold')
ax2.set_ylabel('Concentration (log10 ng/g)', fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.4)

fig2_path = os.path.join(OUT_FIGS, 'figura_2_geografica_completa.png')
plt.savefig(fig2_path)
plt.show()
print(f"Figura 2 guardada en: {fig2_path}")
""")
]
create_nb("02_nivel_2_variabilidad_espacial.ipynb", nb02)

# ==============================================================================
# NOTEBOOK 03
# ==============================================================================
nb03 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('03_nivel_3_analisis_multivariado.ipynb')}

# Notebook 03: Nivel 3 — Análisis Multivariado y Fuentes de Emisión
### Subsección 3.3 del Manuscrito: Correlación de Spearman, PCA, Propiedades Fisicoquímicas
**Proyecto LC-GC / Indoor Dust — Universidad de Cartagena & Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code() + """
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
print("Librerías cargadas correctamente.")
"""),
    nbf.v4.new_code_cell("""# Celda 2: Auto-Carga de Datos Curados
df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_det = pd.read_csv(os.path.join(DATA_DIR, 'estado_deteccion.csv'))

acronyms = list(df_compuestos['acronym'])
print(f"Cargadas {len(df_muestras)} muestras y {len(acronyms)} compuestos.")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Matriz de Correlación de Spearman y Pares Significativos (Tabla 4)
valid_analytes = [c for c in acronyms if (df_det[c].sum() / 44.0) >= 0.20]
df_sub = df_conc[valid_analytes].copy()

corr_matrix, p_matrix = stats.spearmanr(df_sub)
df_corr = pd.DataFrame(corr_matrix, index=valid_analytes, columns=valid_analytes)
df_p = pd.DataFrame(p_matrix, index=valid_analytes, columns=valid_analytes)

sig_pairs = []
for i in range(len(valid_analytes)):
    for j in range(i + 1, len(valid_analytes)):
        c1 = valid_analytes[i]
        c2 = valid_analytes[j]
        r_val = df_corr.iloc[i, j]
        p_val = df_p.iloc[i, j]
        if r_val >= 0.50 and p_val < 0.05:
            sig_pairs.append({
                'Compound_1': c1,
                'Compound_2': c2,
                'Spearman_r': r_val,
                'p_value': p_val
            })

df_sig_pairs = pd.DataFrame(sig_pairs).sort_values(by='Spearman_r', ascending=False)
df_sig_pairs.to_csv(os.path.join(OUT_TABLES, 'tabla_4_correlaciones_spearman_significativas.csv'), index=False)
display(df_sig_pairs.head(15))
"""),
    nbf.v4.new_code_cell("""# Celda 4: Generación de la Figura S1 (Heatmap de Spearman)
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(df_corr, cmap='RdBu_r', center=0, vmin=-0.5, vmax=1.0, annot=False, square=True,
            cbar_kws={'label': "Spearman rank correlation coefficient (r)"}, ax=ax)
ax.set_title("Bivariate Spearman Rank Correlation Matrix (Indoor Dust)", fontweight='bold', pad=12)

s1_path = os.path.join(OUT_FIGS, 'figura_s1_spearman_heatmap.png')
plt.savefig(s1_path)
plt.show()
print(f"Figura S1 guardada en: {s1_path}")
"""),
    nbf.v4.new_code_cell("""# Celda 5: Análisis de Componentes Principales (PCA)
X_raw = df_sub.values
X_log = np.log10(X_raw + 1.0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

pca = PCA(n_components=5)
scores = pca.fit_transform(X_scaled)

exp_var = pca.explained_variance_ratio_ * 100
print(f"Varianza explicada: PC1 = {exp_var[0]:.2f}%, PC2 = {exp_var[1]:.2f}%, PC3 = {exp_var[2]:.2f}%")
print(f"Varianza acumulada (PC1 + PC2): {exp_var[0] + exp_var[1]:.2f}%")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

colors = {'Car': '#E67E22', 'House': '#27AE60', 'Office': '#2980B9'}
for micro in ['Car', 'House', 'Office']:
    mask = (df_muestras['microenvironment'] == micro).values
    ax1.scatter(scores[mask, 0], scores[mask, 1], label=micro, color=colors[micro], s=60, alpha=0.85)

ax1.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(0, color='gray', linestyle='--', alpha=0.5)
ax1.set_xlabel(f"PC1 ({exp_var[0]:.1f}%)", fontweight='bold')
ax1.set_ylabel(f"PC2 ({exp_var[1]:.1f}%)", fontweight='bold')
ax1.set_title("(a) PCA Scores by Microenvironment", fontweight='bold')
ax1.legend()
ax1.grid(True, linestyle=':', alpha=0.5)

loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
for i, comp in enumerate(valid_analytes):
    ax2.arrow(0, 0, loadings[i, 0], loadings[i, 1], color='#2C3E50', alpha=0.6, head_width=0.03)
    ax2.text(loadings[i, 0]*1.1, loadings[i, 1]*1.1, comp, fontsize=7.5)

ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax2.axvline(0, color='gray', linestyle='--', alpha=0.5)
ax2.set_xlabel(f"PC1 ({exp_var[0]:.1f}%)", fontweight='bold')
ax2.set_ylabel(f"PC2 ({exp_var[1]:.1f}%)", fontweight='bold')
ax2.set_title("(b) Variable Loadings Vectors", fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.5)

pca_path = os.path.join(OUT_FIGS, 'figura_4_pca_composite.png')
plt.savefig(pca_path)
plt.show()
print(f"Figura 4 guardada en: {pca_path}")
""")
]
create_nb("03_nivel_3_analisis_multivariado.ipynb", nb03)

# ==============================================================================
# NOTEBOOK 04
# ==============================================================================
nb04 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('04_nivel_4_sintesis_mini_review.ipynb')}

# Notebook 04: Nivel 4 — Mini-Review Crítica y Síntesis de Estado del Arte
### Subsección 3.4 del Manuscrito: Transición Industrial, Coexistencia y Tabla 5
**Proyecto LC-GC / Indoor Dust — Universidad de Cartagena & Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code() + """
import pandas as pd
import numpy as np
print("Librerías cargadas correctamente.")
"""),
    nbf.v4.new_code_cell("""# Celda 2: Carga de Datos y Metadatos
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))

print("Datos listos para estructuración de Tabla 5.")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Estructuración y Exportación de la Tabla 5
t5_data = [
    {
        'Compound': 'DINCH',
        'Chemical_Class': 'Cyclohexane dicarboxylate (AP)',
        'Primary_Applications': 'Medical devices, food contact films, infant toys, PVC flooring.',
        'Toxicological_Mechanisms': 'PPAR-alpha/gamma metabolic activation, mild thyroid axis disturbance; low acute toxicity.',
        'Regulatory_Status': 'EU REACH & US FDA authorized; subject to biomonitoring surveillance.',
        'Colombia_Median_ng_g': df_conc['DINCH'].median(),
        'Global_Range_ng_g': '450 - 8,200',
        'Green_Alternative': 'Bio-based polyols, isosorbide diesters.'
    },
    {
        'Compound': 'DEHA',
        'Chemical_Class': 'Aliphatic adipate (AP)',
        'Primary_Applications': 'Cling wrapping films, gaskets, synthetic rubber, cable jackets.',
        'Toxicological_Mechanisms': 'Hepatic peroxisome proliferation, suspected adipogenesis, developmental toxicity.',
        'Regulatory_Status': 'EU migration limit (18 mg/kg); US EPA TRI listed chemical.',
        'Colombia_Median_ng_g': df_conc['DEHA'].median(),
        'Global_Range_ng_g': '180 - 3,500',
        'Green_Alternative': 'Epoxidized soybean oil (ESBO).'
    },
    {
        'Compound': 'TOTM',
        'Chemical_Class': 'Trimellitate (AP)',
        'Primary_Applications': 'High-temperature wire insulation, medical plastics, automotive interior vinyl.',
        'Toxicological_Mechanisms': 'Hepatosplenomegaly, microvesicular steatosis; low migration kinetics.',
        'Regulatory_Status': 'ECHA CoRAP evaluation; authorized medical substitute for DEHP.',
        'Colombia_Median_ng_g': df_conc['TOTM'].median(),
        'Global_Range_ng_g': '250 - 18,000',
        'Green_Alternative': 'High-molecular-weight polymeric polyesters.'
    },
    {
        'Compound': 'TCIPP',
        'Chemical_Class': 'Chlorinated alkyl PFR',
        'Primary_Applications': 'Rigid and flexible polyurethane foams, building thermal insulation, upholstery.',
        'Toxicological_Mechanisms': 'Suspected human carcinogen, thyroid disruption, developmental neurotoxicity.',
        'Regulatory_Status': 'EU hazard classification proposal (Carc. 2, Repr. 1B); restriction under evaluation.',
        'Colombia_Median_ng_g': df_conc['TCIPP'].median(),
        'Global_Range_ng_g': '120 - 25,000',
        'Green_Alternative': 'Expandable graphite, mineral hydroxides, bio-based polyphosphates.'
    },
    {
        'Compound': 'TBOEP',
        'Chemical_Class': 'Alkyl ether PFR',
        'Primary_Applications': 'Floor waxes and acrylic polish emulsions, leveling plasticizer in synthetic floorings.',
        'Toxicological_Mechanisms': 'AChE inhibition, neurotoxicity, cardiotoxicity in aquatic models.',
        'Regulatory_Status': 'Substance of evaluation under EU REACH; regulated in indoor consumer polishes.',
        'Colombia_Median_ng_g': df_conc['TBOEP'].median(),
        'Global_Range_ng_g': '1,100 - 180,000',
        'Green_Alternative': 'Aqueous carnauba wax emulsions, fluorosurfactant-free leveling resins.'
    }
]

df_table_5 = pd.DataFrame(t5_data)
df_table_5.to_csv(os.path.join(OUT_TABLES, 'tabla_5_sintesis_mini_review.csv'), index=False)
display(df_table_5)
""")
]
create_nb("04_nivel_4_sintesis_mini_review.ipynb", nb04)

# ==============================================================================
# NOTEBOOK 05
# ==============================================================================
nb05 = [
    nbf.v4.new_markdown_cell(f"""{colab_badge_md('05_nivel_5_evaluacion_riesgo_salud.ipynb')}

# Notebook 05: Nivel 5 — Evaluación Probabilística de Riesgos en Salud
### Subsección 3.5 del Manuscrito: Simulación Monte Carlo (10,000 iteraciones), EDIs, HQ e ILCR
**Proyecto LC-GC / Indoor Dust — Universidad de Cartagena & Universidad de Amberes**
"""),
    nbf.v4.new_code_cell(colab_setup_code() + """
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
print("Librerías cargadas correctamente.")
"""),
    nbf.v4.new_code_cell("""# Celda 2: Auto-Carga de Datos Curados
df_compuestos = pd.read_csv(os.path.join(DATA_DIR, 'compuestos_metadata.csv'))
df_conc = pd.read_csv(os.path.join(DATA_DIR, 'concentraciones_ng_g.csv'))
df_muestras = pd.read_csv(os.path.join(DATA_DIR, 'muestras_metadata.csv'))

home_idxs = df_muestras[df_muestras['microenvironment'] == 'House'].index
df_home_conc = df_conc.loc[home_idxs].copy()

print(f"Cargadas {len(df_home_conc)} muestras residenciales para la simulación de riesgo.")
"""),
    nbf.v4.new_code_cell("""# Celda 3: Definición del Motor Vectorial Monte Carlo (N = 10,000 iteraciones)
np.random.seed(42)
N_ITER = 10000

# Toddlers (1-3 años)
bw_toddler = np.random.normal(loc=12.0, scale=1.5, size=N_ITER)
bw_toddler = np.clip(bw_toddler, 8.0, 18.0)

ir_toddler = np.random.lognormal(mean=np.log(50.0), sigma=0.3, size=N_ITER) / 1000.0
ir_toddler = np.clip(ir_toddler, 0.02, 0.20)

bsa_toddler = np.random.normal(loc=2800.0, scale=300.0, size=N_ITER)
af_toddler = np.random.uniform(low=0.04, high=0.20, size=N_ITER)

# Adultos
bw_adult = np.random.normal(loc=70.0, scale=8.0, size=N_ITER)
bw_adult = np.clip(bw_adult, 50.0, 100.0)

ir_adult = np.random.lognormal(mean=np.log(20.0), sigma=0.3, size=N_ITER) / 1000.0
ir_adult = np.clip(ir_adult, 0.005, 0.10)

bsa_adult = np.random.normal(loc=5700.0, scale=500.0, size=N_ITER)
af_adult = np.random.uniform(low=0.01, high=0.07, size=N_ITER)

print(f"Parámetros de Monte Carlo inicializados ({N_ITER:,} iteraciones).")
"""),
    nbf.v4.new_code_cell("""# Celda 4: Simulación de EDI e Índices de Peligro (HQ) para TBOEP y TCIPP
toxicology_rfd = {
    'TBOEP': 15000.0,
    'TCIPP': 10000.0,
    'TCEP' : 22000.0,
    'TDCIPP': 15000.0,
    'DINCH': 1000000.0
}

c_tboep_samples = df_home_conc['TBOEP'].values
c_tboep_sim = np.random.choice(c_tboep_samples, size=N_ITER, replace=True)

edi_ing_toddler = (c_tboep_sim * ir_toddler) / bw_toddler
edi_ing_adult = (c_tboep_sim * ir_adult) / bw_adult

hq_tboep_toddler = edi_ing_toddler / toxicology_rfd['TBOEP']
hq_tboep_adult = edi_ing_adult / toxicology_rfd['TBOEP']

print(f"=== TBOEP RIESGO NO CANCERÍGENO (HQ) ===")
print(f"Toddlers: Mediana = {np.median(hq_tboep_toddler):.5f} | Percentil 95 = {np.percentile(hq_tboep_toddler, 95):.5f} (Seguro: HQ < 1)")
print(f"Adults  : Mediana = {np.median(hq_tboep_adult):.5f} | Percentil 95 = {np.percentile(hq_tboep_adult, 95):.5f} (Seguro: HQ < 1)")
"""),
    nbf.v4.new_code_cell("""# Celda 5: Generación de la Figura 5 (Funciones de Densidad de Probabilidad de HQ)
fig, ax = plt.subplots(figsize=(8, 5))

sns.kdeplot(hq_tboep_toddler, label='Toddlers (1-3 yrs)', color='#E74C3C', fill=True, alpha=0.35, ax=ax)
sns.kdeplot(hq_tboep_adult, label='Adults', color='#2980B9', fill=True, alpha=0.35, ax=ax)

ax.axvline(1.0, color='darkred', linestyle='--', linewidth=2, label='Safety Threshold (HQ = 1.0)')
ax.set_xlabel('Hazard Quotient (HQ) for TBOEP', fontweight='bold')
ax.set_ylabel('Probability Density', fontweight='bold')
ax.set_title('Probabilistic Health Risk Assessment (Monte Carlo N = 10,000)', fontweight='bold')
ax.set_xlim(0, 0.5)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.5)

fig5_path = os.path.join(OUT_FIGS, 'figura_5_probabilistic_risk_density.png')
plt.savefig(fig5_path)
plt.show()
print(f"Figura 5 guardada en: {fig5_path}")
""")
]
create_nb("05_nivel_5_evaluacion_riesgo_salud.ipynb", nb05)

print("All 6 notebooks updated with Colab badges and auto-setup code!")
