from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
import os
import logging

os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def extraer_contenido(ai_message):
    """ Extrae solo el texto del mensaje del LLM """
    return ai_message.content


def crear_chain_sequential():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

    # Prompt: RESUMIR
    prompt_resumen = PromptTemplate.from_template(
        "Resume el siguiente texto."
    "No expliques, no des contexto, no agregues comentarios. "
    "Devuelve únicamente el resumen.\n\nTexto:\n{input}"
    )

    # Prompt: TRADUCIR
    prompt_traduccion = PromptTemplate.from_template(
        "Traduce el siguiente texto al idioma '{idioma}':\n\n{texto}"
    )

    # Primer paso → RESUMEN
    chain_resumen = (
        prompt_resumen 
        | llm 
        | RunnableLambda(extraer_contenido)     # EXTRAEMOS SOLO EL TEXTO
    )

    # Segundo paso → TRADUCCIÓN
    chain_final = (
        {
            "texto": chain_resumen,            # ← Resumen limpio
            "idioma": RunnablePassthrough()    # ← Idioma que manda Qt
        }
        | prompt_traduccion
        | llm
    )

    return chain_final


if __name__ == "__main__":
    chain = crear_chain_sequential()
    result = chain.invoke({
        "input": "La IA está transformando la educación...",
        "idioma": "inglés"
    })
    print(result.content)