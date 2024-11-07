import os
import csv
import json
import re
import pandas as pd
from openai import AzureOpenAI # Si no está la librería instalada, hacer un pip install openai

# Creamos una instancia de cliente de AzureOpenAI
client = AzureOpenAI(
  azure_endpoint = "https://openaicore-sweden.openai.azure.com/", # El endpoint a usar lo daremos al inicio de la competición
  api_key="16o1yakHz3FgF75l9xWKeHiOPXCf6XzOHFXK5oCnjyCPhrwbdj7eJQQJ99AKACfhMk5XJ3w3AAABACOGuvUA",  # La clave también os la daremos al comenzar la competición
  api_version="2024-02-15-preview"
)

criterios = "C02 emissions, water waste, energy intensity, waste recycled, atmospheric emissions, accidents frequency, employees recruitments, women participation, disabilities, bussines ethics"
carpeta = '/Users/mazhihao/Documents/hackathon/Stellantis'
carpeta_lista = os.listdir(carpeta)

for archivo in carpeta_lista:
    with open(f"Stellantis/{archivo}", "r") as f1:
        file1 = f1.read()
        prompt = f"If the data from {file1}\n\n is related to {criterios} and the data must be relevant especially if it has numbers and easy comparable. Give me only one answer: Yes or Not. Only Only one answer "
        message_text = [
            {"role":"system","content":"You are an AI assistant that helps people classify information."},
            {"role":"user","content":"Who are you?"},
            {"role":"assistant","content":"I am an AI digital assistant designed to help people find information, answer questions, and perform a variety of tasks through text-based interactions. My purpose is to assist you with any inquiries you might have to the best of my ability, using the information available up to my last update"},
            {"role":"user","content":prompt},] # Éste último mensaje de usuario es el que será respondido
        
        completion = client.chat.completions.create(
            model="gpt-4-turbo", # IMPORTANTE: aquí hay que poner el nombre del DEPLOYMENT a usar: model = "deployment_name"
            messages = message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        boleano = completion.choices[0].message.content
        if boleano.startswith("n") or  boleano.startswith("N"):
            os.remove(f"Stellantis/{archivo}")
            


"""
message_text = [
    {"role":"system","content":"You are an AI assistant that helps people find information."},
    {"role":"user","content":"Who are you?"},
    {"role":"assistant","content":"I am an AI digital assistant designed to help people find information, answer questions, and perform a variety of tasks through text-based interactions. My purpose is to assist you with any inquiries you might have to the best of my ability, using the information available up to my last update"},
    {"role":"user","content":"Are you gay?"},] # Éste último mensaje de usuario es el que será respondido

# Se debe fijar un contexto máximo en términos de número de mensajes a pasar al modelo, por ejemplo 10.


completion = client.chat.completions.create(
  model="gpt-4-turbo", # IMPORTANTE: aquí hay que poner el nombre del DEPLOYMENT a usar: model = "deployment_name"
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)

print(completion.to_json)"""