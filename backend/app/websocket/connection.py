"""
WebSocket Connection Handlers

This module manages WebSocket connection lifecycle including:
- Client connections
- Client disconnections
- Connection state tracking
- Message broadcasting

Author: O9 Automation Team
Date: 2026-01-13
"""

from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for the application.
    
    This class tracks all active WebSocket connections and provides
    methods to send messages to individual connections or broadcast
    to all connected clients.
    
    Attributes:
        active_connections (list[WebSocket]): List of currently active WebSocket connections
    
    Example:
        >>> manager = ConnectionManager()
        >>> await manager.connect(websocket)
        >>> await manager.send_personal_message({'type': 'hello'}, websocket)
        >>> await manager.broadcast({'type': 'update'})
        >>> manager.disconnect(websocket)
    """
    
    def __init__(self):
        """Initialize the connection manager with an empty connections list"""
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """
        Accept and register a new WebSocket connection.
        
        Args:
            websocket (WebSocket): The WebSocket connection to accept and register
            
        Example:
            >>> await manager.connect(websocket)
            >>> # Connection is now tracked and ready to receive messages
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection from tracking.
        
        Args:
            websocket (WebSocket): The WebSocket connection to remove
            
        Example:
            >>> manager.disconnect(websocket)
            >>> # Connection is no longer tracked
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific WebSocket connection.
        
        Args:
            message (dict): The message to send (will be JSON-encoded)
            websocket (WebSocket): The target WebSocket connection
            
        Raises:
            Exception: If the message cannot be sent (connection may be closed)
            
        Example:
            >>> await manager.send_personal_message({
            ...     'type': 'status_update',
            ...     'message': 'Processing...'
            ... }, websocket)
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            # Remove connection if it's broken
            self.disconnect(websocket)
            raise
    
    async def broadcast(self, message: dict):
        """
        Broadcast a message to all active WebSocket connections.
        
        If a connection fails, it is silently removed from the list.
        This ensures that broken connections don't prevent other
        clients from receiving messages.
        
        Args:
            message (dict): The message to broadcast (will be JSON-encoded)
            
        Example:
            >>> await manager.broadcast({
            ...     'type': 'system_notification',
            ...     'message': 'Server maintenance in 5 minutes'
            ... })
        """
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send broadcast to connection: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.disconnect(conn)


# Global connection manager instance
# Use this throughout the application to manage WebSocket connections
manager = ConnectionManager()


class WebSocketWrapper:
    """
    Wrapper to make FastAPI WebSocket compatible with SeleniumService.
    
    The SeleniumService expects a WebSocket-like object with a send_message
    method, but FastAPI's WebSocket uses send_json. This wrapper bridges
    the gap.
    
    Attributes:
        websocket (WebSocket): The underlying FastAPI WebSocket connection
    
    Example:
        >>> ws_wrapper = WebSocketWrapper(websocket)
        >>> await ws_wrapper.send_message({'type': 'update', 'data': '...'})
    """
    
    def __init__(self, websocket: WebSocket):
        """
        Initialize the WebSocket wrapper.
        
        Args:
            websocket (WebSocket): The FastAPI WebSocket to wrap
        """
        self.websocket = websocket
    
    async def send_message(self, message: dict):
        """
        Send a message through the wrapped WebSocket.
        
        This method converts the message to JSON and sends it through
        the underlying FastAPI WebSocket connection.
        
        Args:
            message (dict): The message to send (will be JSON-encoded)
            
        Raises:
            Exception: If the message cannot be sent
            
        Example:
            >>> await ws_wrapper.send_message({
            ...     'type': 'execution_progress',
            ...     'step': 5,
            ...     'total': 10
            ... })
        """
        await self.websocket.send_json(message)
