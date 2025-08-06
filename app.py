import streamlit as st
import requests
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.language_models.chat_models import BaseChatModel, ChatResult, ChatGeneration
from typing import ClassVar
from pydantic import PrivateAttr


st.set_page_config(page_title="Sleep Assistant RAG Chatbot", page_icon="😴")
st.title("🛌 Sleep Assistant RAG Chatbot")
# =======================
# DeepSeek LLM Wrapper
# =======================
class ChatDeepSeekLLM(BaseChatModel):
    model: ClassVar[str] = "deepseek-chat"
    _api_url: str = PrivateAttr()
    _api_key: str = PrivateAttr()

    def __init__(self, api_url: str, api_key: str):
        super().__init__()
        self._api_url = api_url
        self._api_key = api_key

    @property
    def _llm_type(self) -> str:
        return "deepseek-chat"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop=None,
        run_manager=None,
        **kwargs
    ) -> ChatResult:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user" if isinstance(m, HumanMessage) else "assistant",
                    "content": m.content,
                }
                for m in messages
            ],
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}
        resp = requests.post(self._api_url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        answer = data["choices"][0]["message"]["content"]
        # Return a ChatResult with a flat list of ChatGeneration
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=answer))]
        )

# =======================
# Configuration
# =======================
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "s***************************"

# =======================
# Load RAG Chain
# =======================
@st.cache_resource
def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatDeepSeekLLM(DEEPSEEK_API_URL, DEEPSEEK_API_KEY)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )

rag_chain = load_rag()

# =======================
# Streamlit App UI
# =======================


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm your AI Sleep Assistant. How can I help you today?")
    ]
if "source_docs" not in st.session_state:
    st.session_state.source_docs = []

# Display prior messages with optional sources
for idx, msg in enumerate(st.session_state.chat_history):
    role = "AI" if isinstance(msg, AIMessage) else "Human"
    with st.chat_message(role):
        st.markdown(msg.content)
        if role == "AI" and idx < len(st.session_state.source_docs):
            docs = st.session_state.source_docs[idx]
            if docs:
                with st.expander("Sources"):
                    for i, doc in enumerate(docs):
                        meta = doc.metadata
                        title = meta.get("title", meta.get("source", "Untitled"))
                        snippet = doc.page_content[:250].replace("\n", " ")
                        st.markdown(f"- **Source {i+1}**: *{title}*\n  \n  Snippet: {snippet}…")

# User input
user_query = st.chat_input("Type your sleep question here…", max_chars=1000)
if user_query:
    # Append user message
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    # Get RAG response
    result = rag_chain({"query": user_query})
    answer = result["result"]
    docs = result.get("source_documents", [])

    # Display AI response
    with st.chat_message("AI"):
        st.markdown(answer)
        if docs:
            with st.expander("Sources"):
                for i, doc in enumerate(docs):
                    meta = doc.metadata
                    title = meta.get("title", meta.get("source", "Untitled"))
                    snippet = doc.page_content[:250].replace("\n", " ")
                    st.markdown(f"- **Source {i+1}**: *{title}*\n  \n  Snippet: {snippet}…")

    # Save into session state
    st.session_state.chat_history.append(AIMessage(content=answer))
    st.session_state.source_docs.append(docs)
