"""
API Routes for O9 Test Automation Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import io
import json

from app.database import get_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
from app.services.selenium_executor import get_executor
from app.services.ai_service import AIService
from app.services.excel_service import ExcelService
from app.services.selenium_service import SeleniumService
from app.services.ai_selenium_generator import generate_selenium_script as generate_selenium_script_service
from app.websocket_handler import handle_execute_step, handle_execute_all_steps

router = APIRouter()

# Initialize services
ai_service = AIService()
excel_service = ExcelService()
selenium_service = SeleniumService()


# Pydantic models for request/response
class TestStepCreate(BaseModel):
    step_number: int
    description: str
    expected_result: str
    transaction_code: Optional[str] = None


class TestStepUpdate(BaseModel):
    step_number: Optional[int] = None
    description: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    status: Optional[str] = None
    transaction_code: Optional[str] = None


class TestCaseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    steps: List[TestStepCreate] = []


class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None


class GenerateTestCaseRequest(BaseModel):
    prompt: str


class TestStepResponse(BaseModel):
    id: int
    test_case_id: int
    step_number: int
    description: str
    expected_result: str
    actual_result: Optional[str]
    status: str
    transaction_code: Optional[str]
    selenium_script: Optional[str] = None
    selenium_script_json: Optional[str] = None
    execution_status: Optional[str] = None
    execution_time_ms: Optional[int] = None
    last_executed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TestCaseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    requirements: Optional[str]
    test_case_version: int
    steps: List[TestStepResponse] = []

    class Config:
        from_attributes = True


@router.post("/api/test-cases/generate", response_model=TestCaseResponse)
async def generate_test_case(
    request: GenerateTestCaseRequest,
    db: Session = Depends(get_db)
):
    """Generate a test case from a natural language prompt"""
    try:
        # Generate test case using AI
        generated_data = ai_service.generate_test_case(request.prompt)
        
        # Create test case in database
        test_case = TestCase(
            name=generated_data["test_case_name"],
            description=generated_data.get("description", ""),
            requirements=generated_data.get("requirements", ""),
            status=TestCaseStatus.DRAFT
        )
        db.add(test_case)
        db.flush()  # Get the ID
        
        # Create test steps
        for step_data in generated_data.get("steps", []):
            step = TestStep(
                test_case_id=test_case.id,
                step_number=step_data.get("step_number", 0),
                description=step_data.get("description", ""),
                expected_result=step_data.get("expected_result", ""),
                transaction_code=step_data.get("transaction_code"),
                status=TestStepStatus.NOT_STARTED
            )
            db.add(step)
        
        db.commit()
        db.refresh(test_case)
        
        return test_case
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating test case: {str(e)}"
        )


@router.get("/api/test-cases", response_model=List[TestCaseResponse])
async def get_test_cases(
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all test cases with optional filtering"""
    query = db.query(TestCase)
    
    # Apply status filter
    if status_filter:
        try:
            status_enum = TestCaseStatus(status_filter)
            query = query.filter(TestCase.status == status_enum)
        except ValueError:
            pass  # Invalid status, ignore filter
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (TestCase.name.ilike(search_term)) |
            (TestCase.description.ilike(search_term))
        )
    
    test_cases = query.order_by(TestCase.created_at.desc()).all()
    return test_cases


@router.get("/api/test-cases/{test_case_id}", response_model=TestCaseResponse)
async def get_test_case(test_case_id: int, db: Session = Depends(get_db)):
    """Get a specific test case by ID"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    return test_case


@router.put("/api/test-cases/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(
    test_case_id: int,
    update_data: TestCaseUpdate,
    db: Session = Depends(get_db)
):
    """Update a test case"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    # Update fields
    if update_data.name is not None:
        test_case.name = update_data.name
    if update_data.description is not None:
        test_case.description = update_data.description
    if update_data.requirements is not None:
        test_case.requirements = update_data.requirements
    if update_data.assigned_to is not None:
        test_case.assigned_to = update_data.assigned_to
    if update_data.status is not None:
        try:
            test_case.status = TestCaseStatus(update_data.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {update_data.status}"
            )
    
    test_case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(test_case)
    
    return test_case


