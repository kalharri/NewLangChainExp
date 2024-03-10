
# Before Publishing
    # pip freeze > requirements.txt

    # pip install --user ffmpeg-python

# Entry point for the application
# Bob Howard
# kalharri@gmail.com

# python
import os
from dotenv import load_dotenv
from pathlib import Path
import random

# langchain
from langchain_openai import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from langchain.agents.openai_assistant import OpenAIAssistantRunnable
# from langchain.agents import AgentExecutor

# ours
from Actor import Actor
from Conversation import Conversation


# declare required API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up Actor class' required LLM instance for generating chatbot responses
Actor.set_convo_bot(ChatOpenAI(model = 'gpt-3.5-turbo', temperature = random.uniform(0.8, 1.2)))

# Set up Actor class' System Message prefix text from an RTF file.
# This conditions each stakeholder on how to behave, regardless of role.
with open('assets/StakeholderSystemPrefix.txt', 'r') as file:

    system_prefix = file.read()
    Actor.set_system_prefix(system_prefix)

    # create test stakeholders
    priya   = Actor.from_persona_file('assets/Priya Singh CTO.txt')
    takashi = Actor.from_persona_file('assets/Takashi Mitsui Product Manager.txt')   
    alex    = Actor.from_persona_file('assets/Alexandra Taylor CFO.txt')   

    # create a meeting
    meeting = Conversation(topic = 'Discuss the tradeoffs in creating a mobile app as a webapp, a hybrid app, or a native app', rounds = 4)
    meeting.add_stakeholder(priya)
    meeting.add_stakeholder(takashi)
    meeting.add_stakeholder(alex)


    # start the meeting
    print(meeting.start_conversation())





