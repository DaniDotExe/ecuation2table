import pandas as pd
import re
from typing import List, Dict

def parse_search_equation(equation: str) -> pd.DataFrame:
    """
    Parsea una ecuación de búsqueda y la convierte en una tabla.
    Cada columna representa términos unidos por AND.
    Cada fila representa términos unidos por OR dentro de cada grupo AND.
    
    Args:
        equation (str): La ecuación de búsqueda con operadores AND/OR
        
    Returns:
        pd.DataFrame: Tabla con los términos organizados
    """
    
    # Limpiar la ecuación eliminando espacios extra
    equation = equation.strip()
    
    # Encontrar todos los grupos entre paréntesis que están unidos por AND
    # Patrón para capturar grupos entre paréntesis
    pattern = r'\([^()]+\)'
    and_groups = re.findall(pattern, equation)
    
    # Procesar cada grupo AND
    processed_groups = []
    for i, group in enumerate(and_groups):
        # Remover paréntesis
        group_content = group.strip('()')
        
        # Dividir por OR y limpiar cada término
        or_terms = []
        for term in group_content.split(' OR '):
            # Limpiar comillas y espacios
            clean_term = term.strip().strip('"\'')
            or_terms.append(clean_term)
        
        processed_groups.append({
            'group_name': f'AND_Group_{i+1}',
            'terms': or_terms
        })
    
    # Crear el DataFrame
    # Encontrar el máximo número de términos OR en cualquier grupo
    max_terms = max(len(group['terms']) for group in processed_groups)
    
    # Crear diccionario para el DataFrame
    data = {}
    for group in processed_groups:
        # Rellenar con valores vacíos si el grupo tiene menos términos
        terms = group['terms'] + [''] * (max_terms - len(group['terms']))
        data[group['group_name']] = terms
    
    df = pd.DataFrame(data)
    return df

def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Guarda el DataFrame en un archivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        filename (str): Nombre del archivo CSV
    """
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Tabla guardada en: {filename}")

def print_summary(df: pd.DataFrame):
    """
    Imprime un resumen de la tabla generada.
    
    Args:
        df (pd.DataFrame): DataFrame a resumir
    """
    print("=" * 60)
    print("RESUMEN DE LA ECUACIÓN PARSEADA")
    print("=" * 60)
    print(f"Número de grupos AND: {len(df.columns)}")
    print(f"Máximo de términos OR por grupo: {len(df)}")
    print("\nNúmero de términos por grupo:")
    for col in df.columns:
        non_empty = sum(1 for x in df[col] if x != '')
        print(f"  {col}: {non_empty} términos")
    print("=" * 60)

def main():
    """
    Función principal para ejecutar el parser.
    """
    # Pedir la ruta relativa del archivo al usuario
    print("=== CONVERTIDOR: ECUACIÓN → TABLA ===")
    print("Ingresa la ruta relativa del archivo con la ecuación de búsqueda")
    print("Ejemplo: bci.txt, data/search.txt, ../equations/query.txt")
    file_path = input("Ruta del archivo: ").strip()
    
    if not file_path:
        print("Error: Debes proporcionar una ruta de archivo")
        return
    
    # Convertir a ruta absoluta desde el directorio actual
    import os
    abs_file_path = os.path.abspath(file_path)
    
    # Leer la ecuación desde el archivo
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            equation = file.read().strip()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        print(f"Ruta absoluta buscada: {abs_file_path}")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    print("Ecuación original:")
    print(equation)
    print("\n")
    
    # Parsear la ecuación
    df = parse_search_equation(equation)
    
    # Mostrar resumen
    print_summary(df)
    
    # Mostrar la tabla
    print("\nTABLA GENERADA:")
    print("-" * 80)
    print(df.to_string(index=False))
    
    # Generar nombres de archivo de salida basados en el archivo de entrada
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Crear carpeta outputs si no existe
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_output = os.path.join(output_dir, f"{base_name}_table.csv")
    xlsx_output = os.path.join(output_dir, f"{base_name}_table.xlsx")
    
    # Guardar en CSV
    save_to_csv(df, csv_output)
    
    # Guardar versión Excel si es posible
    try:
        df.to_excel(xlsx_output, index=False)
        print(f"Tabla también guardada en Excel: {xlsx_output}")
    except ImportError:
        print("Nota: Para guardar en Excel, instala openpyxl: pip install openpyxl")

if __name__ == "__main__":
    main()
