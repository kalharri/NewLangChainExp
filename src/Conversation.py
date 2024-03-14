
# The Conversation class simulates a conversation among a group of Actors. 
# Bob Howard
# kalharri@gmail.com

# Notes

# 4/ Add a prompt template to convert the parameter files' content to our system message.
# 5/ Should messages[] be stored once in the Conversation class, as opposed to each Actor? ask RC
# 6/ Monitor for "*Done*" messages in the conversation and terminate the topic early.


import random
from typing import List

# import local classes
from Actor import Actor

class Conversation:

    def __init__(self, rounds: int = 6) -> None:
        """
        Initializes the workshop or meeting with the specified number of rounds.

        Args:
            rounds (int): The number of rounds of conversation at max. Defaults to 6.

        Returns:
            None
        """
        # all stakeholders (Actors) who'll participate in the workshop or meeting
        self._stakeholders: list[Actor] = []
        self._rounds: int = rounds
        self._current_round: int = 0
       
        self._system_behavior: str = None               # System Message Behavior text from a TXT file. Defines how any Actor behaves in a conversation.
        self._system_company: str = None                # System Message Company text from a TXT file. Defines the Actors' corporate context.
        self._topic: str = 'Discuss whatever you like.' # The current topic of the conversation


    def discuss_topic(self, topic: str) -> None:
        """
        Starts a new conversation with a new topic, without clearing chat memory

        Args:
            topic (str): The new topic of the conversation.

        Returns:
            None
        """
        self._topic = topic
        # hand the topic to all members in the conversation
        for member in self._stakeholders:
            member.topic = topic

        print(f"Meeting to discuss: {self._topic}\n\n")

        # countdown the rounds
        while self._current_round < self._rounds:
            self._current_round += 1
            print(f"Round {self._current_round} of {self._rounds}\n\n")

            self.conduct_round(self._topic)


    def conduct_round(self, topic: str):
        """
        Conducts a round of communication among stakeholders.
        
        Args:
            topic (str): The topic of discussion for the round.
        
        Returns:
            None
        """
        # Copy the list to avoid modifying the original list
        remaining_actors = self._stakeholders.copy()
        # Shuffle the list to ensure random order
        random.shuffle(remaining_actors)

        # Iterate over the shuffled list and forward the the responses to all
        while remaining_actors:
            # Remove the last actor from the list
            actor: Actor = remaining_actors.pop()
            # get this actors response
            response: str = actor.invoke()

            if '*Done*' in response:
                print (f"**{actor.first_name}**: done\n\n")
                break
            elif '*Pass*' in response:
                print (f"{actor.first_name}: pass\n\n")
                continue
            else:
                print (f'{response}\n\n')
                self.broadcast_to_others(response, actor)


    # add a bot to the conversation
    def add_stakeholder(self, new_member: Actor) -> None:
        """
        Add a new actor to the conversation.

        Args:
            new_member (Actor): The actor object to be added.

        Returns:
            None
        """
        new_member.behavior = self._system_behavior
        new_member.company = self._system_company
        new_member.create_system_message()
        self._stakeholders.append(new_member)


    def broadcast_to_others(self, message: str, speaker: Actor) -> None:
        """
        Broadcasts a message to all stakeholders in the conversation, other than the speaker.

        Args:
            message (str): The message to be broadcasted.
            speaker (Actor): The speaker of the message.

        Returns:
            None
        """
        for member in self._stakeholders:
            if member != speaker:
                member.hear(message)
                # print(f'{member.first_name} heard {speaker.first_name}\n\n')


    def broadcast_topic(self, topic: str) -> None:
        """
        Broadcasts the topic to all stakeholders in the conversation.

        Args:
            message (str): The message to be broadcasted.

        Returns:
            None
        """
        for member in self._stakeholders:
            member.topic = topic

    # getter & setters

    @property
    def topic(self) ->str:
        return self._topic

    @topic.setter
    def topic(self, new_topic: str) -> None:
        self._topic = new_topic

    @property
    def behavior(self) ->str:
        return self._system_behavior

    @behavior.setter
    def behavior(self, new_behavior: str) -> None:
        self._system_behavior = new_behavior

    @property
    def company(self) ->str:
        return self._system_company

    @company.setter
    def company(self, new_company: str) -> None:
        self._system_company = new_company

    @property
    def stakeholders(self) ->list[Actor]:
        return self._stakeholders



