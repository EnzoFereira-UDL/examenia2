# Contenido para: 1_llmchain.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging

os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def crear_chain_llmchain():
    """Crea un chain simple (Prompt + LLM)."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4
    )

    # 🔥 CORREGIDO:
    # - input_variables en UNA sola lista
    # - "contexto" bien escrito
    # - prompt funcional
    prompt = PromptTemplate(
        input_variables=["tema", "contexto"],
        template="Usando el siguiente contexto:\n\n{contexto}\n\nExplica el tema: {tema}"
    )

    chain = prompt | llm
    return chain


if __name__ == '__main__':
    print("Probando el 'Motor' 1: LLMChain...")

    chain_de_prueba = crear_chain_llmchain()

    respuesta = chain_de_prueba.invoke({
        "tema": "el aprendizaje automático",
        "contexto": "Es un área de la inteligencia artificial"
    })

    print(respuesta.content)