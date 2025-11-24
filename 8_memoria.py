import os
import json
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

# ==============================
# 1. Cargar API Key de Gemini
# ==============================
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ==============================
# 2. Leer PDF sin LangChain
# ==============================
pdf_path = "documentos/fuente.pdf"
reader = PdfReader(pdf_path)

pages = [page.extract_text() for page in reader.pages]
pages = [p for p in pages if p and p.strip()]

print(f"Documento cargado con {len(pages)} páginas")


# ==============================
# 3. Dividir texto (igual que RecursiveCharacterTextSplitter)
# ==============================
def split_text(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

docs = []
for p in pages:
    docs.extend(split_text(p))

print(f"Texto dividido en {len(docs)} fragmentos")


# ==============================
# 4. Embeddings locales (HuggingFace)
# ==============================
print("Cargando modelo embeddings...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ==============================
# 5. Crear o cargar índice FAISS
# ==============================
INDEX_PATH_VECTORS = "faiss_index_vectors.npy"
INDEX_PATH_DOCS = "faiss_index_docs.json"

def create_faiss_index():
    print("Creando índice FAISS...")

    embeddings = model.encode(docs, convert_to_numpy=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    np.save(INDEX_PATH_VECTORS, embeddings)

    with open(INDEX_PATH_DOCS, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    return index, docs, embeddings


def load_faiss_index():
    print("Cargando índice FAISS existente...")
    embeddings = np.load(INDEX_PATH_VECTORS)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    with open(INDEX_PATH_DOCS, "r", encoding="utf-8") as f:
        docs = json.load(f)

    return index, docs, embeddings


if os.path.exists(INDEX_PATH_VECTORS):
    index, docs, embeddings = load_faiss_index()
else:
    index, docs, embeddings = create_faiss_index()

print("FAISS listo.")


# ==============================
# 6. Función de recuperación (retriever)
# ==============================
def retrieve(query, k=3):
    q_emb = model.encode([query])
    distances, indices = index.search(q_emb, k)
    return [docs[i] for i in indices[0]]


# ==============================
# 7. Modelo LLM Gemini
# ==============================
llm = genai.GenerativeModel("gemini-2.5-flash")


# ==============================
# 8. Función preguntar (RAG)
# ==============================
def preguntar(pregunta):
    print(f"\n Pregunta: {pregunta}")

    context = retrieve(pregunta, k=3)

    prompt = f"""
Usa el siguiente contexto para responder.
Si no hay suficiente información, responde:
"No tengo información suficiente en el documento."

Contexto:
{context}

Pregunta:
{pregunta}

Respuesta:
"""

    respuesta = llm.generate_content(prompt)
    print("Respuesta:", respuesta.text.strip())


# ==============================
# Ejemplos
# ==============================
if __name__ == "__main__":
    preguntar("¿De qué trata el documento?")
    preguntar("¿Qué conclusiones se mencionan?")
