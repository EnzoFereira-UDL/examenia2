# Contenido para: main_memoria.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

def crear_modelo_chat_limitado():
    """
    Crea un modelo de conversación que SOLO recuerda
    los últimos 5 turnos de conversación.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable GOOGLE_API_KEY no está definida en .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )

    # === Memoria correctamente configurada ===
    memory = ConversationBufferWindowMemory(
        k=3,
        return_messages=True,
        input_key="human_input",
        output_key="ai_output"
    )

    # === Prompt controlado (NO concatena historial completo) ===
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template="""
            Eres un asistente útil y claro. Responde de manera directa y comprensible.
            Historial reciente: {history}
            Usuario: {human_input}
            Asistente:
        """
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        input_key="human_input",
        output_key="ai_output",
        verbose=False
    )

    return conversation


#
# === 3. EL BLOQUE DE PRUEBA (AQUÍ ESTÁ LA CORRECCIÓN) ===
#
if __name__ == '__main__':
    print("Probando el modelo de 'Chat Limitado (k=5)'...")
    
    chain_de_prueba = crear_modelo_chat_limitado()
    
    print("Chat con Gemini (Límite 5 PARES). Escribe 'salir' para terminar.\n")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() in ["salir", "exit"]:
            break

        #
        # ¡¡¡ESTA ES LA LÍNEA QUE ARREGLA TODO!!!
        # Usamos .invoke() que SÍ maneja la memoria.
        #
        respuesta_dict = chain_de_prueba.invoke({"input": mensaje})
        
        #
        # .invoke() devuelve un diccionario, 
        # la respuesta está en la clave 'response'
        #
        print("Gemini:", respuesta_dict.get('response', 'Error: No hubo respuesta'))