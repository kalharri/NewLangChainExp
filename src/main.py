
# Before Publishing
    # pip freeze > requirements.txt
# virtual environment
    # source langchain-env/bin/activate

# Entry point for the application
# Bob Howard
# kalharri@gmail.com

# Notes

# 1/ Choose and substitute appropriate Langchain agent for the Actor's LLM rather than the default ChatOpenAI model.


# python
import os
from dotenv import load_dotenv
from pathlib import Path
import random

# langchain
from langchain_openai import ChatOpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
# from langchain.agents import AgentExecutor

# ours
from Actor import Actor
from Conversation import Conversation


# declare required API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Set up Actor class' required LLM instance for generating chatbot responses
Actor.set_convo_bot(ChatOpenAI(model = 'gpt-3.5-turbo', temperature = random.uniform(0.8, 1.2)))

# create a meeting
meeting = Conversation(rounds = 10)

# Set up Conversation class' System Message prefix text from a txt file.
# This conditions each stakeholder on how to behave, regardless of role.
with open('assets/StakeholderSystemInstructions.txt', 'r') as file:
    meeting.behavior = file.read()

    # And the company profile, as well
    with open('assets/StakeholderSystemCompany.txt', 'r') as file:
        meeting.company = file.read()

    # create test stakeholders
    priya   = Actor.from_persona_file('assets/Priya Singh CTO.txt')
    takashi = Actor.from_persona_file('assets/Takashi Mitsui Product Manager.txt')   
    alex    = Actor.from_persona_file('assets/Alexandra Taylor CFO.txt')   

    # Add the Actors to the meeting
    meeting.add_stakeholder(priya)
    meeting.add_stakeholder(takashi)
    meeting.add_stakeholder(alex)

    # start the conversation
    # meeting.discuss_topic("Please brainstorm possible features for a new, AI-based sensor suite and patient monitoring solution. Fixed sensors, associated with the bed, would be paired with portable sensor(s) that a practitioner might wield. Please limit yourselves to a max of 55 words per utterance.")
    meeting.discuss_topic("Brainstorm possible features for a new alpine survival system that we're thinking about. Please limit yourselves to a max of 60 words per utterance.")







