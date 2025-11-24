# lc_4_parseo.py
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os
import logging

# Silenciar logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar API Key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def crear_chain_parseo():
    """
    Chain simple:
    Prompt → LLM → StrOutputParser
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

    prompt = PromptTemplate.from_template(
        "Resume el siguiente texto en una oración clara y concisa:\n\n{input}"
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser
    return chain


# Test opcional
if __name__ == "__main__":
    chain = crear_chain_parseo()
    resultado = chain.invoke("La inteligencia artificial está transformando la educación...")
    print(resultado)
