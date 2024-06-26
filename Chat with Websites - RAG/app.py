import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load the environment variables
load_dotenv()


def get_vectorestore_from_url(url):
    # get the text from the website
    loader = WebBaseLoader(url)
    document = loader.load()

    # split the text into sentences
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    # get the vector store 
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()

    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the convversation.")
    ])
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        "system", "Answer the user's questions based on the below context:\n\n{context}",
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt=prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_query):
    # Get the vector store and retriever chain
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)

    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
            "chat_history": st.session_state.chat_history,
            "input": user_query
        })
    return response['answer']

# App config
st.set_page_config(page_title="Chat with Websites", page_icon=":shark:")
st.title("Chat with Websites")

# Sidebar
with st.sidebar:
    st.header("Settings")
    web_ulr = st.text_input("Website URL")

if web_ulr is None or web_ulr == "":
    st.warning("Please enter a website URL")

else:
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! How can I help you today?"),
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorestore_from_url(web_ulr)

    # User Input
    user_query = st.chat_input("Type your message here...")

    if user_query is not None and user_query != "":
        # response = get_response(user_query)
        response = get_response(user_query)
        # st.write(response)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # Conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