@router.post("/api/test-cases/{test_case_id}/approve", response_model=TestCaseResponse)
async def approve_test_case(test_case_id: int, db: Session = Depends(get_db)):
    """Approve a test case"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    test_case.status = TestCaseStatus.APPROVED
    test_case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(test_case)
    
    return test_case


@router.delete("/api/test-cases/{test_case_id}")
async def delete_test_case(test_case_id: int, db: Session = Depends(get_db)):
    """Delete a test case"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    db.delete(test_case)
    db.commit()
    
    return {"message": "Test case deleted successfully"}


@router.put("/api/test-cases/{test_case_id}/steps/{step_id}")
async def update_test_step(
    test_case_id: int,
    step_id: int,
    update_data: TestStepUpdate,
    db: Session = Depends(get_db)
):
    """Update a test step"""
    step = db.query(TestStep).filter(
        TestStep.id == step_id,
        TestStep.test_case_id == test_case_id
    ).first()
    
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test step not found"
        )
    
    # Update fields
    if update_data.step_number is not None:
        step.step_number = update_data.step_number
    if update_data.description is not None:
        step.description = update_data.description
    if update_data.expected_result is not None:
        step.expected_result = update_data.expected_result
    if update_data.actual_result is not None:
        step.actual_result = update_data.actual_result
    if update_data.status is not None:
        try:
            step.status = TestStepStatus(update_data.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {update_data.status}"
            )
    if update_data.transaction_code is not None:
        step.transaction_code = update_data.transaction_code
    
    db.commit()
    db.refresh(step)
    
    return step


