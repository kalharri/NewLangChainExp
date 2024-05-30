
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

# anvil
import anvil.server

# local classes
from Actor import Actor
from Conversation import Conversation


# set required API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
anvil_uplink_key = os.getenv('ANVIL_UPLINK_KEY')
# anvil.server.connect(anvil_uplink_key)

# Set up Actor class' required LLM instance for generating chatbot responses
Actor.set_convo_bot(ChatOpenAI(model = 'gpt-4o', temperature = 0.65))

# create a meeting
meeting = Conversation(rounds = 15)

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
        dimitri = Actor.from_persona_file('assets/Dimitri Petrov Senior VP Marketing.txt') 

        # Assign skillsets
        priya.skillset = "Wilderness Survival"
        takashi.skillset = "Alpine Hiking & Camping"
        alex.skillset = "Medical Emergency Response"

        # Add the Actors to the meeting
        meeting.add_stakeholder(priya)
        meeting.add_stakeholder(takashi)
        meeting.add_stakeholder(alex)
        meeting.add_stakeholder(dimitri)

        # start the conversation
        # meeting.discuss_topic("Please brainstorm possible features for a new, AI-based sensor suite and patient monitoring solution. Fixed sensors, associated with the bed, would be paired with portable sensor(s) that a practitioner might wield. Please limit yourselves to a max of 55 words per utterance.")
        # meeting.discuss_topic("Brainstorm possible features for a new alpine survival system that we're thinking about. First, define the product's goals and converge on an easily-articulable set. Next, define the audience for the initial release. When you agree on audience, you can brainstorm the product features. Please limit yourselves to a max of 75 words per utterance.")
 

        meeting.discuss_topic("You are participating in a strategic workshop to brainstorm possible features for a new alpine survival system. During the brainstorming phase, focus on generating as many ideas as possible without criticism. Once you feel that the brainstorming phase is complete, shift to critically evaluating the ideas. Question the feasibility, practicality, and potential impact of the suggestions. Aim to refine and improve each idea through constructive criticism. Please limit yourselves to a max of 100 words per utterance, not including the emotes you have generated.")
    

        # ****** above is seed of a Workshop class ******
