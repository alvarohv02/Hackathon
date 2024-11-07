import os
import pandas as pd

# Ruta de la carpeta con los archivos CSV
carpeta_csv = '/Users/mazhihao/Documents/hackathon'

for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv'):  # Asegurarse de que solo procese archivos CSV
        ruta_csv = os.path.join(carpeta_csv, archivo)
        
        print(f"Procesando {archivo}...")

        try:
            df = pd.read_csv(ruta_csv)

            # Convertir a formato Markdown
            markdown = df.to_markdown(index=False)

            # Imprimir el resultado
            print(markdown)

            # Guardar el resultado en un archivo de texto
            nombre_salida = f'tabla_markdown_{os.path.splitext(archivo)[0]}.md'
            with open(nombre_salida, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            print(f"Archivo {archivo} convertido y guardado como {nombre_salida}")

        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
