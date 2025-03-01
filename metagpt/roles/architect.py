#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : architect.py
"""

from metagpt.actions import WriteDesign, WritePRD, Feedback
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.schema import Message


class Architect(Role):
    """
    Represents an Architect role in a software development process.
    
    Attributes:
        name (str): Name of the architect.
        profile (str): Role profile, default is 'Architect'.
        goal (str): Primary goal or responsibility of the architect.
        constraints (str): Constraints or guidelines for the architect.
    """
    
    def __init__(self, 
                 name: str = "Bob", 
                 profile: str = "Architect", 
                 goal: str = "Design a concise, usable, complete python system",
                 constraints: str = "Try to specify good open source tools as much as possible",
                 feedback: str = True) -> None:
        """Initializes the Architect with given attributes."""
        super().__init__(name, profile, goal, constraints, feedback)
        
        # Initialize actions specific to the Architect role
        self._init_actions([WriteDesign])
        if feedback:
            self._add_action_at_head(Feedback)
        # Set events or actions the Architect should watch or be aware of
        self._watch([WritePRD])

    async def _think(self) -> None:

        if self._rc.todo is None:
            self._set_state(0)
            return

        if self._rc.state + 1 < len(self._states):
            self._set_state(self._rc.state + 1)
        else:
            self._rc.todo = None

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        todo = self._rc.todo
        
        if isinstance(todo, Feedback):
            msg = self._rc.memory.get_by_action(WritePRD)[0]
            feedback, prev_role, _ =  await todo.run(msg)
            ret = Message(feedback, role=self.profile, cause_by=type(todo), send_to=prev_role)
            self._rc.long_term_memory.save_feedback(ret, init=False)
        elif isinstance(todo, WriteDesign):
            msg = self._rc.memory.get_by_action(WritePRD)
            design =  await todo.run(msg)
            ret = Message(design.content, role=self.profile, cause_by=WriteDesign)
        else:
            raise NotImplementedError
        
        self._rc.memory.add(ret)
        return ret
    
    async def _react(self) -> Message:
        while True:
            await self._think()
            if self._rc.todo is None:
                break
            msg = await self._act()
            todo = self._rc.todo
            ret = Message(msg.content, role=self.profile, cause_by=type(todo))

        return ret