"""
Add a guaranteed-to-work test case for Mock O9 Platform
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
import json

def create_working_test():
    init_db()
    db = SessionLocal()
    
    try:
        # Check if exists
        existing = db.query(TestCase).filter(TestCase.name == "Mock O9 - Working Test").first()
        if existing:
            print(f"Test already exists: ID {existing.id}")
            return existing.id
        
        # Create test case
        tc = TestCase(
            name="Mock O9 - Working Test",
            description="Verified working test for Mock O9 Platform",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 running on localhost:3001",
            assigned_to="Test Automation"
        )
        db.add(tc)
        db.flush()
        
        # Step 1: Login with ONLY JSON commands
        step1_json = json.dumps([
            {"action": "navigate", "url": "http://localhost:3001", "description": "Open Mock O9"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "input", "locator_type": "id", "locator_value": "username", "text": "testuser", "description": "Enter username"},
            {"action": "input", "locator_type": "id", "locator_value": "password", "text": "password123", "description": "Enter password"},
            {"action": "click", "locator_type": "id", "locator_value": "login-button", "description": "Click login"},
            {"action": "wait", "duration": 2, "description": "Wait for redirect"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Welcome", "description": "Verify dashboard loaded"}
        ])
        
        step1 = TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to Mock O9\n\nNavigate to http://localhost:3001\nEnter credentials: testuser / password123\nClick login and verify dashboard loads",
            expected_result="Successfully logged in, dashboard displays 'Welcome to O9 Platform'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# This is for display only\n# System executes JSON commands\n# The actual execution uses JSON commands from selenium_script_json",
            selenium_script_json=step1_json
        )
        db.add(step1)
        
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"✓ Working test case created!")
        print(f"  Test Case ID: {tc.id}")
        print(f"  Name: {tc.name}")
        print(f"  Access: http://localhost:5173/test-case/{tc.id}")
        print(f"{'='*60}\n")
        
        return tc.id
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    test_id = create_working_test()
    if test_id:
        print(f"✓ Success! Go to: http://localhost:5173/test-case/{test_id}")
    else:
        print("✗ Failed to create test")