@router.post("/api/test-cases/{test_case_id}/steps")
async def create_test_step(
    test_case_id: int,
    step_data: TestStepCreate,
    db: Session = Depends(get_db)
):
    """Create a new test step"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    step = TestStep(
        test_case_id=test_case_id,
        step_number=step_data.step_number,
        description=step_data.description,
        expected_result=step_data.expected_result,
        transaction_code=step_data.transaction_code,
        status=TestStepStatus.NOT_STARTED
    )
    
    db.add(step)
    db.commit()
    db.refresh(step)
    
    return step


@router.delete("/api/test-cases/{test_case_id}/steps/{step_id}")
async def delete_test_step(
    test_case_id: int,
    step_id: int,
    db: Session = Depends(get_db)
):
    """Delete a test step"""
    step = db.query(TestStep).filter(
        TestStep.id == step_id,
        TestStep.test_case_id == test_case_id
    ).first()
    
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test step not found"
        )
    
    db.delete(step)
    db.commit()
    
    return {"message": "Test step deleted successfully"}


@router.get("/api/test-cases/{test_case_id}/export-excel")
async def export_test_case_excel(test_case_id: int, db: Session = Depends(get_db)):
    """Export a test case to Excel format"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    # Generate Excel workbook
    wb = excel_service.generate_excel([test_case])
    
    # Save to bytes
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Return as file download
    filename = f"test_case_{test_case_id}_{test_case.name.replace(' ', '_')}.xlsx"
    
    return StreamingResponse(
        io.BytesIO(output.read()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/api/test-cases/{test_case_id}/generate-selenium")
async def generate_selenium_script(test_case_id: int, db: Session = Depends(get_db)):
    """Generate Selenium script for a test case"""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )
    
    script = selenium_service.generate_selenium_script(test_case)
    
    # Return as text file download
    return StreamingResponse(
        io.BytesIO(script.encode('utf-8')),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=test_{test_case_id}_{test_case.name.replace(' ', '_')}.py"}
    )


@router.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total = db.query(TestCase).count()
    approved = db.query(TestCase).filter(TestCase.status == TestCaseStatus.APPROVED).count()
    in_progress = db.query(TestCase).filter(TestCase.status == TestCaseStatus.IN_PROGRESS).count()
    completed = db.query(TestCase).filter(TestCase.status == TestCaseStatus.COMPLETED).count()
    failed = db.query(TestCase).filter(TestCase.status == TestCaseStatus.FAILED).count()
    draft = db.query(TestCase).filter(TestCase.status == TestCaseStatus.DRAFT).count()
    
    return {
        "total": total,
        "draft": draft,
        "approved": approved,
        "in_progress": in_progress,
        "completed": completed,
        "failed": failed
    }


# Selenium execution endpoints
@router.post("/api/test-steps/{step_id}/generate-selenium")
async def generate_selenium_for_step(step_id: int, db: Session = Depends(get_db)):
    """Generate Selenium script for a specific test step"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"=== Starting generate-selenium for step {step_id} ===")
    
    try:
        # Get the step
        logger.info(f"Fetching step {step_id} from database...")
        step = db.query(TestStep).filter(TestStep.id == step_id).first()
        
        if not step:
            logger.error(f"Step {step_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Test step not found"
            )
        
        logger.info(f"Step found: {step.description[:50] if step.description else 'No description'}...")
        
        # Check required fields
        if not step.description or not step.expected_result:
            logger.error(f"Step {step_id} missing description or expected result")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Step must have both description and expected result"
            )
        
        # Generate scripts
        logger.info(f"Calling generate_selenium_script_service...")
        scripts = generate_selenium_script_service(step.description, step.expected_result, step.step_number)
        logger.info(f"Scripts generated successfully")
        logger.info(f"Script keys: {list(scripts.keys())}")
        logger.info(f"Python script length: {len(scripts.get('selenium_script', ''))}")
        logger.info(f"JSON script length: {len(scripts.get('selenium_script_json', ''))}")
        
        # CRITICAL: Verify JSON is valid before saving
        json_script = scripts.get('selenium_script_json')
        if not json_script:
            logger.error(f"AI did not generate JSON script")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI failed to generate JSON script"
            )
        
        try:
            json_commands = json.loads(json_script)
            if not isinstance(json_commands, list):
                raise ValueError("JSON script must be an array")
            
            # Validate each command has required fields
            for idx, cmd in enumerate(json_commands):
                if not isinstance(cmd, dict):
                    raise ValueError(f"Command {idx+1} is not a JSON object")
                if 'action' not in cmd:
                    raise ValueError(f"Command {idx+1} missing 'action' field")
            
            logger.info(f"✓ JSON validation passed - {len(json_commands)} commands")
            
            # SECURITY CHECK: Ensure it's not Python code
            json_lower = json_script.lower()
            python_indicators = ['import ', 'from ', 'driver = webdriver', 'def ', 'class ', 'webdriver.', 'by.', 'find_element']
            found_python = []
            for indicator in python_indicators:
                if indicator in json_lower:
                    found_python.append(indicator)
                    logger.warning(f"⚠️  JSON contains Python indicator '{indicator}' - this should not happen")
            
            # CRITICAL: If Python code detected, reject the generation
            if found_python:
                logger.error(f"✗ FATAL: Python code detected in JSON script! Indicators: {found_python}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI generated Python code instead of JSON commands. Please try regenerating. Detected: {', '.join(found_python)}"
                )
            
        except json.JSONDecodeError as e:
            logger.error(f"Generated JSON is invalid: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI generated invalid JSON: {str(e)}"
            )
        except ValueError as e:
            logger.error(f"JSON validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid JSON format: {str(e)}"
            )
        
        # CRITICAL FINAL CHECK: Verify JSON before saving
        # Double-check that selenium_script_json is actually JSON, not Python
        final_json_check = scripts['selenium_script_json'].lower()
        final_python_indicators = ['import ', 'from ', 'driver = webdriver', 'def ', 'class ', 'webdriver.', 'by.']
        final_found = [ind for ind in final_python_indicators if ind in final_json_check]
        
        if final_found:
            logger.error(f"✗ FATAL: Python code detected in final JSON check! Rejecting save.")
            logger.error(f"  Indicators found: {final_found}")
            logger.error(f"  JSON preview: {scripts['selenium_script_json'][:200]}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"CRITICAL: Attempted to save Python code as JSON. This should never happen. Please regenerate."
            )
        
        # Update step
        logger.info(f"Updating step in database...")
        step.selenium_script = scripts['selenium_script']  # For display only
        step.selenium_script_json = scripts['selenium_script_json']  # For execution
        db.commit()
        db.refresh(step)
        logger.info(f"✓ Scripts saved to database (Python for display, JSON for execution)")
        logger.info(f"✓ Final validation: JSON is clean, no Python code detected")
        
        # Verify it was saved
        logger.info(f"Verified - DB has script: {bool(step.selenium_script)}, length: {len(step.selenium_script) if step.selenium_script else 0}")
        logger.info(f"Script preview: {step.selenium_script[:100] if step.selenium_script else 'None'}...")
        
        # Return response with explicit data
        response_data = {
            'step_id': step_id,
            'selenium_script': step.selenium_script,  # The Python code
            'selenium_script_json': step.selenium_script_json,  # The JSON commands
            'success': True,
            'message': 'Script generated successfully',
            'script_length': len(step.selenium_script) if step.selenium_script else 0
        }
        
        logger.info(f"Returning response with script length: {response_data['script_length']}")
        logger.info(f"Response keys: {list(response_data.keys())}")
        logger.info(f"=== Returning successful response for step {step_id} ===")
        return response_data
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"=== ERROR in generate-selenium for step {step_id} ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.exception(e)
        
        # Rollback database changes
        db.rollback()
        
        # Return detailed error message
        # Use string concatenation instead of f-string to avoid format specifier errors
        error_detail = "Failed to generate Selenium script: " + str(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )


@router.put("/api/test-steps/{step_id}/update-selenium")
async def update_selenium_script(step_id: int, update_data: dict, db: Session = Depends(get_db)):
    """Update Selenium script for a test step (manual edit)"""
    step = db.query(TestStep).filter(TestStep.id == step_id).first()
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test step not found"
        )
    
    if 'selenium_script' in update_data:
        step.selenium_script = update_data['selenium_script']
    
    if 'selenium_script_json' in update_data:
        step.selenium_script_json = update_data['selenium_script_json']
    
    db.commit()
    
    return {'message': 'Script updated successfully'}


@router.post("/api/test-cases/{test_case_id}/generate-all-selenium")
async def generate_all_selenium(test_case_id: int, db: Session = Depends(get_db)):
    """Generate Selenium scripts for all steps in a test case"""
    steps = db.query(TestStep).filter(
        TestStep.test_case_id == test_case_id
    ).order_by(TestStep.step_number).all()
    
    if not steps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found or has no steps"
        )
    
    generated_count = 0
    for step in steps:
        if not step.selenium_script:  # Only generate if not already exists
            scripts = generate_selenium_script_service(step.description, step.expected_result)
            step.selenium_script = scripts['selenium_script']
            step.selenium_script_json = scripts['selenium_script_json']
            generated_count += 1
    
    db.commit()
    
    return {'message': f'Generated Selenium scripts for {generated_count} steps'}


# WebSocket endpoints
@router.websocket("/ws/execute-step/{step_id}")
async def websocket_execute_step(websocket: WebSocket, step_id: int):
    """WebSocket endpoint for executing a single test step"""
    await websocket.accept()
    db = next(get_db())
    
    try:
        await handle_execute_step(websocket, step_id, db)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({'type': 'execution_error', 'error': str(e)})
    finally:
        db.close()


@router.websocket("/ws/execute-all/{test_case_id}")
async def websocket_execute_all(websocket: WebSocket, test_case_id: int):
    """WebSocket endpoint for executing all steps in a test case"""
    await websocket.accept()
    db = next(get_db())
    
    try:
        await handle_execute_all_steps(websocket, test_case_id, db)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({'type': 'execution_error', 'error': str(e)})
    finally:
        db.close()

