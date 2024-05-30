
# 
# Bob Howard
# kalharri@gmail.com

# Notes

# 1/ Choose and substitute appropriate Langchain agent for the Actor's LLM rather than the default ChatOpenAI model.


# Standard library imports
import os
from typing import List, Optional

# Third-party imports
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Local application/library-specific imports
from prompt_templates import system_message_template, human_message_template, ai_message_template



class Actor:
    """
    The Actor class models a corporate character, suitable for design thinking sessions or other types of conversations in simulated workshops or meetings.

    Attributes:
        first_name (str): The first name of the actor.
        last_name (str): The last name of the actor.
        role (str): The corporate role of the actor.
        persona (str): The instructions for the actor.
        temperature (float): The temperature value for generating responses.
    """

    # Class variables
    __convo_bot: ChatOpenAI = None          # app-provided LLM instance to conduct conversations with the personified Actor.


    # Class variable setters
    @classmethod
    def set_convo_bot(cls, bot: ChatOpenAI) -> None:
        """
        Set the conversation bot for the class.

        Args:
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


    def __init__(self, first_name: str = 'Unknown', last_name: str = 'Unknown', role: str = 'Unknown', persona: str = "You are a helpful assistant.", temperature: float = 0.65, skillset: str = "") -> None:
        """
        Initializes an instance of the Actor class.
        
        Args:
            first_name (str, optional): The first name of the actor. Defaults to 'Unknown'.
            last_name (str, optional): The last name of the actor. Defaults to 'Unknown'.
            role (str, optional): The corporate role of the actor. Defaults to 'Unknown'.
            persona (str, optional): The instructions for the actor. Defaults to "You are a helpful, corporate assistant.".
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

        self._behavior: str = None
        self._company: str = None
        self._skillset: str = skillset

        if skillset:
            detailed_skillset = self.expand_skillset(skillset)
            # print(f"**{self._first_name}**: {detailed_skillset}\n\n")
 

    # override the dunder method to format an instance of this class as a string
    def __str__(self):
        """
        Convert the Actor object to a string representation.

        Returns:
            str: The string representation of the object.
        """
        return str(self.__class__) + '\n' + '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in self.__dict__))


    def expand_skillset(self, skillset: str) -> str:
        """
        Expands a given skillset into a detailed description using the embedded language model.

        Args:
            skillset (str): The name of the skillset to be expanded (e.g., "Alpine Hiking & Camping").

        Returns:
            str: A detailed description of the skillset.
        """
        base_prompt = f"Describe the following skillset in detail: {skillset}"
        self.__convo_bot.temperature = 0.65
        response = self.__convo_bot.invoke(base_prompt)
        self._persona += f"\n\nExtra Skillset: {response}"

        return response


    def invoke(self, message: Optional[str] = None) -> str:
        """
        Calls the cached chat model with a user message and returns the chatbot's response.

        Args:
            message (str): The user message to be passed to the chatbot. If None, the last "heard" message will process

        Returns:
            str: The chatbot's response to the user message.
        """
        if message:
            # append the user's message to the local conversation memory
            self._append_message('human', message)

        # execute the LLM on the local message history
        if not self.__convo_bot:
            raise Exception('No language model instance found! Please set the conversation bot using Actor.set_convo_bot() before invoking.')

        # invoke the model
        self.__convo_bot.temperature = self._temperature
        response: str = self.__convo_bot.invoke(self._message_history)

        if response and (not ('*Pass*' in response.content)):
            # append the LLM's response to the local conversation memory
            self._append_message('human', response.content)
            return response.content
        else:
            return self.first_name + ': *Pass*'


    def create_system_message(self) -> None:
        """
        Creates the system message based on the Actor's persona and appends it to the message history

        Returns:
            None
        """
        self._append_message('system')

    
    def hear(self, message: str) -> None:
        """
        Simulates "hearing" a message from another Actor
        
        Args:
            message (str): The message content to be 'heard' by the Actor

        Returns:
            None
        """        
        self._append_message('human', message)


    def _append_message(self, message_type: str, content: Optional[str] = '') -> None:
        """
        Helper method to format and append messages to the message history.

        Args:
            message_type (str): The type of the message ('human', 'ai', or 'system').
            content (Optional[str]): The content of the message.
        """
        if message_type == 'human':
            formatted_message = human_message_template.format(content=content)
            self._message_history.append(HumanMessage(content=formatted_message))
        elif message_type == 'ai':
            formatted_message = ai_message_template.format(response=content)
            self._message_history.append(AIMessage(content=formatted_message))
        elif message_type == 'system':
            formatted_message = system_message_template.format(
                behavior=self._behavior,
                company=self._company,
                persona=self._persona
            )
            self._message_history.append(SystemMessage(content=formatted_message))
            

    # getters & setters

    @property
    def skillset(self) -> str:
        """
        Gets the skillset of the actor.

        Returns:
            str: The skillset of the actor.
        """
        return self._skillset

    @skillset.setter
    def skillset(self, value: str) -> None:
        """
        Sets the skillset of the actor and expands it into a detailed description.

        Args:
            value (str): The name of the skillset to be set and expanded.
        """
        self._skillset = value
        detailed_skillset = self.expand_skillset(value)
        # print(f'{self.first_name} {self.last_name} has learned about: {detailed_skillset}')
    
    @property
    def topic(self) -> str:
        """
        Gets the current topic.

        Returns:
            str: The current topic.
        """
        return self._topic
    
    @topic.setter
    def topic(self, new_topic: str) -> None:
        """
        Sets a new topic and appends it to the message history.

        Args:
            new_topic (str): The new topic to be set.
        """
        if new_topic:
            self._topic = new_topic
            self._message_history.append(HumanMessage(content = new_topic))
        
    @property
    def full_name(self) -> str:
        """
        Gets the full name of the actor.

        Returns:
            str: The full name of the actor.
        """
        return self._first_name + ' ' + self._last_name

    @property
    def first_name(self) -> str:
        """
        Gets the first name of the actor.

        Returns:
            str: The first name of the actor.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Sets the first name of the actor.

        Args:
            value (str): The new first name to be set.
        """
        self._first_name = value
        self._first_name = value

    @property
    def last_name(self) -> str:
        """
        Gets the last name of the actor.

        Returns:
            str: The last name of the actor.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Sets the last name of the actor.

        Args:
            value (str): The new last name to be set.
        """
        self._last_name = value

    @property
    def role(self) -> str:
        """
        Gets the role of the actor.

        Returns:
            str: The role of the actor.
        """
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        """
        Sets the role of the actor.

        Args:
            value (str): The new role to be set.
        """
        self._role = value

    @property
    def behavior(self) -> str:
        """
        Gets the behavior of the actor.

        Returns:
            str: The behavior of the actor.
        """
        return self._behavior

    @behavior.setter
    def behavior(self, value: str) -> None:
        """
        Sets the behavior of the actor.

        Args:
            value (str): The new behavior to be set.
        """
        self._behavior = value
    
    @property
    def company(self) -> str:
        """
        Gets the company of the actor.

        Returns:
            str: The company of the actor.
        """
        return self._company

    @company.setter
    def company(self, value: str) -> None:
        """
        Sets the company of the actor.

        Args:
            value (str): The new company to be set.
        """
        self._company = value
    
    @property
    def persona(self) -> str:
        """
        Gets the persona of the actor.

        Returns:
            str: The persona of the actor.
        """
        return self._persona

    @persona.setter
    def persona(self, value: str) -> None:
        """
        Sets the persona of the actor.

        Args:
            value (str): The new persona to be set.
        """
        self._persona = value
    
    @property
    def temperature(self) -> float:
        """
        Gets the temperature for generating responses.

        Returns:
            float: The temperature for generating responses.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        """
        Sets the temperature for generating responses.

        Args:
            value (float): The new temperature to be set.
        """
        self._temperature = value
    
    # Get the Actor's most recent prompt input 
    @property
    def last_prompt(self) ->str:
        """
        Gets the most recent prompt input.

        Returns:
            str: The content of the second to last message.
        """
        if len(self._message_history) < 2:
            return ''
        
        return self._message_history[-2].content


    @property
    def last_response(self) ->str:
        """
        Gets the last response from the messages context.

        Returns:
            str: The content of the last message in memory.
        """
        return self._message_history[-1].content

