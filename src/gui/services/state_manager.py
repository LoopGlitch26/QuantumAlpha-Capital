"""
State Manager - Global reactive state management for UI
"""

from typing import Optional
from src.backend.bot_engine import SystemState


class StateManager:
    """Manages global application state for UI components"""

    def __init__(self):
        self._system_state: SystemState = SystemState()
        self._observers = []

    def update(self, new_state: SystemState):
        """
        Update state with new data from market processor.
        Called by bot_service when system state changes.
        """
        self._system_state = new_state
        # Notify observers (future enhancement)
        for observer in self._observers:
            try:
                observer(new_state)
            except Exception:
                pass

    def get_state(self) -> SystemState:
        """Get current application state"""
        return self._system_state

    def subscribe(self, callback):
        """Subscribe to state changes (future enhancement)"""
        if callback not in self._observers:
            self._observers.append(callback)

    def unsubscribe(self, callback):
        """Unsubscribe from state changes"""
        if callback in self._observers:
            self._observers.remove(callback)
