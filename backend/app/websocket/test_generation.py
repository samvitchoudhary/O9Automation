"""
Test Generation Handlers

This module handles test case generation from natural language descriptions.
It uses AI to generate test cases and provides real-time progress updates
via WebSocket to avoid timeout issues.

Author: O9 Automation Team
Date: 2026-01-13
"""

from fastapi import WebSocket
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus
from app.services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)


async def handle_generate_test_case(websocket: WebSocket, description: str, db: Session):
    """
    Generate test case from natural language description with real-time progress updates.
    
    This handler creates a new test case and generates test steps using AI.
    It uses WebSocket for real-time progress updates to avoid HTTP timeout issues
    that occur with long-running AI generation operations.
    
    Args:
        websocket (WebSocket): The WebSocket connection for real-time updates
        description (str): Natural language description of the test case
        db (Session): Database session
        
    Emits:
        generation_progress: Progress updates during generation (multiple times)
        generation_complete: When generation finishes successfully
        generation_error: If generation fails
        
    Flow:
        1. Create test case record in database
        2. Generate test steps using AI service (slow operation)
        3. Save all steps to database
        4. Send completion message with redirect URL
        
    Example:
        >>> # Client sends via WebSocket
        >>> await websocket.send_json({
        ...     'type': 'generate_test_case',
        ...     'description': 'Test login functionality'
        ... })
        >>> 
        >>> # Server responds with progress
        >>> # -> generation_progress: {'step': 1, 'total': 4, 'message': 'Creating test case...', 'progress': 10}
        >>> # -> generation_progress: {'step': 2, 'total': 4, 'message': 'Generating test steps...', 'progress': 30}
        >>> # -> generation_progress: {'step': 3, 'total': 4, 'message': 'Saving steps...', 'progress': 70}
        >>> # -> generation_progress: {'step': 4, 'total': 4, 'message': 'Complete!', 'progress': 100}
        >>> # -> generation_complete: {'test_case_id': 1, 'redirect_url': '/test-case/1'}
    """
    try:
        logger.info(f"\n{'='*80}")
        logger.info(f"GENERATING TEST CASE (WebSocket)")
        logger.info(f"{'='*80}")
        logger.info(f"Description: {description[:200]}...")
        
        # Step 1: Create test case
        await websocket.send_json({
            'type': 'generation_progress',
            'step': 1,
            'total': 4,
            'message': 'Creating test case...',
            'progress': 10
        })
        
        ai_service = AIService()
        
        tc = TestCase(
            name=f"Generated Test Case - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            description=description,
            status=TestCaseStatus.DRAFT,
            requirements=""
        )
        
        db.add(tc)
        db.flush()
        
        logger.info(f"✓ Test case created: ID {tc.id}")
        
        # Step 2: Generate steps with AI (this is the slow part)
        await websocket.send_json({
            'type': 'generation_progress',
            'step': 2,
            'total': 4,
            'message': 'Generating test steps with AI... (this may take 30-60 seconds)',
            'progress': 30
        })
        
        # Generate test case using AI service
        generated_data = ai_service.generate_test_case(description)
        
        logger.info(f"✓ AI generated {len(generated_data.get('steps', []))} steps")
        
        # Step 3: Save steps to database
        await websocket.send_json({
            'type': 'generation_progress',
            'step': 3,
            'total': 4,
            'message': f'Saving {len(generated_data.get("steps", []))} test steps to database...',
            'progress': 70
        })
        
        steps_created = 0
        for step_data in generated_data.get("steps", []):
            step = TestStep(
                test_case_id=tc.id,
                step_number=step_data.get("step_number", 0),
                description=step_data.get("description", ""),
                expected_result=step_data.get("expected_result", ""),
                transaction_code=step_data.get("transaction_code"),
                status=TestStepStatus.NOT_STARTED
            )
            db.add(step)
            steps_created += 1
        
        db.commit()
        db.refresh(tc)
        
        logger.info(f"✓ Committed {steps_created} steps to database")
        
        # Step 4: Complete
        await websocket.send_json({
            'type': 'generation_progress',
            'step': 4,
            'total': 4,
            'message': 'Complete! Redirecting...',
            'progress': 100
        })
        
        logger.info(f"\n{'='*80}")
        logger.info(f"✓ TEST CASE GENERATION COMPLETE")
        logger.info(f"  Test Case ID: {tc.id}")
        logger.info(f"  Name: {tc.name}")
        logger.info(f"  Steps: {steps_created}")
        logger.info(f"{'='*80}\n")
        
        # Send success with redirect info
        await websocket.send_json({
            'type': 'generation_complete',
            'success': True,
            'test_case_id': tc.id,
            'test_case_name': tc.name,
            'steps_count': steps_created,
            'redirect_url': f'/test-case/{tc.id}'
        })
        
    except Exception as e:
        db.rollback()
        logger.error(f"\n✗ ERROR GENERATING TEST CASE: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        await websocket.send_json({
            'type': 'generation_error',
            'success': False,
            'error': f'Failed to generate test case: {str(e)}'
        })
