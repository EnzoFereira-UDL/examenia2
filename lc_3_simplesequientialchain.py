# lc_3_simplesequentialchain.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
import os
import logging

os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar clave
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def extraer_contenido(msg):
    """ Convierte AIMessage → texto limpio """
    return msg.content

def crear_chain_simple():
    """
    Chain simple: Resume → Traduce
    El idioma será dinámico desde Qt.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

    # 1. Prompt para RESUMIR
    prompt_resumen = PromptTemplate.from_template(
        "Resume el siguiente texto."
    "No expliques, no des contexto, no agregues comentarios. "
    "Devuelve únicamente el resumen.\n\nTexto:\n{input}"
    )

    # 2. Prompt para TRADUCIR
    prompt_traduccion = PromptTemplate.from_template(
        "Traduce el siguiente texto al idioma '{idioma}':\n\n{texto}"
    )

    # Chain paso 1 → resumen
    chain_resumen = (
        prompt_resumen |
        llm |
        RunnableLambda(extraer_contenido)   # limpiar texto
    )

    # Chain paso 2 → traducción
    chain_final = (
        {
            "texto": chain_resumen,       # resultado del resumen
            "idioma": RunnablePassthrough()
        }
        | prompt_traduccion
        | llm
    )

    return chain_final


# Test individual
if __name__ == "__main__":
    chain = crear_chain_simple()
    result = chain.invoke({
        "input": "La IA está cambiando la educación...",
        "idioma": "inglés"
    })
    print(result.content)