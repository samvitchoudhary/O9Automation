"""
WebSocket handler for real-time test execution updates

DEPRECATED: This file is kept for backward compatibility.
New code should import from app.websocket module instead.

This module re-exports handlers from the refactored websocket module
to maintain backward compatibility with existing code.

Author: O9 Automation Team
Date: 2026-01-13
Last Modified: 2026-01-13 (Refactored into app.websocket module)
"""

# Re-export from new module structure for backward compatibility
from app.websocket import (
    ConnectionManager,
    WebSocketWrapper,
    manager,
    handle_execute_step,
    handle_execute_all_steps,
    handle_generate_test_case
)

# Keep old function for backward compatibility (deprecated)
async def handle_execute_selenium(data: dict, websocket, db):
    """
    DEPRECATED: Use handle_execute_step instead.
    
    This function is kept for backward compatibility but should not be used
    in new code. Use handle_execute_step from app.websocket.test_execution instead.
    
    Args:
        data (dict): Contains 'step_id' key
        websocket: WebSocket connection
        db: Database session
    """
    from app.websocket.test_execution import handle_execute_step
    step_id = data.get('step_id')
    if step_id:
        await handle_execute_step(websocket, step_id, db)
    else:
        await websocket.send_json({
            'type': 'selenium_error',
            'message': 'No step_id provided'
        })
