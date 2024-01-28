
# Before Publishing
    # pip freeze > requirements.txt

    # pip install --user ffmpeg-python

# Entry point for the application
# Bob Howard
# kalharri@gmail.com

import os
from dotenv import load_dotenv
from pathlib import Path
import threading  # Import threading for synchronization

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from openai import OpenAI

from RealtimeTTS import TextToAudioStream, OpenAIEngine


# Define a callback function that will be called when voice playback is done
def on_playback_finished():
    playback_finished.set()  # Set the system event to signal that playback is finished

# declare required API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# set up for speech output
engine = OpenAIEngine()
stream = TextToAudioStream(engine, log_characters = True, on_audio_stream_stop = on_playback_finished)

def llm_response_generator(messages):
    for string_chunk in chain.stream({"input": "how can LangSmith help with testing?"}):
        # print(string_chunk, end="")
        yield string_chunk

# initialize the bot's conversation memory
messages = [
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ]

# setup the prompt template for Langchain
prompt = ChatPromptTemplate.from_messages(messages)

# set up the chat model, the output parser to pretty up its responses, and construct the chain
llm = ChatOpenAI(temperature=0.9)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# wrap the llm response generator with the TTS stream
stream.feed(llm_response_generator(messages = messages))

# Create an event to signal when playback is finished
playback_finished = threading.Event()

stream.play_async(fast_sentence_fragment = True, minimum_sentence_length=5)

# Wait for the playback to finish
playback_finished.wait()  # This will block until the event is set by on_playback_finished



"""
HOW TO DO RAG WITH LANGCHAIN. INDEX WRAPS THE MODEL, LOADS RELEVANT CHUNKS FOR CONTEXT

# load the LangSmith overview directly from their website
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()

# compute embeddings and store it in a vector database
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)
"""
