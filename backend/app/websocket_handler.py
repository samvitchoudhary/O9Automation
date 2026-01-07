"""
WebSocket handler for real-time test execution updates
"""
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import TestStep, ExecutionStatus
from app.services.selenium_executor import get_executor
import json


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


async def handle_execute_step(websocket: WebSocket, step_id: int, db: Session):
    """Execute a single test step via WebSocket"""
    try:
        # Load step from database
        step = db.query(TestStep).filter(TestStep.id == step_id).first()
        if not step:
            await websocket.send_json({'type': 'execution_error', 'error': 'Step not found'})
            return
        
        # Update status to running
        step.execution_status = ExecutionStatus.RUNNING
        db.commit()
        await websocket.send_json({
            'type': 'status_update',
            'step_id': step_id,
            'status': 'running'
        })
        
        # Get executor
        executor = get_executor()
        
        # Initialize browser if not already initialized
        if not executor.driver or not executor.session_active:
            await websocket.send_json({'type': 'progress', 'message': 'Initializing browser...'})
            executor.initialize_browser()
        
        # CRITICAL: Verify we have JSON commands (not Python script)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"=== EXECUTE STEP {step_id} REQUEST ===")
        
        if not step.selenium_script_json:
            logger.error(f"Step {step_id} has no JSON script!")
            await websocket.send_json({
                'type': 'execution_error',
                'error': 'No JSON script found. Please generate a script first.',
                'step_id': step_id
            })
            return
        
        # CRITICAL CHECK: Verify it's valid JSON and not Python code
        try:
            commands = json.loads(step.selenium_script_json)
            if not isinstance(commands, list):
                raise ValueError("JSON script must be an array of commands")
            
            logger.info(f"Step {step_id} has {len(commands)} JSON commands")
            
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
        
        # Create callback for real-time updates
        update_queue = []
        
        def sync_emit(event_type: str, data: dict):
            update_queue.append({'type': event_type, **data})
        
        # CRITICAL: Execute the JSON commands, NOT the Python script
        logger.info(f"Executing JSON commands for step {step_id}")
        result = executor.execute_script(
            step.selenium_script_json,  # ← JSON commands for execution
            emit_callback=sync_emit,
            keep_alive=False  # Close browser after individual step
        )
        
        # Send queued updates
        for update in update_queue:
            update['step_id'] = step_id
            await websocket.send_json(update)
        
        # Update step in database
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
        
        # Send final status
        await websocket.send_json({
            'type': 'execution_complete',
            'step_id': step_id,
            'status': result['status'],
            'execution_time_ms': result['execution_time_ms'],
            'error_message': result.get('error_message')
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

