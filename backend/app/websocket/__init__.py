"""
WebSocket Module

This module handles all WebSocket connections and real-time communication
between the frontend and backend.

Modules:
- connection: Connection lifecycle management
- test_execution: Test case and step execution
- test_generation: Test case generation with AI

Author: O9 Automation Team
Date: 2026-01-13
"""

from .connection import ConnectionManager, WebSocketWrapper, manager
from .test_execution import handle_execute_step, handle_execute_all_steps
from .test_generation import handle_generate_test_case

__all__ = [
    'ConnectionManager',
    'WebSocketWrapper',
    'manager',
    'handle_execute_step',
    'handle_execute_all_steps',
    'handle_generate_test_case',
]
