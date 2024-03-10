
# The Conversation class simulates a conversation among a group of Actors. 
# Bob Howard
# kalharri@gmail.com

import random
from typing import List

# import local classes
from Actor import Actor

class Conversation:

    def __init__(self, topic: str = 'Speak about whatever you like.', rounds: int = 6) -> None:

        # define instance variables
        self._stakeholders: list[Actor] = []        # all stakeholders who'll participate in the workshop or meeting
        self._topic: str = topic                    # the topic to discuss
        self._rounds: int = rounds                  # how many rounds of conversation at max
        self._current_round: int = 0


    def discuss_topic(self, topic: str) -> None:
        """
        Starts a new conversation with a new topic, without clearing chat memory

        Args:
            topic (str): The new topic of the conversation.

        Returns:
            None
        """
        self._topic = topic

        # countdown the rounds
        while self._current_round < self._rounds:
            self.conduct_round(self._topic)


    def conduct_round(self, prompt: str):
        # Copy the list to avoid modifying the original list
        remaining_actors = self._stakeholders.copy()
        # Shuffle the list to ensure random order
        random.shuffle(remaining_actors)

        # Iterate over the shuffled list and forward the response to each actor
        while remaining_actors:
            # Remove the last actor from the list
            actor = remaining_actors.pop()
            # get this actors response
            response = actor.member(prompt)
            # let others in the meeting "hear" about it
            self.broadcast(response)


    # add a bot to the conversation
    def add_stakeholder(self, new_member: Actor) -> None:
        """
        Add a new actor to the conversation.

        Args:
            new_member (Actor): The actor object to be added.

        Returns:
            None
        """
        self._stakeholders.append(new_member)


    def broadcast(self, message: str) -> None:
        """
        Broadcasts a message to all stakeholders in the conversation.

        Args:
            message (str): The message to be broadcasted.

        Returns:
            None
        """
        for member in self._stakeholders:
            member.hear(message)


    @property
    def topic(self) ->str:
        return self._topic

    @topic.setter
    def topic(self, new_topic: str) -> None:
        if new_topic:
            self._topic = new_topic


    @property
    def stakeholders(self) ->list[Actor]:
        return self._stakeholders



