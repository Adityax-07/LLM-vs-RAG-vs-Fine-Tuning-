import os
import glob as glob_module
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "llama-3.1-8b-instant"

DOCS_PATH  = "data/docs"
PDFS_PATH  = "data/pdfs"
INDEX_PATH = "data/faiss_index"
EMBED_MODEL = "all-MiniLM-L6-v2"

SYSTEM_PROMPT = (
    "You are a programming tutor. Use only the provided context to answer. "
    "If the answer is not in the context, say 'I don't have that in my knowledge base.'"
)


def build_vectorstore() -> FAISS:
    # Load .txt documents
    print("Loading text documents...")
    loader = DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader,
                             loader_kwargs={"encoding": "utf-8"})
    documents = loader.load()
    print(f"  Loaded {len(documents)} text files.")

    # Load PDFs from data/pdfs/ if any exist
    pdf_files = glob_module.glob(os.path.join(PDFS_PATH, "**/*.pdf"), recursive=True)
    for pdf_path in pdf_files:
        try:
            pdf_loader = PyPDFLoader(pdf_path)
            documents.extend(pdf_loader.load())
            print(f"  Loaded PDF: {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"  Warning: Could not load {pdf_path}: {e}")

    print(f"Total documents loaded: {len(documents)} ({len(pdf_files)} PDFs)")

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_PATH)
    print(f"Vector store saved to {INDEX_PATH}/")
    return vectorstore


def load_vectorstore() -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)


def ask_rag(question: str, vectorstore: FAISS) -> dict:
    start = time.time()

    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the following context to answer the question accurately.

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    elapsed = round(time.time() - start, 2)
    answer = response.choices[0].message.content.strip()

    return {
        "system": "RAG",
        "question": question,
        "answer": answer,
        "context_used": context,
        "response_time": elapsed,
    }


if __name__ == "__main__":
    if not os.path.exists(INDEX_PATH):
        vs = build_vectorstore()
    else:
        print("Loading existing vector store...")
        vs = load_vectorstore()

    test_q = "What is binary search?"
    print(f"\nQuestion: {test_q}\n")
    result = ask_rag(test_q, vs)
    print(f"Answer:\n{result['answer']}")
    print(f"\nContext used:\n{result['context_used'][:300]}...")
    print(f"\nResponse time: {result['response_time']}s")
