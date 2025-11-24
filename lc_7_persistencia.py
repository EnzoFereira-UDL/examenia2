import os, json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# -- Archivo JSON donde se guardará la memoria --
MEMORY_FILE = "memoria.json"

# --- Memoria LangChain ---
memory = ConversationBufferMemory(return_messages=True)

# --- Guardar memoria en JSON ---
def guardar_memoria():
    data = memory.load_memory_variables({})
    history_text = []

    for msg in data.get("history", []):
        if hasattr(msg, "type") and hasattr(msg, "content"):
            history_text.append({"type": msg.type, "content": msg.content})

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"history": history_text}, f, ensure_ascii=False, indent=2)

# --- Cargar memoria desde JSON ---
def cargar_memoria():
    if not os.path.exists(MEMORY_FILE):
        return

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        for msg in data.get("history", []):
            if msg["type"] == "human":
                memory.chat_memory.add_user_message(msg["content"])
            elif msg["type"] == "ai":
                memory.chat_memory.add_ai_message(msg["content"])

# --- Ejecutar el modelo con memoria persistente ---
def ejecutar_con_memoria(texto):
    history = memory.load_memory_variables({}).get("history", [])
    chain = prompt | llm

    response = chain.invoke({"history": history, "input": texto})
    
    memory.save_context({"input": texto}, {"output": response.content})
    guardar_memoria()

    return response.content.strip()

# --- Configuración del modelo ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente amable que recuerda toda la conversación anterior."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# Cargar memoria previa si existe
cargar_memoria()

# -------------------------------
# 🟦 FUNCIÓN PARA CONECTAR A QT
# -------------------------------
class ChainPersistencia:
    def invoke(self, values):
        texto = values.get("input")
        return ejecutar_con_memoria(texto)

# Función que exporta el modelo (igual que los otros motores)
def crear_chain_persistencia():
    return ChainPersistencia()
