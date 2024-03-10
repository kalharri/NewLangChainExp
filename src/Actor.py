
# Actor class models a corporatecharacter, suitable for design thinking sessions or other simulated workshops or meetings

import os

# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)


class Actor:

    # Class variables
    __convo_bot: ChatOpenAI = None   # app-provided LLM instance to conduct conversations with the personified Actor.
    __system_prefix: str = None      # System Message prefix text from an RTF file. Defines how any Actor behaves in a conversation.

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
    def set_system_prefix(cls, instructions: str):
        """
        Set the system prefix that defines all actor behaviors in conversations.
        
        Args:
            cls: The class object.
            instructions (str): The instructions for the system prefix.
        
        Returns:
            None
        """
        cls.__system_prefix = instructions

    @classmethod
    def load_system_prefix(cls, filename: str) -> str:
        """
        Load the System Message prefix text from an txt file.

        Args:
            filename (str): The full path of the file to load the System Message prefix from.

        Returns:
            str: The System Message prefix text.
        """
        with open(filename, 'r') as file:
            return file.read()


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

            print(f"loaded actor's persona from file: {file_path}")

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
 
        # init the bot's conversation memory & give it it's instructions via a system message.
        self._message_history: list = []
        self._message_history.append(self.system_message)
 


    # override the dunder method to format an instance of this class as a string
    def __str__(self):
        """
        Convert the Actor object to a string representation.

        Returns:
            str: The string representation of the object.
        """
        return str(self.__class__) + '\n' + '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in self.__dict__))
    

    def __call__(self, message: str) -> str:
        """
        Calls the cached chatbot with a user message and returns the chatbot's response.
        Allows constructions like:
            maggie = Actor("Maggie", temperature=1.6, synopsis)
            response = maggie("What's your name?")

        Args:
            message (str): The user message to be passed to the chatbot. If None, the last "heard" message will process

        Returns:
            str: The chatbot's response to the user message.
        """
        if message:
            # append the user's message to the local conversation memory
            self._message_history.append(HumanMessage(content = message))

        # execute the LLM on the updated message history
        if not self.__convo_bot:
            raise Exception('no language model found!')

        self.__convo_bot.temperature = self._temperature
        result = self.__convo_bot(self._message_history)

        # append the LLM's response to the local conversation memory
        self._message_history.append(AIMessage(content = result.content))

        return result.content

    def hear(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self._message_history.append(f"{name}: {message}")           


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
    def file_path(self) -> str:
        return self._file_path
   
    @property
    def system_message(self) -> SystemMessage:
        """
        Property function to get the system message.
        Returns:
            SystemMessage: The system message object with the prefix and persona instructions.
        """
        return SystemMessage(
            content = self.__system_prefix + '\n\n' + self.persona
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


