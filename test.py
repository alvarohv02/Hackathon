from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "https://westeurope.api.cognitive.microsoft.com/"
key = "778cd3003d86499e82d67db670bbbc36"

# sample document
formUrl = "https://www.forvia.com/sites/default/files/2024-03/FORVIA_%202023_Sustainability%20Report_WEB.pdf"

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", document_url=formUrl)
result = poller.result()

for idx, style in enumerate(result.styles):
    print(
        "Document contains {} content".format(
         "handwritten" if style.is_handwritten else "no handwritten"
        )
    )

# for page in result.pages:
#     for line_idx, line in enumerate(page.lines):
#         print(
#          "...Line # {} has text content '{}'".format(
#         line_idx,
#         line.content.encode("utf-8")
#         )
#     )

#     for selection_mark in page.selection_marks:
#         print(
#          "...Selection mark is '{}' and has a confidence of {}".format(
#          selection_mark.state,
#          selection_mark.confidence
#          )
#     )

# for table_idx, table in enumerate(result.tables):
#     print(
#         "Table # {} has {} rows and {} columns".format(
#         table_idx, table.row_count, table.column_count
#         )
#     )
        
#     for cell in table.cells:
#         print(
#             "...Cell[{}][{}] has content '{}'".format(
#             cell.row_index,
#             cell.column_index,
#             cell.content.encode("utf-8"),
#             )
#         )

import pandas as pd
import csv
from openpyxl import load_workbook

# Creamos una lista para almacenar DataFrames de cada tabla
dataframes = []

# # Recorremos cada tabla en el resultado
# for table_idx, table in enumerate(result.tables):
#     print(f"Procesando la Tabla #{table_idx} con {table.row_count} filas y {table.column_count} columnas")
    
#     # Inicializamos una lista para almacenar las filas de la tabla
#     rows = [[] for _ in range(table.row_count)]
    
#     # Recorremos las celdas de la tabla para llenar las filas y columnas
#     for cell in table.cells:
#         # Añadimos el contenido de la celda en su posición de fila y columna
#         rows[cell.row_index].append(cell.content)
    
#     # Convertimos la lista de filas a un DataFrame
#     df = pd.DataFrame(rows)
#     dataframes.append(df)  # Agregamos el DataFrame a la lista de tablas
    
#     # Opcional: Mostrar el DataFrame de la tabla
#     print(f"DataFrame de la Tabla #{table_idx}:\n{df}\n")

# # Si necesitas acceder a cada DataFrame de forma independiente:
# # dataframes[0], dataframes[1], etc.

# # Si quieres combinar todas las tablas en un solo DataFrame (solo si tienen las mismas columnas):
# # combined_df = pd.concat(dataframes, ignore_index=True)

# # Guardar cada DataFrame en un archivo CSV
# for idx, df in enumerate(dataframes):
#     # Definimos el nombre del archivo para cada tabla
#     filename = f"tabla_{idx}.csv"
    
#     # Guardamos el DataFrame como CSV
#     df.to_csv(filename, index=False)
    
#     print(f"DataFrame de la Tabla #{idx} guardado como {filename}")

# Lista para almacenar DataFrames de cada tabla
dataframes = []

# Recorremos cada tabla en el resultado
for table_idx, table in enumerate(result.tables):
    print(f"Procesando la Tabla #{table_idx} con {table.row_count} filas y {table.column_count} columnas")
    
    # Creamos una matriz vacía para la tabla, con dimensiones filas x columnas
    table_data = [['' for _ in range(table.column_count)] for _ in range(table.row_count)]
    
    # Recorremos las celdas de la tabla y colocamos el contenido en la posición correcta
    for cell in table.cells:
        table_data[cell.row_index][cell.column_index] = cell.content
    
    # Convertimos la matriz en un DataFrame
    df = pd.DataFrame(table_data)
    dataframes.append(df)
    
    # Mostrar el DataFrame resultante (opcional)
    print(f"DataFrame de la Tabla #{table_idx}:\n{df}\n")

# Guardar cada DataFrame en un archivo CSV
for idx, df in enumerate(dataframes):
    filename = f"tabla_{idx}.csv"
    df.to_csv(filename, index=False)
    print(f"DataFrame de la Tabla #{idx} guardado como {filename}")