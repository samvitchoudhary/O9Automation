"""
Test Execution Handlers

This module handles the execution of test cases and individual test steps.
It manages the entire test execution lifecycle including:
- Auto-login prepending
- Step-by-step execution
- Real-time progress updates
- Error handling and reporting

Author: O9 Automation Team
Date: 2026-01-13
"""

from fastapi import WebSocket
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import TestStep, ExecutionStatus, TestCase
from app.services.selenium_executor import get_executor
from app.services.selenium_service import SeleniumService
from .connection import WebSocketWrapper
import json
import logging

logger = logging.getLogger(__name__)


async def handle_execute_step(websocket: WebSocket, step_id: int, db: Session):
    """
    Execute a single test step via WebSocket.
    
    This handler executes a single test step with auto-login prepended.
    It retrieves the step from the database, prepends the login step if needed,
    executes the combined script, and reports results in real-time.
    
    CRITICAL: This function ONLY executes JSON commands, NEVER Python code.
    The selenium_script_json field must contain valid JSON command arrays.
    
    Args:
        websocket (WebSocket): The WebSocket connection for real-time updates
        step_id (int): ID of the test step to execute
        db (Session): Database session
        
    Emits:
        execution_error: If step not found or validation fails
        status_update: When execution starts
        execution_complete: When execution finishes successfully
        execution_error: If execution fails
        
    Flow:
        1. Load step from database
        2. Load Step 1 (login) from same test case
        3. Validate JSON commands exist
        4. Parse and combine login + target step commands
        5. Validate commands structure (no Python code)
        6. Execute with SeleniumService
        7. Update database with results
        8. Send completion message
        
    Example:
        >>> # Client sends via WebSocket
        >>> await websocket.send_json({'type': 'execute_step', 'step_id': 5})
        >>> 
        >>> # Server responds with progress
        >>> # -> status_update: {'status': 'running', 'message': 'Executing...'}
        >>> # -> execution_complete: {'status': 'passed', 'message': 'Success'}
    """
    try:
        # Load step from database
        step = db.query(TestStep).filter(TestStep.id == step_id).first()
        if not step:
            await websocket.send_json({
                'type': 'execution_error',
                'error': 'Step not found',
                'step_id': step_id
            })
            return
        
        # Get Step 1 (login step) from the same test case
        step_1 = db.query(TestStep).filter(
            TestStep.test_case_id == step.test_case_id,
            TestStep.step_number == 1
        ).first()
        
        if not step_1:
            logger.warning(f"Step 1 (login) not found for test case {step.test_case_id}")
            # Continue without auto-login if Step 1 doesn't exist
        
        # Update status to running
        step.execution_status = ExecutionStatus.RUNNING
        db.commit()
        
        logger.info(f"=== EXECUTE STEP {step_id} (Step {step.step_number}) REQUEST ===")
        
        # CRITICAL: Verify we have JSON commands (not Python script)
        if not step.selenium_script_json:
            logger.error(f"Step {step_id} has no JSON script!")
            await websocket.send_json({
                'type': 'execution_error',
                'error': 'No JSON script found. Please generate a script first.',
                'step_id': step_id
            })
            return
        
        # Parse Step 1 commands (if available)
        step_1_commands = []
        if step_1 and step_1.selenium_script_json:
            try:
                step_1_commands = json.loads(step_1.selenium_script_json)
                if not isinstance(step_1_commands, list):
                    step_1_commands = []
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse Step 1 JSON commands")
                step_1_commands = []
        
        # Parse target step commands
        try:
            target_commands = json.loads(step.selenium_script_json)
            if not isinstance(target_commands, list):
                raise ValueError("JSON script must be an array of commands")
            
            # Determine which commands to execute
            if step.step_number == 1:
                # If this IS Step 1, just run it normally
                commands = target_commands
                logger.info(f"Step 1 (Login) - Executing {len(commands)} commands")
                await websocket.send_json({
                    'type': 'status_update',
                    'step_id': step_id,
                    'status': 'running',
                    'message': 'Executing Step 1 (Login)...'
                })
            else:
                # For any other step, prepend Step 1 commands
                if step_1_commands:
                    commands = step_1_commands.copy()
                    # Add a separator wait
                    commands.append({
                        "action": "wait",
                        "duration": 1,
                        "description": f"--- Login complete, now executing Step {step.step_number} ---"
                    })
                    # Add target step commands
                    commands.extend(target_commands)
                    logger.info(
                        f"Step {step.step_number} - Executing Step 1 ({len(step_1_commands)} commands) + "
                        f"Step {step.step_number} ({len(target_commands)} commands) = {len(commands)} total"
                    )
                    await websocket.send_json({
                        'type': 'status_update',
                        'step_id': step_id,
                        'status': 'running',
                        'message': f'Executing Step 1 (Login) + Step {step.step_number}...'
                    })
                else:
                    # No Step 1 found, just run target step
                    commands = target_commands
                    logger.info(f"Step {step.step_number} - No Step 1 found, executing {len(commands)} commands only")
                    await websocket.send_json({
                        'type': 'status_update',
                        'step_id': step_id,
                        'status': 'running',
                        'message': f'Executing Step {step.step_number}...'
                    })
            
            logger.info(f"Total commands to execute: {len(commands)}")
            
            # SECURITY CHECK: Ensure it's not Python code
            script_lower = step.selenium_script_json.lower()
            python_indicators = [
                'import ', 'from ', 'driver = webdriver', 
                'def ', 'class ', 'print(', '.quit()'
            ]
            
            for indicator in python_indicators:
                if indicator in script_lower:
                    raise ValueError(
                        f"Detected Python code in JSON script (found '{indicator}'). "
                        f"This system ONLY executes JSON commands. "
                        f"The Python script is for display only."
                    )
            
            # VALIDATION: All items must be dicts with 'action' key
            for idx, cmd in enumerate(commands):
                if not isinstance(cmd, dict):
                    raise ValueError(
                        f"Command {idx+1} is not a JSON object (got {type(cmd).__name__})"
                    )
                if 'action' not in cmd:
                    raise ValueError(
                        f"Command {idx+1} missing 'action' field. "
                        f"Valid actions: navigate, click, input, wait, verify_element_present"
                    )
            
            logger.info(f"✓ JSON validation passed for step {step_id}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in step {step_id}: {e}")
            await websocket.send_json({
                'type': 'execution_error',
                'error': f'Invalid JSON format: {str(e)}',
                'step_id': step_id
            })
            return
        except ValueError as e:
            logger.error(f"JSON validation failed for step {step_id}: {e}")
            await websocket.send_json({
                'type': 'execution_error',
                'error': str(e),
                'step_id': step_id
            })
            return
        
        # Debug logging
        logger.info(f"Step description: {step.description[:100] if step.description else 'N/A'}")
        logger.info(f"Step number: {step.step_number}")
        logger.info(f"Has selenium_script (Python - display only): {bool(step.selenium_script)}")
        logger.info(f"Has selenium_script_json (JSON - for execution): {bool(step.selenium_script_json)}")
        logger.info(f"JSON script preview: {step.selenium_script_json[:300]}...")
        
        # CRITICAL: Execute the JSON commands, NOT the Python script
        logger.info(f"Executing JSON commands for step {step_id}")
        
        # Use the SeleniumService for JSON-only execution
        selenium_service = SeleniumService()
        ws_wrapper = WebSocketWrapper(websocket)
        
        result = await selenium_service.execute_commands(
            commands=commands,
            step_id=step_id,
            websocket=ws_wrapper
        )
        
        # Update step in database
        if result['status'] == 'passed':
            step.execution_status = ExecutionStatus.PASSED
            step.actual_result = step.expected_result
        elif result['status'] == 'error':
            step.execution_status = ExecutionStatus.ERROR
        else:
            step.execution_status = ExecutionStatus.FAILED
        
        step.execution_time_ms = None  # SeleniumService doesn't return this yet
        step.error_message = result.get('message', '') if result['status'] != 'passed' else None
        step.last_executed_at = datetime.utcnow()
        db.commit()
        
        # Send final status
        await websocket.send_json({
            'type': 'execution_complete',
            'step_id': step_id,
            'status': result['status'],
            'message': result.get('message', ''),
            'screenshot': result.get('screenshot')
        })
        
    except Exception as e:
        logger.error(f"Error executing step {step_id}: {e}", exc_info=True)
        await websocket.send_json({
            'type': 'execution_error',
            'error': str(e),
            'step_id': step_id
        })


