# lc_6_memoria.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
import logging

# Silenciar logs molestos
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar API KEY
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Memoria real
memory = ConversationBufferMemory(return_messages=True)

# Prompt con historial
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil y recuerdas la conversación previa."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])


def ejecutar_con_memoria(texto):
    """Ejecuta el modelo conservando la memoria entre llamadas."""

    # Convertir historial interno → texto con formato:
    # Tú: ...
    # IA: ...
    historial_memoria = memory.load_memory_variables({}).get("history", [])

    historial_formateado = ""
    for mensaje in historial_memoria:
        if mensaje.type == "human":
            historial_formateado += f"Tú: {mensaje.content}\n"
        else:
            historial_formateado += f"IA: {mensaje.content}\n"

    # Chain minimalista
    chain = prompt | llm

    # Llamada al modelo
    response = chain.invoke({
    "history": [HumanMessage(content=historial_formateado)],
    "input": texto
    })

    # Guardar en memoria
    memory.save_context({"input": texto}, {"output": response.content})

    # Devolver solo el texto de la IA
    return response.content.strip()


# Función que será importada en la GUI
def crear_chain_memoria():
    return ejecutar_con_memoria