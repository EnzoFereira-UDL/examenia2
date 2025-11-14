#pip install langchain langchain-google-genai google-generativeai
#pip install python-dotenv

# Contenido para: main_historial.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

# 
# === ESTA ES LA FUNCIÓN QUE IMPORTARÁ TU GUI ===
#
def crear_modelo_historial():
    """
    Crea un chain de conversación con memoria 
    completa (recuerda todo).
    """
    
    # Cargar variables del archivo .env
    load_dotenv()

    # Obtener la clave API desde las variables de entorno
    api_key = os.getenv("GOOGLE_API_KEY")

    # Verifica que esté cargada
    if not api_key:
        raise ValueError("La variable GOOGLE_API_KEY no está definida en el archivo .env")

    # Crear el modelo LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=api_key
    )

    # Memoria para el historial de conversación (Buffer completo)
    memory = ConversationBufferMemory()

    # Cadena de conversación
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True 
    )
    
    # La función DEVUELVE el chain
    return conversation


# --- Bloque de prueba ---
# Esto solo se ejecuta si corres "python main_historial.py"
if __name__ == '__main__':
    print("Probando el modelo de 'Historial Completo'...")
    
    # 1. Creamos el modelo
    chain_de_prueba = crear_modelo_historial()
    
    # 2. Bucle de prueba
    print("Chat con Gemini (Historial Completo). Escribe 'salir' para terminar.\n")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit"]:
            break

        # Usamos .invoke()
        respuesta_dict = chain_de_prueba.invoke({"input": mensaje})
        print("Gemini:", respuesta_dict.get('response', 'Error'))