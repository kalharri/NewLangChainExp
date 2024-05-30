
# The Conversation class simulates a conversation among a group of Actors. 
# Bob Howard
# kalharri@gmail.com

# Notes

# 5/ Should messages[] be stored once in the Conversation class, as opposed to each Actor? ask RC
# 6/ Monitor for "*Done*" messages in the conversation and terminate the topic early?


# Python
import random
from typing import List, Optional

# Anvil
import anvil.server


# import local classes
from Actor import Actor

class Conversation:

    def __init__(self, rounds: int = 6) -> None:
        """
        Initializes the Conversation instance with the specified number of rounds.

        Args:
            rounds (int): The maximum number of rounds for the conversation. Defaults to 6.
        """
        # all stakeholders (Actors) who'll participate in the workshop or meeting
        self._stakeholders: list[Actor] = []
        self._rounds: int = rounds
        self._current_round: int = 0
        self._system_behavior: Optional[str] = None                 # System Message Behavior text from a TXT file. Defines how any Actor behaves in a conversation.
        self._system_company: Optional[str] = None                  # System Message Company text from a TXT file. Defines the Actors' corporate context.
        self._topic: str = 'Discuss whatever you like.'             # The current topic of the conversation


    def discuss_topic(self, topic: str) -> None:
        """
        Starts a new conversation with the given topic without clearing the chat memory.

        Args:
            topic (str): The new topic of the conversation.
        """
        self._topic = topic
        # hand the topic to all members in the conversation
        for member in self._stakeholders:
            member.topic = topic

        print(f"{self._topic}\n\n")

        # conduct the rounds
        while self._current_round < self._rounds:
            self._current_round += 1
            print(f"\nRound {self._current_round} of {self._rounds}\n\n")

            self.conduct_round()


    def conduct_round(self) -> None:
        """
        Conducts a round of communication among stakeholders.
        """
        # Copy and shuffle the list to ensure random order
        remaining_actors = self._stakeholders.copy()
        random.shuffle(remaining_actors)

        # Iterate over the shuffled list of Actors
        while remaining_actors:
            actor: Actor = remaining_actors.pop()
            response: str = actor.invoke()

            if '*Done*' in response:
                print (f"**{actor.first_name}**: done\n\n")
            elif '*Pass*' in response:
                print (f"{actor.first_name}: pass\n\n")
            else:
                print (f'{response}\n\n')
                self.broadcast_to_others(response, actor)
        
        # Allow the human facilitator to comment at the end of each round           
        try:
            comment = input('Enter a comment: ')
            if comment and (comment != 'pass'):
                self.broadcast_to_others(f'Facilitator: {comment}', None)
        except EOFError:
            print("Input ended unexpectedly.")
        except Exception as e:
            print(f"An error occurred during input: {e}")


    # add a bot to the conversation
    def add_stakeholder(self, new_member: Actor) -> None:
        """
        Add a new actor to the conversation.

        Args:
            new_member (Actor): The actor object to add.
        """
        if not isinstance(new_member, Actor):
            raise TypeError("new_member must be an instance of Actor")

        new_member.behavior = self._system_behavior
        new_member.company = self._system_company
        new_member.create_system_message()
        self._stakeholders.append(new_member)


    def broadcast_to_others(self, message: str, speaker: Optional[Actor] = None) -> None:
        """
        Broadcasts a message to all stakeholders in the conversation, other than the speaker.

        Args:
            message (str): The message to be broadcast.
            speaker (Optional[Actor]): The speaker of the message. Defaults to None.
        """
        for member in self._stakeholders:
            if member != speaker:
                member.hear(message)
                # print(f'{member.first_name} heard {speaker.first_name}\n\n')


    def broadcast_topic(self, topic: str) -> None:
        """
        Broadcasts the topic to all stakeholders in the conversation.

        Args:
            topic (str): The topic to be broadcast.
        """
        for member in self._stakeholders:
            member.topic = topic

    # getter & setters

    @property
    def topic(self) -> str:
        """
        Gets the current topic of the conversation.

        Returns:
            str: The current topic.
        """
        return self._topic

    @topic.setter
    def topic(self, new_topic: str) -> None:
        """
        Sets a new topic for the conversation and appends it to the message history.

        Args:
            new_topic (str): The new topic to be set.
        """
        if isinstance(new_topic, str) and new_topic.strip():
            self._topic = new_topic
            self._append_message('human', new_topic)
        else:
            raise ValueError("The new topic must be a non-empty string.")

    @property
    def behavior(self) -> str:
        """
        Gets the system behavior.

        Returns:
            str: The system behavior.
        """
        return self._system_behavior

    @behavior.setter
    def behavior(self, new_behavior: str) -> None:
        """
        Sets a new system behavior.

        Args:
            new_behavior (str): The new system behavior.
        """
        if isinstance(new_behavior, str) and new_behavior.strip():
            self._system_behavior = new_behavior
        else:
            raise ValueError("The new behavior must be a non-empty string.")

    @property
    def company(self) -> str:
        """
        Gets the system company.

        Returns:
            str: The system company.
        """
        return self._system_company

    @company.setter
    def company(self, new_company: str) -> None:
        """
        Sets a new system company.

        Args:
            new_company (str): The new system company.
        """
        if isinstance(new_company, str) and new_company.strip():
            self._system_company = new_company
        else:
            raise ValueError("The new company must be a non-empty string.")

    @property
    def stakeholders(self) -> List[Actor]:
        """
        Gets the list of stakeholders in the conversation.

        Returns:
            List[Actor]: The list of stakeholders.
        """
        return self._stakeholders
