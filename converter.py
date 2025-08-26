#!/usr/bin/env python3
"""
Utilidad para convertir entre ecuaciones de búsqueda y tablas.

Uso:
    python converter.py equation-to-table <archivo_ecuacion.txt>
    python converter.py table-to-equation <archivo_tabla.csv/.xlsx>
    python converter.py --help
"""

import sys
import os
from pathlib import Path

# Importar nuestros módulos personalizados
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    import ecuacion2table as eq_parser
    import table2ecuation as t2e
    import pandas as pd
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de tener pandas instalado: pip install pandas openpyxl")
    sys.exit(1)

def equation_to_table(equation_file: str, output_prefix: str = None):
    """
    Convierte una ecuación de búsqueda a tabla.
    
    Args:
        equation_file (str): Archivo con la ecuación de búsqueda
        output_prefix (str): Prefijo para los archivos de salida
    """
    try:
        # Leer ecuación
        with open(equation_file, 'r', encoding='utf-8') as file:
            equation = file.read().strip()
        
        print(f"📄 Procesando ecuación desde: {equation_file}")
        print(f"📏 Longitud de la ecuación: {len(equation)} caracteres")
        
        # Parsear ecuación
        df = eq_parser.parse_search_equation(equation)
        
        # Generar nombres de archivo de salida
        if output_prefix is None:
            base_name = Path(equation_file).stem
            output_prefix = f"{base_name}_table"
        
        # Crear carpeta outputs si no existe
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        csv_file = output_dir / f"{output_prefix}.csv"
        xlsx_file = output_dir / f"{output_prefix}.xlsx"
        
        # Guardar archivos
        eq_parser.save_to_csv(df, str(csv_file))
        
        try:
            df.to_excel(str(xlsx_file), index=False)
            print(f"📊 Tabla Excel guardada: {xlsx_file}")
        except ImportError:
            print("⚠️  Para Excel instala: pip install openpyxl")
        
        # Mostrar resumen
        eq_parser.print_summary(df)
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {equation_file}")
        return None
    except Exception as e:
        print(f"❌ Error al procesar: {e}")
        return None

def table_to_equation_converter(table_file: str, output_prefix: str = None):
    """
    Convierte una tabla a ecuación de búsqueda.
    
    Args:
        table_file (str): Archivo CSV o Excel con la tabla
        output_prefix (str): Prefijo para los archivos de salida
    """
    try:
        print(f"📊 Procesando tabla desde: {table_file}")
        
        # Leer tabla
        df = t2e.read_table_from_file(table_file)
        if df is None:
            return None
        
        print(f"📐 Dimensiones de la tabla: {df.shape[0]} filas x {df.shape[1]} columnas")
        
        # Generar nombres de archivo de salida
        if output_prefix is None:
            base_name = Path(table_file).stem
            output_prefix = f"{base_name}_equation"
        
        # Crear carpeta outputs si no existe
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        equation_file = output_dir / f"{output_prefix}.txt"
        
        # Convertir a ecuación
        equation = t2e.table_to_equation(df)
        
        # Guardar archivo
        t2e.save_equation_to_file(equation, str(equation_file), pretty_format=False)
        
        # Mostrar estadísticas
        t2e.print_statistics(df)
        
        print(f"\n📝 Ecuación generada ({len(equation)} caracteres):")
        print("=" * 80)
        print(equation[:200] + "..." if len(equation) > 200 else equation)
        
        return equation
        
    except Exception as e:
        print(f"❌ Error al procesar: {e}")
        return None

def show_help():
    """Muestra la ayuda del programa."""
    help_text = """
🔄 CONVERTIDOR ECUACIÓN ↔ TABLA

DESCRIPCIÓN:
    Herramienta para convertir entre ecuaciones de búsqueda booleanas y tablas estructuradas.

USO:
    python converter.py equation-to-table <archivo_ecuacion.txt> [output_prefix]
    python converter.py table-to-equation <archivo_tabla.csv/.xlsx> [output_prefix]
    python converter.py --help

COMANDOS:
    equation-to-table    Convierte ecuación → tabla (CSV + Excel)
    table-to-equation    Convierte tabla → ecuación (TXT + formateado)
    --help              Muestra esta ayuda

EJEMPLOS:
    python converter.py equation-to-table bci.txt
    python converter.py table-to-equation bci_table.csv
    python converter.py equation-to-table search.txt my_output

FORMATOS SOPORTADOS:
    📥 Entrada: .txt (ecuaciones), .csv, .xlsx, .xls (tablas)
    📤 Salida: .csv, .xlsx (tablas), .txt (ecuaciones)

ESTRUCTURA:
    📊 Tablas: Columnas = grupos AND, Filas = términos OR
    📝 Ecuaciones: (term1 OR term2) AND (term3 OR term4) AND ...
"""
    print(help_text)

def main():
    """Función principal del programa."""
    if len(sys.argv) < 2:
        print("❌ Error: Se requieren argumentos")
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command in ['--help', '-h', 'help']:
        show_help()
        return
    
    if command == 'equation-to-table':
        if len(sys.argv) < 3:
            print("❌ Error: Se requiere el archivo de ecuación")
            print("Uso: python converter.py equation-to-table <archivo_ecuacion.txt>")
            sys.exit(1)
        
        equation_file = sys.argv[2]
        output_prefix = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = equation_to_table(equation_file, output_prefix)
        if result is not None:
            print("✅ Conversión completada exitosamente")
        
    elif command == 'table-to-equation':
        if len(sys.argv) < 3:
            print("❌ Error: Se requiere el archivo de tabla")
            print("Uso: python converter.py table-to-equation <archivo_tabla.csv/.xlsx>")
            sys.exit(1)
        
        table_file = sys.argv[2]
        output_prefix = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = table_to_equation_converter(table_file, output_prefix)
        if result is not None:
            print("✅ Conversión completada exitosamente")
        
    else:
        print(f"❌ Error: Comando '{command}' no reconocido")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
