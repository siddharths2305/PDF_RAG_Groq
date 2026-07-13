import os
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="PDF Chatbot with Groq",
    layout="wide"
)

st.title("📄 PDF Chatbot using Groq + FAISS")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Settings")

groq_api_key = st.sidebar.text_input(
    "Groq API Key",
    value=os.getenv("GROQ_API_KEY", ""),
    type="password"
)

model_name = st.sidebar.selectbox(
    "Groq Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
)

# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None and st.session_state.vectorstore is None:

    with st.spinner("Processing PDF..."):

        pdf_path = None

        try:
            # Save uploaded PDF
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            # Load PDF
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            st.write(f"📄 Pages Loaded: {len(docs)}")

            if len(docs) == 0:
                st.error("No pages found in PDF.")
                st.stop()

            # Debug first pages
            for i, doc in enumerate(docs[:3]):
                st.write(
                    f"📄 Page {i+1} length: {len(doc.page_content)} characters"
                )

                if len(doc.page_content) > 0:
                    st.write(doc.page_content[:500])

            # Total extracted text
            total_text = "".join(
                doc.page_content for doc in docs
            )

            st.write(
                f"📚 Total extracted text length: {len(total_text)}"
            )

            if len(total_text.strip()) == 0:
                st.error(
                    "No extractable text found. This PDF may be scanned/image-based."
                )
                st.stop()

            # Split documents
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            st.write(
                f"🧩 Chunks Created: {len(chunks)}"
            )

            if len(chunks) == 0:
                st.error("No chunks generated.")
                st.stop()

            # Show sample chunk
            st.write("🔍 Sample Chunk:")
            st.write(chunks[0].page_content[:500])

            # Embeddings
            embeddings = get_embeddings()

            test_vec = embeddings.embed_query(
                "hello world"
            )

            st.write(
                f"✅ Embedding Size: {len(test_vec)}"
            )

            # Create FAISS vector store
            vectorstore = FAISS.from_documents(
                chunks,
                embeddings
            )

            st.session_state.vectorstore = vectorstore

            st.success(
                f"✅ PDF Indexed Successfully ({len(chunks)} chunks)"
            )

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)

# --------------------------------------------------
# CHAT SECTION
# --------------------------------------------------

if st.session_state.vectorstore is not None:

    query = st.chat_input(
        "Ask a question about the PDF..."
    )

    if query:

        if not groq_api_key:
            st.error("Please enter your Groq API Key.")
            st.stop()

        try:

            retriever = (
                st.session_state.vectorstore
                .as_retriever(
                    search_kwargs={"k": 4}
                )
            )

            retrieved_docs = retriever.invoke(query)

            st.write(
                f"🔍 Retrieved {len(retrieved_docs)} chunks"
            )

            if len(retrieved_docs) == 0:
                st.warning(
                    "No relevant content found."
                )
                st.stop()

            context = "\n\n".join(
                doc.page_content
                for doc in retrieved_docs
            )

            prompt = f"""
You are a helpful PDF assistant.

Use ONLY the supplied context.

If the answer is not present in the context,
reply exactly:

I could not find that information in the PDF.

Context:
{context}

Question:
{query}

Answer:
"""

            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name=model_name,
                temperature=0.2
            )

            response = llm.invoke(prompt)

            answer = (
                response.content
                if hasattr(response, "content")
                else str(response)
            )

            st.chat_message("user").write(query)
            st.chat_message("assistant").write(answer)

            st.session_state.chat_history.append(
                {
                    "question": query,
                    "answer": answer
                }
            )

            with st.expander("📚 Retrieved Chunks"):

                for i, doc in enumerate(
                    retrieved_docs,
                    start=1
                ):

                    page = doc.metadata.get(
                        "page",
                        "N/A"
                    )

                    st.markdown(
                        f"### Chunk {i} | Page {page}"
                    )

                    st.write(
                        doc.page_content[:1000]
                    )

        except Exception as e:
            st.error(
                f"Query Error: {e}"
            )

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if st.session_state.chat_history:

    st.subheader("💬 Chat History")

    for item in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"**Question:** {item['question']}"
        )

        st.markdown(
            f"**Answer:** {item['answer']}"
        )

        st.divider()

# --------------------------------------------------
# RESET
# --------------------------------------------------

if st.button("🔄 Reset Session"):

    st.session_state.vectorstore = None
    st.session_state.chat_history = []

    st.rerun()
