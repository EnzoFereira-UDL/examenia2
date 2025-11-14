# Contenido para: 1_llmchain.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging

# Silenciar mensajes de gRPC / Google
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_llmchain():
    """Crea un chain simple (Prompt + LLM)."""
    
    # Inicializar Google Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.4
    )
    
    # Crear el prompt
    prompt = PromptTemplate(
        input_variables=["tema"],
        template="Explícale a un niño el tema {tema}."
    )

    # Nueva forma (con tubería)
    chain = prompt | llm
    
    # La función DEVUELVE el chain listo
    return chain

#
# --- Bloque de prueba ---
# (Esto solo se ejecuta si corres "python 1_llmchain.py" directamente)
#
if __name__ == '__main__':
    print("Probando el 'Motor' 1: LLMChain...")
    
    # 1. Creamos el chain llamando a la función
    chain_de_prueba = crear_chain_llmchain()
    
    # 2. Ejecutamos la prueba
    respuesta = chain_de_prueba.invoke({"tema": "el aprendizaje automático"})
    
    # 3. Imprimimos el contenido (como lo tenías tú)
    print(respuesta.content)