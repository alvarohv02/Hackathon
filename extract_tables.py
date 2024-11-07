from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas as pd
import csv

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

# Creamos una lista para almacenar DataFrames de cada tabla
dataframes = []

# Recorremos cada tabla en el resultado
for table_idx, table in enumerate(result.tables):
    print(f"Procesando la Tabla #{table_idx} con {table.row_count} filas y {table.column_count} columnas")
    
    # Creamos una matriz vacía para la tabla, con dimensiones filas x columnas
    table_data = [['' for _ in range(table.column_count)] for _ in range(table.row_count)]
    
    # Recorremos las celdas de la tabla y colocamos el contenido en la posición correcta
    for cell in table.cells:
        # Concatenamos el contenido de las celdas en la misma posición
        if table_data[cell.row_index][cell.column_index]:
            table_data[cell.row_index][cell.column_index] += ' ' + cell.content
        else:
            table_data[cell.row_index][cell.column_index] = cell.content
    
    # Convertimos la matriz en un DataFrame
    df = pd.DataFrame(table_data)
    dataframes.append(df)
    
    # Mostrar el DataFrame resultante (opcional)
    print(f"DataFrame de la Tabla #{table_idx}:\n{df}\n")

# Guardar cada DataFrame en un archivo CSV
for idx, df in enumerate(dataframes):
    filename = f"magna_csv/tabla_{idx}.csv"
    df.to_csv(filename, index=False)
    print(f"DataFrame de la Tabla #{idx} guardado como {filename}")

