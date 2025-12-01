# lc_5_varios_pasos.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
import os, logging


def crear_chain_varios_pasos():
    # Silenciar logs
    os.environ["GRPC_VERBOSITY"] = "NONE"
    os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
    logging.getLogger("absl").setLevel(logging.ERROR)
    logging.getLogger("grpc").setLevel(logging.ERROR)

    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # Prompt 1 → Resumen
    prompt_resumen = PromptTemplate.from_template(
        "Resume el siguiente texto."
    "No expliques, no des contexto, no agregues comentarios. "
    "Devuelve únicamente el resumen.\n\nTexto:\n{input}"
    )

    # Prompt 2 → Traducción
    prompt_traduccion = PromptTemplate.from_template(
        "Traduce el siguiente texto al {idioma}: {input}"
    )

    # Pipeline final correcto
    chain = (
        RunnableParallel(
            resumen = prompt_resumen | llm,
            idioma = RunnablePassthrough()
        )
        | (lambda entrada: {
            "input": entrada["resumen"].content,
            "idioma": entrada["idioma"]
        })
        | prompt_traduccion
        | llm
        | StrOutputParser()
    )

    return chain