from groq import Groq
from dotenv import load_dotenv
import os

class ModeloOpenAI:
    def __init__(self):
        pass

def modeloSimple(self):
    load_dotenv()
    cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))
    respuesta = cliente.chat.completions.create(model='llama-3.1-8b-instant',
                                                messages=[{'role':'user',
                                                           'content':'crea un resumen de la pelicula gigantes de acero'}])

    print(respuesta.choices[0].message.content)