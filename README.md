# Convertidor Ecuación ↔ Tabla

Este proyecto convierte ecuaciones de búsqueda booleanas en tablas estructuradas y viceversa.

## 🚀 Instalación y Configuración

### Opción 1: Usar el entorno virtual existente
```bash
# Activar el entorno virtual incluido
source .venv/bin/activate
```

### Opción 2: Replicar el entorno desde cero
```bash
# 1. Crear un nuevo entorno virtual
python3 -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate

# 3. Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

### Verificar instalación
```bash
# Verificar que pandas está instalado
python -c "import pandas; print('Pandas version:', pandas.__version__)"
python -c "import openpyxl; print('OpenPyXL instalado correctamente')"
```

## 📋 Dependencias

El proyecto requiere las siguientes librerías (incluidas en `requirements.txt`):

- **pandas** (2.3.2): Manipulación y análisis de datos
- **openpyxl** (3.1.5): Lectura y escritura de archivos Excel
- **numpy** (2.3.2): Operaciones numéricas (dependencia de pandas)

## 📋 Uso

### Convertir Ecuación → Tabla

```bash
python ecuacion2table.py
```

- El programa te pedirá la **ruta relativa** del archivo con la ecuación
- Ejemplos de rutas válidas:
  - `bci.txt`
  - `data/search.txt`
  - `../equations/query.txt`

**Salida:**
- `outputs/{nombre}_table.csv` - Tabla en formato CSV
- `outputs/{nombre}_table.xlsx` - Tabla en formato Excel

### Convertir Tabla → Ecuación

```bash
python table2ecuation.py
```

- El programa te pedirá la **ruta relativa** del archivo de tabla
- Formatos soportados: `.csv`, `.xlsx`, `.xls`
- Ejemplos de rutas válidas:
  - `data.csv`
  - `tables/results.xlsx`
  - `../data/search_table.csv`

**Salida:**
- `outputs/{nombre}_equation.txt` - Ecuación en una línea

### Script Unificado (Opcional)

```bash
# Ecuación → Tabla
python converter.py equation-to-table archivo.txt

# Tabla → Ecuación
python converter.py table-to-equation archivo.csv

# Ayuda
python converter.py --help
```

## 📊 Estructura de Datos

### Tabla
- **Columnas**: Grupos unidos por AND
- **Filas**: Términos unidos por OR dentro de cada grupo

### Ecuación
```
(term1 OR term2 OR term3) AND (term4 OR term5) AND (term6 OR term7 OR term8)
```

## 📁 Estructura del Proyecto

```
ecuation2table/
├── .venv/                    # Entorno virtual
├── outputs/                  # Carpeta de archivos generados (excluida en git)
├── requirements.txt          # Dependencias del proyecto
├── bci.txt                   # Archivo de ejemplo
├── ecuacion2table.py         # Convertidor ecuación → tabla
├── table2ecuation.py         # Convertidor tabla → ecuación
├── converter.py              # Script unificado
├── .gitignore                # Archivos excluidos del control de versiones
└── README.md                 # Este archivo
```

## 💡 Ejemplos

### Archivo de ecuación de entrada (bci.txt):
```
("brain computer interface*" OR BCI) AND ("machine learning" OR "deep learning") AND ("EEG" OR "electroencephalograph*")
```

### Tabla resultante:
| AND_Group_1 | AND_Group_2 | AND_Group_3 |
|-------------|-------------|-------------|
| brain computer interface* | machine learning | EEG |
| BCI | deep learning | electroencephalograph* |

### Ecuación regenerada:
```
("brain computer interface*" OR BCI) AND ("machine learning" OR "deep learning") AND (EEG OR electroencephalograph*)
```

## 🔧 Características

- ✅ **Rutas relativas**: Usa rutas desde el directorio actual
- ✅ **Múltiples formatos**: CSV, Excel, TXT
- ✅ **Preservación de estructura**: Mantiene la lógica booleana
- ✅ **Limpieza automática**: Maneja espacios y comillas
- ✅ **Estadísticas**: Muestra información detallada del procesamiento
- ✅ **Archivo requirements**: Fácil replicación del entorno
- ✅ **Una sola salida**: Genera únicamente el archivo de ecuación principal
- ✅ **Organización de archivos**: Todos los outputs en carpeta `outputs/`
- ✅ **Control de versiones**: Carpeta `outputs/` excluida del git

## 🔄 Replicación del Entorno

Para clonar este proyecto en otro sistema:

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd ecuation2table

# 2. Crear entorno virtual
python3 -m venv .venv

# 3. Activar entorno virtual
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar instalación
python -c "import pandas, openpyxl; print('Entorno configurado correctamente')"
```
