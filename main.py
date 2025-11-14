# Contenido para: main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# 
# === ESTA ES LA FUNCIÓN QUE IMPORTARÁ TU GUI ===
#
def crear_modelo_simple():
    """
    Crea un chain simple que actúa como poeta,
    sin memoria.
    """
    
    # Cargar variables del archivo .env
    load_dotenv()

    # Obtener la clave API
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("La variable GOOGLE_API_KEY no está definida en el archivo .env")

    # Crear el modelo LLM (esto ya lo tenías)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )
    
    # En lugar de invocarlo, creamos un "template"
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente de IA, que busca ayudar al usuario"),
        ("human", "{input}") # ¡Aquí entrará el texto del botón!
    ])
    
    output_parser = StrOutputParser()

    # Creamos el "motor" (chain)
    chain = prompt | llm | output_parser
    
    # La función DEVUELVE el motor, no lo ejecuta
    return chain

# --- Bloque de prueba (esto no lo usa la GUI) ---
if __name__ == '__main__':
    print("Probando el modelo 'Simple'...")
    chain_de_prueba = crear_modelo_simple()
    
    print("Escribe (o 'salir'):\n")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit"]:
            break

        # Aquí sí lo invocamos, pero con el input del usuario
        respuesta = chain_de_prueba.invoke({"input": mensaje})
        print("Poeta:", respuesta)