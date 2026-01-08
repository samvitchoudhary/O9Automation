"""
WebSocket handler for real-time test execution updates
"""
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import TestStep, ExecutionStatus
from app.services.selenium_executor import get_executor
from app.services.selenium_service import SeleniumService
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


class WebSocketWrapper:
    """Wrapper to make WebSocket compatible with SeleniumService"""
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
    
    async def send_message(self, message: dict):
        await self.websocket.send_json(message)


async def handle_execute_selenium(data: dict, websocket: WebSocket, db: Session):
    """
    Execute Selenium test step
    CRITICAL: This function ONLY executes JSON commands, NEVER Python code
    """
    step_id = data.get('step_id')
    
    if not step_id:
        await websocket.send_json({
            'type': 'selenium_error',
            'message': 'No step_id provided'
        })
        return
    
    step = None
    try:
        # Get the test step
        step = db.query(TestStep).filter(TestStep.id == step_id).first()
        
        if not step:
            await websocket.send_json({
                'type': 'selenium_error',
                'message': f'Test step {step_id} not found'
            })
            return
        
        # CRITICAL CHECK 1: Verify JSON script exists
        if not step.selenium_script_json:
            await websocket.send_json({
                'type': 'selenium_error',
                'message': 'No JSON commands found for this step. Please regenerate the script.'
            })
            return
        
        # CRITICAL CHECK 2: Validate it's actually JSON
        try:
            commands = json.loads(step.selenium_script_json)
        except json.JSONDecodeError as e:
            await websocket.send_json({
                'type': 'selenium_error',
                'message': f'Invalid JSON in selenium_script_json: {str(e)}'
            })
            return
        
        # CRITICAL CHECK 3: Verify it's a list
        if not isinstance(commands, list):
            await websocket.send_json({
                'type': 'selenium_error',
                'message': f'JSON commands must be a list, got {type(commands).__name__}'
            })
            return
        
        # CRITICAL CHECK 4: Verify commands structure
        if not commands:
            await websocket.send_json({
                'type': 'selenium_error',
                'message': 'JSON commands list is empty'
            })
            return
        
        for i, cmd in enumerate(commands):
            if not isinstance(cmd, dict):
                await websocket.send_json({
                    'type': 'selenium_error',
                    'message': f'Command {i} is not a dictionary, got {type(cmd).__name__}'
                })
                return
            
            if 'action' not in cmd:
                await websocket.send_json({
                    'type': 'selenium_error',
                    'message': f'Command {i} missing required "action" field'
                })
                return
        
        # CRITICAL CHECK 5: Detect Python code indicators (should never happen)
        json_str = step.selenium_script_json.lower()
        python_indicators = ['import ', 'webdriver.chrome', 'driver = ', 'def ', 'class ', '.quit()']
        
        for indicator in python_indicators:
            if indicator in json_str:
                await websocket.send_json({
                    'type': 'selenium_error',
                    'message': f'FATAL ERROR: Python code detected in JSON field. This should never happen. Please regenerate the script.'
                })
                return
        
        # Log what we're about to execute
        print(f"\n{'='*60}")
        print(f"EXECUTING JSON COMMANDS FOR STEP {step_id}")
        print(f"Number of commands: {len(commands)}")
        print(f"First command: {commands[0].get('action')} - {commands[0].get('description', 'N/A')}")
        print(f"{'='*60}\n")
        
        # Update status
        step.execution_status = ExecutionStatus.RUNNING
        step.last_executed_at = datetime.now()
        db.commit()
        
        await websocket.send_json({
            'type': 'execution_started',
            'step_id': step_id
        })
        
        # Execute commands using SeleniumService
        selenium_service = SeleniumService()
        ws_wrapper = WebSocketWrapper(websocket)
        
        result = await selenium_service.execute_commands(
            commands=commands,
            step_id=step_id,
            websocket=ws_wrapper
        )
        
        # Update step with results
        step.execution_status = ExecutionStatus.PASSED if result['status'] == 'passed' else ExecutionStatus.FAILED
        step.last_executed_at = datetime.now()
        step.error_message = result.get('message', '') if result['status'] != 'passed' else None
        
        # Store logs in error_message if failed, or in a comment
        if result.get('logs'):
            if result['status'] != 'passed':
                step.error_message = result.get('logs', '')
        
        db.commit()
        
        await websocket.send_json({
            'type': 'execution_complete',
            'step_id': step_id,
            'status': result['status'],
            'message': result.get('message', ''),
            'screenshot': result.get('screenshot')
        })
        
    except Exception as e:
        print(f"Error executing Selenium test: {e}")
        import traceback
        traceback.print_exc()
        
        # Update step status
        if step:
            step.execution_status = ExecutionStatus.FAILED
            step.last_executed_at = datetime.now()
            step.error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
            db.commit()
        
        await websocket.send_json({
            'type': 'selenium_error',
            'message': f'Execution failed: {str(e)}'
        })


async def handle_execute_step(websocket: WebSocket, step_id: int, db: Session):
    """Execute a single test step via WebSocket - automatically prepends Step 1 (login) for all steps except Step 1 itself"""
    try:
        # Load step from database
        step = db.query(TestStep).filter(TestStep.id == step_id).first()
        if not step:
            await websocket.send_json({'type': 'execution_error', 'error': 'Step not found'})
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
        
        # CRITICAL: Verify we have JSON commands (not Python script)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"=== EXECUTE STEP {step_id} (Step {step.step_number}) REQUEST ===")
        
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
            except:
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
                    logger.info(f"Step {step.step_number} - Executing Step 1 ({len(step_1_commands)} commands) + Step {step.step_number} ({len(target_commands)} commands) = {len(commands)} total")
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
            
            # VALIDATION: All items must be dicts with 'action' key (validate final commands array)
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
        
        # Create callback for real-time updates
        update_queue = []
        
        def sync_emit(event_type: str, data: dict):
            update_queue.append({'type': event_type, **data})
        
        # CRITICAL: Execute the JSON commands, NOT the Python script
        logger.info(f"Executing JSON commands for step {step_id}")
        
        # Use the new SeleniumService for JSON-only execution
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
        await websocket.send_json({
            'type': 'execution_error',
            'error': str(e)
        })


async def handle_execute_all_steps(websocket: WebSocket, test_case_id: int, db: Session):
    """Execute all steps in a test case sequentially"""
    try:
        # Load all steps for this test case
        steps = db.query(TestStep).filter(
            TestStep.test_case_id == test_case_id
        ).order_by(TestStep.step_number).all()
        
        executor = get_executor()
        
        # Initialize browser once for all steps
        await websocket.send_json({'type': 'progress', 'message': 'Initializing browser...'})
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
        executor.close_browser()
        await websocket.send_json({
            'type': 'all_steps_complete',
            'test_case_id': test_case_id
        })
        
    except Exception as e:
        executor = get_executor()
        executor.close_browser()
        await websocket.send_json({
            'type': 'execution_error',
            'error': str(e)
        })

