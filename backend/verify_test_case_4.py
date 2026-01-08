"""
Verify test case 4 was created correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep
import json

init_db()
db = SessionLocal()

try:
    tc = db.query(TestCase).filter(TestCase.id == 4).first()
    if not tc:
        print("Test case 4 not found!")
        exit(1)
    
    steps = db.query(TestStep).filter(TestStep.test_case_id == 4).order_by(TestStep.step_number).all()
    
    print(f"\n{'='*80}")
    print(f"VERIFYING TEST CASE 4")
    print(f"{'='*80}")
    print(f"\nTest Case: {tc.name}")
    print(f"ID: {tc.id}")
    print(f"Total Steps: {len(steps)}")
    print(f"\n{'='*80}")
    print(f"STEP VERIFICATION")
    print(f"{'='*80}\n")
    
    all_valid = True
    
    for s in steps:
        has_json = bool(s.selenium_script_json)
        valid_json = False
        
        if has_json:
            try:
                commands = json.loads(s.selenium_script_json)
                if isinstance(commands, list) and len(commands) > 0:
                    valid_json = True
                    first_action = commands[0].get('action', 'N/A')
                else:
                    first_action = 'Invalid'
            except:
                first_action = 'Parse Error'
        else:
            first_action = 'No JSON'
        
        status = '✓' if (has_json and valid_json) else '✗'
        if not (has_json and valid_json):
            all_valid = False
        
        print(f"{status} Step {s.step_number:2d}: {s.description[:60]:60s} | JSON: {len(commands) if valid_json else 0} commands | First: {first_action}")
    
    print(f"\n{'='*80}")
    if all_valid:
        print(f"✓ ALL STEPS HAVE VALID JSON COMMANDS")
    else:
        print(f"✗ SOME STEPS HAVE ISSUES")
    print(f"{'='*80}\n")
    
finally:
    db.close()
