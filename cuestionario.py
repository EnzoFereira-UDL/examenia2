# lc_8_rag.py
import os
import re
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

class GeneradorCuestionario:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", # Usamos flash por su gran ventana de contexto
            temperature=0.3, # Baja temperatura para ser preciso con las respuestas
            google_api_key=API_KEY,
        )
        self.respuestas_correctas = [] # Aquí guardaremos la clave (Ej: ['A', 'B', 'C', 'A', 'D'])
        self.preguntas_texto = ""      # Aquí guardamos el texto para mostrar al usuario

    def procesar_pdf_y_generar_preguntas(self, pdf_path):
        """Lee el PDF y genera las preguntas y la hoja de respuestas."""
        try:
            # 1. Leer PDF
            reader = PdfReader(pdf_path)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text() or ""
            
            # Limitar caracteres si es excesivamente grande (opcional, aprox 30k tokens)
            texto_completo = texto_completo[:100000] 

            # 2. Prompt diseñado para separar Preguntas de Respuestas
            prompt = (
                "Eres un profesor experto. Basado en el siguiente texto, genera un examen de 5 preguntas "
                "de opción múltiple (A, B, C, D).\n\n"
                "REGLAS DE FORMATO:\n"
                "1. Primero escribe las 5 preguntas claramente.\n"
                "2. Usa el separador exacto '---CLAVE_RESPUESTAS---' al final de las preguntas.\n"
                "3. Después del separador, escribe SOLO las letras correctas separadas por comas (Ejemplo: A,C,D,B,A).\n\n"
                f"TEXTO BASE:\n{texto_completo}\n\n"
                "Genera el examen:"
            )

            # 3. Invocar modelo
            resultado = self.llm.invoke(prompt)
            contenido = resultado.content

            # 4. Procesar respuesta (Separar Preguntas de Clave)
            if "---CLAVE_RESPUESTAS---" in contenido:
                partes = contenido.split("---CLAVE_RESPUESTAS---")
                self.preguntas_texto = partes[0].strip()
                clave_raw = partes[1].strip()
                
                # Limpiar la clave para tener una lista limpia ['A', 'B', ...]
                # Busca letras A-D ignorando espacios o puntos
                self.respuestas_correctas = re.findall(r'[A-D]', clave_raw.upper())
            else:
                # Fallback por si el modelo no respeta el formato
                self.preguntas_texto = contenido
                self.respuestas_correctas = []
            
            return True, self.preguntas_texto

        except Exception as e:
            return False, f"Error al procesar PDF: {str(e)}"

    def evaluar_respuestas(self, respuestas_usuario_str):
        """
        Compara las respuestas del usuario (string) con las correctas.
        Ejemplo input usuario: "a, b, c, a, d"
        """
        if not self.respuestas_correctas:
            return "Error: No hay respuestas correctas cargadas. Genere el cuestionario primero."

        # Limpiar input usuario
        respuestas_usuario = re.findall(r'[A-D]', respuestas_usuario_str.upper())

        if len(respuestas_usuario) != 5:
            return f"Error: Detecté {len(respuestas_usuario)} respuestas. Por favor ingresa 5 letras (A, B, C, D) separadas por comas."

        # Calcular puntaje
        aciertos = 0
        detalle = ""
        
        for i, (user, correct) in enumerate(zip(respuestas_usuario, self.respuestas_correctas)):
            num = i + 1
            if user == correct:
                aciertos += 1
                detalle += f"P{num}: Correcta ({user})\n"
            else:
                detalle += f"P{num}: Incorrecta (Tú: {user} | Correcta: {correct})\n"

        porcentaje = (aciertos / 5) * 100
        
        resultado_final = (
            f"Resultados del Examen:\n"
            f"----------------------\n"
            f"Calificación: {porcentaje}%\n"
            f"Aciertos: {aciertos}/5\n\n"
            f"Detalle:\n{detalle}"
        )
        return resultado_final

# Función factory para instanciar en la ventana principal
def crear_chain_rag2():
    return GeneradorCuestionario()