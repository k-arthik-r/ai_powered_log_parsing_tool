# ------------------------------------- IMPORT STATEMENTS --------------------------------------------------------------

import os
import time
import tempfile
import streamlit as st
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from parser import parse_log
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ------------------------------------ Loading .env file ---------------------------------------------------------------
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# ------------------------------------- STREAMLIT UI -------------------------------------------------------------------
st.logo(image="./meta-ai-logo.jpg-2.webp")
st.title("Log Parsing Tool")
st.sidebar.markdown(":red[Disclaimer:]")
sb_1 = st.sidebar.write("\nUpload your Log File & unleash the power of Llama 3 to answer your queries.\n")
st.sidebar.write("")
# ------------------------------------- LOADING THE LOG FILE -----------------------------------------------------------

uploaded_file = st.sidebar.file_uploader("Upload your Log File here: ", type=["log", "txt"],
                                         accept_multiple_files=False)
temp_file_path = None
if uploaded_file is not None:
    # Create a temporary file and write the uploaded file's content to it
    if "vectors" not in st.session_state:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        # Just to check where it's being stored.
        print(temp_file_path)


def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)
    try:
        os.remove("parsed_log_data.csv")
        print("File deleted successfully")
    except FileNotFoundError:
        print("File not found")


def file_loader():
    if "vectors" not in st.session_state:

        # If no parsing is needed
        if "not_log" in st.session_state:
            st.session_state.loader = TextLoader(file_path=temp_file_path)
        else:
            st.session_state.loader = CSVLoader(file_path="parsed_log_data.csv")
        st.session_state.log_file = st.session_state.loader.load()

        # Create a text splitter
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=60,
                                                                        length_function=len)

        # Splitting into smaller chunks.
        split_logs = st.session_state.text_splitter.split_documents(st.session_state.log_file)

        # Unlink the temporary file after use.
        os.unlink(temp_file_path)

        try:
            # Converting into embeddings.
            st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

            # Initializing the FAISS DB & storing the embeddings in it

            st.session_state.vectors = FAISS.from_documents(documents=split_logs,
                                                            embedding=st.session_state.embeddings)
        except Exception:
            st.warning("Please Check your embedding model & Refresh the page.")


# ------------------------------------- DEFINE PROMPT TEMPLATE ---------------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an advanced AI assistant integrated with a RAG (Retrieval-Augmented Generation) system,
                   "specialized in log analysis. Suggest next steps or further investigations when appropriate.
                   If you don't know the answer just say that you don't know.Don't try to make up an answer based on your
                   assumptions.
                   "Response Format:
                    Structure your responses clearly, using sections or bullet points for complex analyses.
                    Include the log entry which supports your answer
                    Include relevant log messages when explaining your findings.
                    Clearly distinguish between information from logs, retrieved knowledge, and your own analysis.
                    Provide the final answer to the question first in bold.
                    Clarification and Precision: If log formats or contents are unclear, ask for clarification.
                    """
         ),
        ("user", "The Log Data is as follows : {context}. User Question : {input}")
    ]
)

# Load Llama-3 LLM
try:
    llm = ChatGroq(groq_api_key=groq_api_key,
                   model_name="Llama3-70b-8192")
except Exception as e:
    st.warning("There was a problem with the Groq API. Please try again.")


def vector_embeddings(llm):
    # Create a chain for LLM & Prompt Template to inject to LLM for inferencing
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    # Creating a retriever to fetch top 2 chunks related to User_Prompt by making similarity search.
    retriever = st.session_state.vectors.as_retriever(search_kwargs={'k': 2})

    # Create a retrieval chain which links the retriever & document chain
    st.session_state.retrieval_chain = create_retrieval_chain(retriever, document_chain)


if "vectors" not in st.session_state:
    display_messages = []
    if uploaded_file is not None:
        with st.spinner(text="Parsing the Log File..."):
            type_of_log, msg = parse_log(temp_file_path)

        if type_of_log is not None and msg == "success":
            display_messages.append(st.sidebar.success("Detected " + type_of_log + " Logs."))
            time.sleep(1)
            display_messages.append(st.sidebar.success("Parsing Completed Successfully!"))
        else:
            display_messages.append(st.sidebar.warning("File didn't match predefined logs."))
            time.sleep(1)
            display_messages.append(st.sidebar.warning("Not Parsing."))
            st.session_state.not_log = True

        with st.spinner("Creating Vector Embeddings..."):
            file_loader()

        if "vectors" in st.session_state:
            display_messages.append(st.sidebar.success("Embedding are ready.."))
            vector_embeddings(llm)
            # Remove the success_msg
            time.sleep(1)

            for message in display_messages:
                message.empty()
                time.sleep(1)  # Clearing all temporary informative messages.

if uploaded_file is not None and "vectors" in st.session_state:
    message_container = st.container(height=500, border=False)
    if user_prompt := st.chat_input("Enter your query: ", key="prompt_for_llm"):
        message_container.markdown(":orange[User Prompt: ]")
        message_container.write(user_prompt)
        with st.spinner("Generating response.."):
            start_time = time.time()
            response = st.session_state.retrieval_chain.invoke({"input": user_prompt})
        st.sidebar.markdown("\n\n\n:green[Response Time : ]" + " " +
                            str(round((time.time() - start_time), 2)) + " sec.")
        message_container.markdown(":blue[Response:]")
        message_container.write(response['answer'])

# This block is to remove the chains, retrievers & embeddings from the session when user removes his log file.
if uploaded_file is None:
    st.warning("Please upload your Log file before asking questions.")
    if "vectors" in st.session_state:
        clear_cache()

