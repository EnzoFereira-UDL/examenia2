import google.generativeai as genai
import os

# Pega tu API KEY aquí directamente para probar, o usa os.getenv
genai.configure(api_key="AIzaSyBfnNaBk1QSKKerwc_4xuWxip34Ke0VgFA")

print("Listando modelos disponibles...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)