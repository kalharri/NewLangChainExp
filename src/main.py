
# Before Publishing
    # pip freeze > requirements.txt




# Entry point for the application
# Bob Howard
# kalharri@gmail.com

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

# import openai

# declare app's required API keys
load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')


llm = ChatOpenAI(temperature=0.9)

response: str = llm.invoke("how can langsmith help with testing?")

print(response)


