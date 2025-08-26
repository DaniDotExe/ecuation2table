import pandas as pd
import sys
from typing import List, Optional

def read_table_from_file(file_path: str) -> pd.DataFrame:
    """
    Lee una tabla desde un archivo CSV o Excel.
    
    Args:
        file_path (str):     print(f"\nEcuación guardada en: {equation_file}")

def convert_custom_operators(df: pd.DataFrame, group_op: str = "AND", term_op: str = "OR") -> str:rchivo CSV o Excel
        
    Returns:
        pd.DataFrame: DataFrame con los datos de la tabla
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Formato de archivo no soportado. Use CSV o Excel (.xlsx/.xls)")
        
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def clean_term(term: str) -> str:
    """
    Limpia un término individual, agregando comillas si contiene espacios.
    
    Args:
        term (str): Término a limpiar
        
    Returns:
        str: Término limpio y formateado
    """
    if pd.isna(term) or term == '':
        return None
    
    term = str(term).strip()
    
    # Si el término contiene espacios y no está ya entre comillas, agregar comillas
    if ' ' in term and not (term.startswith('"') and term.endswith('"')):
        term = f'"{term}"'
    
    return term

def table_to_equation(df: pd.DataFrame, group_operator: str = "AND", term_operator: str = "OR") -> str:
    """
    Convierte una tabla de términos en una ecuación de búsqueda.
    
    Args:
        df (pd.DataFrame): DataFrame con los términos organizados
        group_operator (str): Operador entre grupos (columnas) - por defecto "AND"
        term_operator (str): Operador entre términos (filas) - por defecto "OR"
        
    Returns:
        str: Ecuación de búsqueda formateada
    """
    
    groups = []
    
    for column in df.columns:
        # Obtener todos los términos no vacíos de la columna
        terms = []
        for value in df[column]:
            clean_value = clean_term(value)
            if clean_value:
                terms.append(clean_value)
        
        # Si hay términos en esta columna, crear el grupo
        if terms:
            if len(terms) == 1:
                # Si solo hay un término, no necesita paréntesis
                group = terms[0]
            else:
                # Si hay múltiples términos, unirlos con OR y agregar paréntesis
                group = f"({f' {term_operator} '.join(terms)})"
            
            groups.append(group)
    
    # Unir todos los grupos con AND
    if len(groups) == 1:
        equation = groups[0]
    else:
        equation = f" {group_operator} ".join(groups)
    
    return equation

def format_equation_pretty(equation: str, max_line_length: int = 100) -> str:
    """
    Formatea la ecuación de manera más legible con saltos de línea.
    
    Args:
        equation (str): Ecuación a formatear
        max_line_length (int): Longitud máxima de línea antes del salto
        
    Returns:
        str: Ecuación formateada con saltos de línea
    """
    # Dividir por AND para formatear cada grupo en una línea
    and_parts = equation.split(' AND ')
    
    formatted_parts = []
    for i, part in enumerate(and_parts):
        if i == 0:
            formatted_parts.append(part)
        else:
            formatted_parts.append(f"AND {part}")
    
    # Unir con saltos de línea si es muy largo
    if len(equation) > max_line_length:
        return ' \n'.join(formatted_parts)
    else:
        return equation

def save_equation_to_file(equation: str, file_path: str, pretty_format: bool = True):
    """
    Guarda la ecuación en un archivo de texto.
    
    Args:
        equation (str): Ecuación a guardar
        file_path (str): Ruta del archivo donde guardar
        pretty_format (bool): Si formatear la ecuación de manera legible
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            if pretty_format:
                formatted_equation = format_equation_pretty(equation)
                file.write(formatted_equation)
            else:
                file.write(equation)
        
        print(f"Ecuación guardada en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def print_statistics(df: pd.DataFrame):
    """
    Imprime estadísticas sobre la tabla procesada.
    
    Args:
        df (pd.DataFrame): DataFrame procesado
    """
    print("=" * 60)
    print("ESTADÍSTICAS DE LA TABLA")
    print("=" * 60)
    print(f"Número de grupos (columnas): {len(df.columns)}")
    print(f"Número máximo de términos por grupo: {len(df)}")
    
    print("\nTerminos por grupo:")
    total_terms = 0
    for col in df.columns:
        non_empty = sum(1 for x in df[col] if pd.notna(x) and str(x).strip() != '')
        total_terms += non_empty
        print(f"  {col}: {non_empty} términos")
    
    print(f"\nTotal de términos únicos: {total_terms}")
    print("=" * 60)

def main():
    """
    Función principal para ejecutar la conversión de tabla a ecuación.
    """
    # Pedir la ruta relativa del archivo al usuario
    print("=== CONVERTIDOR: TABLA → ECUACIÓN ===")
    
    # Configurar argumentos de línea de comandos o input del usuario
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("Ingresa la ruta relativa del archivo de tabla (CSV o Excel)")
        print("Ejemplo: data.csv, tables/results.xlsx, ../data/search_table.csv")
        input_file = input("Ruta del archivo: ").strip()
        
        if not input_file:
            print("Error: Debes proporcionar una ruta de archivo")
            return
    
    # Convertir a ruta absoluta desde el directorio actual
    import os
    abs_input_file = os.path.abspath(input_file)
    
    print(f"Procesando archivo: {input_file}")
    print(f"Ruta absoluta: {abs_input_file}")
    
    # Leer la tabla
    df = read_table_from_file(abs_input_file)
    if df is None:
        return
    
    print(f"\nTabla leída exitosamente:")
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    
    # Mostrar vista previa de la tabla
    print("\nVista previa de la tabla:")
    print("-" * 80)
    print(df.head(10).to_string(index=False))
    if len(df) > 10:
        print(f"... y {len(df) - 10} filas más")
    
    # Imprimir estadísticas
    print_statistics(df)
    
    # Convertir a ecuación
    equation = table_to_equation(df)
    
    print("\nECUACIÓN GENERADA:")
    print("-" * 80)
    print(equation)
    
    # Generar nombres de archivo de salida basados en el archivo de entrada
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Crear carpeta outputs si no existe
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    equation_file = os.path.join(output_dir, f"{base_name}_equation.txt")
    
    # Guardar archivo
    save_equation_to_file(equation, equation_file, pretty_format=False)
    
    print(f"\nEcuación guardada en: {equation_file}")

def convert_custom_operators(df: pd.DataFrame, group_op: str = "AND", term_op: str = "OR") -> str:
    """
    Función auxiliar para convertir con operadores personalizados.
    
    Args:
        df (pd.DataFrame): DataFrame con los términos
        group_op (str): Operador entre grupos
        term_op (str): Operador entre términos dentro de grupos
        
    Returns:
        str: Ecuación con operadores personalizados
    """
    return table_to_equation(df, group_operator=group_op, term_operator=term_op)

if __name__ == "__main__":
    main()
