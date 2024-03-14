
# The Actor class models a corporate character, suitable for design thinking sessions or other 
# types of conversations in simulated workshops or meetings.
# Bob Howard
# kalharri@gmail.com

# Notes

# 1/ Choose and substitute appropriate Langchain agent for the Actor's LLM rather than the default ChatOpenAI model.


import os

# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)


class Actor:

    # Class variables
    __convo_bot: ChatOpenAI = None          # app-provided LLM instance to conduct conversations with the personified Actor.


    # Class variable setters
    @classmethod
    def set_convo_bot(cls, bot: ChatOpenAI):
        """
        Set the conversation bot for the class.

        Args:
            cls: The class itself.
            bot (ChatOpenAI): The conversation bot to set.

        Returns:
            None
        """
        cls.__convo_bot = bot


    @classmethod

    def from_persona_file(cls, file_path: str) -> 'Actor':
        """
        Load a text-based persona file and create a corresponding Actor object

        Args:
            file_path (str): The full path of the file to load the persona from.

        Returns:
            Actor: The Actor object based on the loaded persona.
        """
        with open(file_path, 'r') as file:
            persona: str = file.read()

            # Isolate the filename from the path & extension
            filename_without_path = os.path.basename(file_path)
            filename_without_extension, _ = os.path.splitext(filename_without_path)

            # Now split the remaining filename into parts
            parts = filename_without_extension.split(' ', 2)
            first_name, last_name, role = parts

            # Create the Actor instance
            instance: Actor = Actor(persona = persona, first_name = first_name, last_name = last_name, role = role)

            print(f"loaded actor's persona from file: {file_path}\n")

            return instance


    def __init__(self, first_name: str = 'Unknown', last_name: str = 'Unknown', role: str = 'Unknown', persona: str = "You are a helpful, corporate assistant.", temperature: float = 0.9) -> None:
        """
        Initializes an instance of the Actor class.
        
        Args:
            name (str, optional): The name of the actor. Defaults to Unknown.
            role (str, optional): The corporate role of the actor. Defaults to "You are a helpful, corporate assistant.".
            persona (str, optional): The instructions for the actor. Defaults to Unknown.
            temperature (float, optional): The temperature value for generating responses. Defaults to 0.9.
            
        Returns:
            None
        """

        # define instance variables to model an individual Actor
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._role: str = role
        self._persona: str = persona
        self._temperature: float = temperature
        self._topic: str = 'Discuss anything at all.' # *** move to Conversation class ***
 
        # init the bot's conversation memory & give it it's instructions via a system message.
        self._message_history: list = []
#        self._message_history.append(self.system_message)

        self._behavior: str = None
        self._company: str = None
 

    # override the dunder method to format an instance of this class as a string
    def __str__(self):
        """
        Convert the Actor object to a string representation.

        Returns:
            str: The string representation of the object.
        """
        return str(self.__class__) + '\n' + '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in self.__dict__))
    

    def __call__(self, message: str = None) -> str:
        """
        Calls the cached chat model with a user message and returns the chatbot's response.
        Allows constructions like:
            maggie = Actor(first_name = "Maggie", temperature=1.6)
            response = maggie("What's your name?")

        Args:
            message (str): The user message to be passed to the chatbot. If None, the last "heard" message will process

        Returns:
            str: The chatbot's response to the user message.
        """
        if message:
            # append the user's message to the local conversation memory
            self._message_history.append(HumanMessage(content = message))
        else:
            # use the last message in the local conversation memory as the prompt
            message = self.last_response

        # execute the LLM on the local message history
        if not self.__convo_bot:
            raise Exception('no language model found!')

        # invoke the model
        self.__convo_bot.temperature = self._temperature
        response = self.__convo_bot(self._message_history)

        if response and (not ('*Pass*' in response.content)):
            # append the LLM's response to the local conversation memory
            self._message_history.append(HumanMessage(content = response.content)) # *** chg to HumanMessage + look for other cases
            return response.content
        else:
            return self.first_name + ': *Pass*'

    def create_system_message(self) -> None:
        """
        Creates the system message based on the Actor's persona.

        Returns:
            None
        """
        self._message_history.append(self.system_message)

    def hear(self, message: str) -> None:
        """
        Simulates "hearing" a message from another Actor
        
        Args:
            message (str): The message content to be recorded.

        Returns:
            None
        """        
        self._message_history.append(HumanMessage(content = message))      # *** should this be a HumanMessage?
    

    @property
    def topic(self) -> str:
        return self._topic
    
    @topic.setter
    def topic(self, new_topic: str) -> None:
        if new_topic:
            self._topic = new_topic
            self._message_history.append(HumanMessage(content = new_topic))
        

    # Getters & setters

    @property
    def full_name(self) -> str:
        return self._first_name + ' ' + self._last_name

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self._first_name = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        self._last_name = value

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        self._role = value

    @property
    def behavior(self) -> str:
        return self._behavior

    @behavior.setter
    def behavior(self, value: str) -> None:
        self._behavior = value
    
    @property
    def company(self) -> str:
        return self._company

    @company.setter
    def company(self, value: str) -> None:
        self._company = value
    
    @property
    def persona(self) -> str:
        return self._persona

    @persona.setter
    def persona(self, value: str) -> None:
        self._persona = value
    
    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value
    
    @property
    def system_message(self) -> SystemMessage:
        """
        Property function to get the system message.
        Returns:
            SystemMessage: The system message object with the Instructions, Company and persona.
        """
        return SystemMessage(
            content = self.behavior + '\n\n' + self.company + '\n\n' + self.persona
        )
    

    # Get the Actor's most recent prompt input 
    @property
    def last_prompt(self) ->str:
        """
        Returns what the Actor last responded to.

        Returns:
            str: The content of the second to last message.
        """
        if len(self._message_history) < 2:
            return ''
        
        return self._message_history[-2].content


    @property
    def last_response(self) ->str:
        """
        Returns the Actor's last response from the messages context.

        Returns:
            str: The content of the last message in memory.
        """
        return self._message_history[-1].content

