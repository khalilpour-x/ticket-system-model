"""
Ticket system based on a state model.
States: open, in progress, resolved, closed
"""

from enum import Enum
from typing import Optional
from datetime import datetime


class TicketState(Enum):
    """Enumeration of valid ticket states."""
    OPEN = "open"
    IN_PROGRESS = "in progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketStateTransitionError(Exception):
    """Exception raised when an invalid state transition is attempted."""
    pass


class Ticket:
    """
    A ticket class that manages state transitions based on a state model.
    
    Valid transitions:
    - open -> in progress
    - open -> closed
    - in progress -> resolved
    - in progress -> open (reopen)
    - resolved -> closed
    - resolved -> in progress (reopen for fixes)
    """
    
    def __init__(self, ticket_id: str, title: str, description: str = ""):
        """
        Initialize a new ticket.
        
        Args:
            ticket_id: Unique identifier for the ticket
            title: Title of the ticket
            description: Optional description of the ticket
        """
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.state = TicketState.OPEN
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.state_history = [(self.state, self.created_at)]
    
    def _is_valid_transition(self, new_state: TicketState) -> bool:
        """
        Check if a transition from current state to new state is valid.
        
        Args:
            new_state: The target state
            
        Returns:
            True if transition is valid, False otherwise
        """
        valid_transitions = {
            TicketState.OPEN: [TicketState.IN_PROGRESS, TicketState.CLOSED],
            TicketState.IN_PROGRESS: [TicketState.RESOLVED, TicketState.OPEN],
            TicketState.RESOLVED: [TicketState.CLOSED, TicketState.IN_PROGRESS],
            TicketState.CLOSED: [],  # No transitions from closed state
        }
        
        return new_state in valid_transitions.get(self.state, [])
    
    def transition_to(self, new_state: TicketState) -> None:
        """
        Transition the ticket to a new state.
        
        Args:
            new_state: The target state
            
        Raises:
            TicketStateTransitionError: If the transition is invalid
        """
        if new_state == self.state:
            raise TicketStateTransitionError(
                f"Ticket is already in state '{self.state.value}'"
            )
        
        if not self._is_valid_transition(new_state):
            raise TicketStateTransitionError(
                f"Invalid transition from '{self.state.value}' to '{new_state.value}'"
            )
        
        self.state = new_state
        self.updated_at = datetime.now()
        self.state_history.append((self.state, self.updated_at))
    
    def open(self) -> None:
        """Transition ticket to OPEN state."""
        self.transition_to(TicketState.OPEN)
    
    def start_progress(self) -> None:
        """Transition ticket to IN_PROGRESS state."""
        self.transition_to(TicketState.IN_PROGRESS)
    
    def resolve(self) -> None:
        """Transition ticket to RESOLVED state."""
        self.transition_to(TicketState.RESOLVED)
    
    def close(self) -> None:
        """Transition ticket to CLOSED state."""
        self.transition_to(TicketState.CLOSED)
    
    def get_state(self) -> TicketState:
        """Get the current state of the ticket."""
        return self.state
    
    def get_state_history(self) -> list:
        """Get the complete state transition history."""
        return [
            {
                "state": state.value,
                "timestamp": timestamp.isoformat()
            }
            for state, timestamp in self.state_history
        ]
    
    def __str__(self) -> str:
        """String representation of the ticket."""
        return (
            f"Ticket(id={self.ticket_id}, title='{self.title}', "
            f"state={self.state.value}, updated_at={self.updated_at.isoformat()})"
        )
    
    def __repr__(self) -> str:
        """Developer-friendly representation of the ticket."""
        return self.__str__()
