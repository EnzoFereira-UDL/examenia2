# lc_8_rag.py

import os
from dotenv import load_dotenv

import numpy as np
from pypdf import PdfReader
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

EMBED_MODEL = "models/text-embedding-004"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
    google_api_key=API_KEY,
)

PDF_PATH = "documentos/fuente.pdf"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def _leer_pdf(path: str) -> str:
    reader = PdfReader(path)
    textos = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(textos)

def _dividir_en_chunks(texto: str):
    chunks = []
    paso = CHUNK_SIZE - CHUNK_OVERLAP
    for i in range(0, len(texto), paso):
        ch = texto[i:i + CHUNK_SIZE]
        if ch.strip():
            chunks.append(ch)
    return chunks

_texto_pdf = _leer_pdf(PDF_PATH)
_chunks = _dividir_en_chunks(_texto_pdf)

def _embed_text(text: str):
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=text,
        task_type="retrieval_document",
    )
    return np.array(resp["embedding"], dtype=float)

_chunk_embeddings = []
for ch in _chunks:
    _chunk_embeddings.append(_embed_text(ch))
_chunk_embeddings = np.vstack(_chunk_embeddings)
_chunk_embeddings = _chunk_embeddings / np.maximum(
    np.linalg.norm(_chunk_embeddings, axis=1, keepdims=True),
    1e-8
)

def _buscar_contexto(pregunta: str, k: int = 3):
    q_vec = _embed_text(pregunta)
    q_vec = q_vec / max(np.linalg.norm(q_vec), 1e-8)
    sims = _chunk_embeddings @ q_vec
    idx = sims.argsort()[::-1][:k]
    return "\n\n---\n\n".join(_chunks[i] for i in idx)

def preguntar_rag(pregunta: str) -> str:
    pregunta = pregunta.strip()
    if not pregunta:
        return "Escribe una pregunta."

    try:
        contexto = _buscar_contexto(pregunta, k=3)
        prompt = (
            "Usa exclusivamente la siguiente información del documento para responder.\n"
            "Si no encuentras la respuesta, responde exactamente:\n"
            "\"No tengo información suficiente en el documento.\"\n\n"
            f"Contexto:\n{contexto}\n\n"
            f"Pregunta: {pregunta}\n\n"
            "Respuesta:"
        )
        resp = llm.invoke(prompt)
        return (resp.content or "").strip()

    except Exception as e:
        return f"Ocurrió un error al consultar el documento: {e}"

# ------------------------------------------------------------------
# 🔥 FUNCIÓN QUE DEBE USAR LA VENTANA PRINCIPAL
# ------------------------------------------------------------------
def crear_chain_rag():
    return preguntar_rag