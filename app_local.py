import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
# Streamlit page setup
st.set_page_config(page_title="Sleep Summary Assistant", page_icon="😴", layout="wide")
st.title("🛌 Sleep Assistant with Chat")
# Load RAG system
@st.cache_resource
def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model="deepseek-r1", base_url="http://localhost:8080")
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True, chain_type="stuff"
    )
    return rag_chain


rag_chain = load_rag()

# Generate Dynamic Prompt based on Sleep Statistics
def generate_dynamic_prompt(sleep_stats):
    prompt = f"""
    You are an expert sleep consultant. Based on the following sleep statistics, provide personalized insights:

    Sleep Statistics:
    {sleep_stats}

    Provide recommendations and insights based on the given data.
    """
    return prompt.strip()



# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm your AI Sleep Assistant. Please enter your sleep statistics or ask your sleep-related questions!")
    ]

# Sidebar: Enter Sleep Statistics manually
with st.sidebar:
    st.header("Enter Sleep Statistics")
    sleep_stats = st.text_area(
        "Paste your sleep stage statistics here (e.g., Sleep Efficiency, REM %, NREM %, etc.):",
        height=200
    )

    if st.button("Generate Sleep Summary"):
        dynamic_prompt = generate_dynamic_prompt(sleep_stats)
        
        # Generate sleep summary from dynamic prompt
        llm = ChatOllama(model="deepseek-r1", base_url="http://localhost:8080")
        summary_chain = ChatPromptTemplate.from_template(dynamic_prompt) | llm | StrOutputParser()
        sleep_summary = summary_chain.invoke({})
        
        st.session_state.sleep_summary = sleep_summary
        st.success("✅ Sleep summary generated!")

# Display sleep summary if available
if 'sleep_summary' in st.session_state:
    st.subheader("Sleep Summary")
    st.markdown(st.session_state.sleep_summary)

# Chat interface
st.subheader("Sleep Chatbot")
for message in st.session_state.chat_history:
    role = "AI" if isinstance(message, AIMessage) else "Human"
    with st.chat_message(role):
        st.write(message.content)

# User input for chatbot
user_query = st.chat_input("Type your question about sleep here...", max_chars=1000)

if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        # Incorporate RAG retrieval with sleep summary context
        context = st.session_state.get('sleep_summary', 'No summary provided yet.')
        prompt_template = f"""
        You are a helpful AI sleep assistant.
        Use the provided sleep summary as additional context:

        Sleep Summary: {context}

        Answer the user's question clearly and accurately. If necessary, retrieve additional information from the knowledge base.
        Question: {user_query}
        """

        # Invoke RAG system with the prompt
        response = rag_chain({"query": prompt_template})

        answer = response["result"]
        st.write(answer)

    st.session_state.chat_history.append(AIMessage(content=answer))
