# WebSocket Module

This module handles all WebSocket connections and real-time communication between the frontend and backend.

## Overview

The WebSocket module provides real-time, bidirectional communication for:
- Test case and step execution
- Test case generation with AI
- Progress updates during long-running operations
- Error reporting and status updates

## Architecture

```
app/websocket/
├── __init__.py          # Module exports
├── connection.py         # Connection lifecycle management
├── test_execution.py     # Test step and test case execution
└── test_generation.py    # AI-powered test case generation
```

## Modules

### `connection.py`
Manages WebSocket connection lifecycle.

**Classes:**
- `ConnectionManager`: Tracks active connections and provides broadcasting
- `WebSocketWrapper`: Adapter for FastAPI WebSocket compatibility

**Usage:**
```python
from app.websocket import manager, WebSocketWrapper

# Accept connection
await manager.connect(websocket)

# Send message
await manager.send_personal_message({'type': 'update'}, websocket)

# Broadcast to all
await manager.broadcast({'type': 'notification'})
```

### `test_execution.py`
Handles execution of test steps and test cases.

**Functions:**
- `handle_execute_step(websocket, step_id, db)`: Execute a single test step
- `handle_execute_all_steps(websocket, test_case_id, db)`: Execute all steps in a test case

**Features:**
- Auto-login prepending (Step 1 is automatically prepended to all other steps)
- JSON-only command execution (Python code is never executed)
- Real-time progress updates via WebSocket
- Comprehensive error handling and validation

**Usage:**
```python
from app.websocket import handle_execute_step

# Execute step 5
await handle_execute_step(websocket, step_id=5, db=db_session)
```

### `test_generation.py`
Handles AI-powered test case generation.

**Functions:**
- `handle_generate_test_case(websocket, description, db)`: Generate test case from natural language

**Features:**
- Real-time progress updates (avoids HTTP timeout issues)
- AI-powered step generation
- Automatic database persistence
- Redirect URL generation

**Usage:**
```python
from app.websocket import handle_generate_test_case

# Generate test case
await handle_generate_test_case(
    websocket=websocket,
    description="Test login functionality",
    db=db_session
)
```

## WebSocket Events

### Client → Server

#### Execute Step
```json
{
  "type": "execute_step",
  "step_id": 5
}
```

#### Execute All Steps
```json
{
  "type": "execute_all",
  "test_case_id": 1
}
```

#### Generate Test Case
```json
{
  "type": "generate_test_case",
  "description": "Test login functionality"
}
```

### Server → Client

#### Execution Started
```json
{
  "type": "execution_started",
  "step_id": 5
}
```

#### Status Update
```json
{
  "type": "status_update",
  "step_id": 5,
  "status": "running",
  "message": "Executing Step 1 (Login) + Step 5..."
}
```

#### Execution Complete
```json
{
  "type": "execution_complete",
  "step_id": 5,
  "status": "passed",
  "message": "Step executed successfully"
}
```

#### Generation Progress
```json
{
  "type": "generation_progress",
  "step": 2,
  "total": 4,
  "message": "Generating test steps with AI...",
  "progress": 30
}
```

#### Generation Complete
```json
{
  "type": "generation_complete",
  "success": true,
  "test_case_id": 1,
  "test_case_name": "Generated Test Case - 2026-01-13 10:30",
  "steps_count": 17,
  "redirect_url": "/test-case/1"
}
```

#### Error
```json
{
  "type": "execution_error",
  "error": "Step not found",
  "step_id": 5
}
```

## Security Considerations

### JSON-Only Execution
**CRITICAL**: This module ONLY executes JSON commands, NEVER Python code.

- The `selenium_script_json` field must contain valid JSON command arrays
- Python code detection is performed before execution
- If Python code is detected, execution is aborted with an error

### Validation
All commands are validated before execution:
- Must be a list of dictionaries
- Each command must have an 'action' field
- Python code indicators are checked and rejected

## Error Handling

All functions include comprehensive error handling:
- Database errors are caught and reported
- Selenium errors are caught and logged
- Validation errors are caught before execution
- All errors are sent to the client via WebSocket

## Dependencies

- `fastapi`: WebSocket support
- `sqlalchemy`: Database operations
- `app.models`: Database models
- `app.services.selenium_service`: Selenium execution
- `app.services.ai_service`: AI-powered generation

## Migration from Old Code

The old `websocket_handler.py` file is kept for backward compatibility but is deprecated.

**Old code:**
```python
from app.websocket_handler import handle_execute_step
```

**New code:**
```python
from app.websocket import handle_execute_step
```

## Testing

To test WebSocket functionality:

1. Start the backend server
2. Connect to WebSocket endpoint: `ws://localhost:8000/ws/execute-step`
3. Send test messages and verify responses

## Future Enhancements

- [ ] Connection pooling for multiple clients
- [ ] Rate limiting for WebSocket connections
- [ ] Authentication/authorization for WebSocket connections
- [ ] Compression for large messages
- [ ] Reconnection handling on client side