async def handle_execute_all_steps(websocket: WebSocket, test_case_id: int, db: Session):
    """
    Execute all steps in a test case sequentially.
    
    This handler executes all steps in a test case one by one, maintaining
    the browser session between steps (except for the last step).
    
    Args:
        websocket (WebSocket): The WebSocket connection for real-time updates
        test_case_id (int): ID of the test case to execute
        db (Session): Database session
        
    Emits:
        progress: When browser is initialized
        status_update: For each step (multiple times)
        execution_complete: When each step finishes
        all_steps_complete: When all steps are done
        execution_error: If any step fails
        
    Flow:
        1. Load all steps for test case
        2. Initialize browser once
        3. For each step:
           a. Update status to running
           b. Execute step
           c. Update database
           d. Send completion message
        4. Close browser
        5. Send final summary
        
    Example:
        >>> # Client sends via WebSocket
        >>> await websocket.send_json({'type': 'execute_all', 'test_case_id': 1})
        >>> 
        >>> # Server responds with progress for each step
        >>> # -> progress: {'message': 'Initializing browser...'}
        >>> # -> status_update: {'step_id': 1, 'status': 'running'}
        >>> # -> execution_complete: {'step_id': 1, 'status': 'passed'}
        >>> # -> ... (continues for all steps)
        >>> # -> all_steps_complete: {'test_case_id': 1}
    """
    executor = None
    try:
        # Load all steps for this test case
        steps = db.query(TestStep).filter(
            TestStep.test_case_id == test_case_id
        ).order_by(TestStep.step_number).all()
        
        if not steps:
            await websocket.send_json({
                'type': 'execution_error',
                'error': f'No steps found for test case {test_case_id}'
            })
            return
        
        executor = get_executor()
        
        # Initialize browser once for all steps
        await websocket.send_json({
            'type': 'progress',
            'message': 'Initializing browser...'
        })
        executor.initialize_browser()
        
        for idx, step in enumerate(steps):
            # Update status
            step.execution_status = ExecutionStatus.RUNNING
            db.commit()
            await websocket.send_json({
                'type': 'status_update',
                'step_id': step.id,
                'status': 'running'
            })
            
            # Create callback (simplified)
            update_queue = []
            
            def sync_emit(event_type: str, data: dict):
                update_queue.append({'type': event_type, **data})
            
            # Execute
            if step.selenium_script_json:
                # Determine if this is the last step
                is_last_step = (idx == len(steps) - 1)
                
                # Keep browser alive for all steps except the last one
                result = executor.execute_script(
                    step.selenium_script_json, 
                    emit_callback=sync_emit,
                    keep_alive=not is_last_step  # Keep alive except for last step
                )
                
                # Send queued updates
                for update in update_queue:
                    update['step_id'] = step.id
                    await websocket.send_json(update)
                
                # Update database
                if result['status'] == 'passed':
                    step.execution_status = ExecutionStatus.PASSED
                    step.actual_result = step.expected_result
                elif result['status'] == 'error':
                    step.execution_status = ExecutionStatus.ERROR
                else:
                    step.execution_status = ExecutionStatus.FAILED
                
                step.execution_time_ms = result['execution_time_ms']
                step.error_message = result.get('error_message')
                step.last_executed_at = datetime.utcnow()
                db.commit()
                
                # Notify completion
                await websocket.send_json({
                    'type': 'execution_complete',
                    'step_id': step.id,
                    'status': result['status'],
                    'execution_time_ms': result['execution_time_ms'],
                    'error_message': result.get('error_message')
                })
            else:
                await websocket.send_json({
                    'type': 'execution_error',
                    'step_id': step.id,
                    'error': 'No Selenium script found for this step'
                })
        
        # Close browser after all steps
        if executor:
            executor.close_browser()
        await websocket.send_json({
            'type': 'all_steps_complete',
            'test_case_id': test_case_id
        })
        
    except Exception as e:
        logger.error(f"Error executing all steps for test case {test_case_id}: {e}", exc_info=True)
        if executor:
            executor.close_browser()
        await websocket.send_json({
            'type': 'execution_error',
            'error': str(e)
        })
