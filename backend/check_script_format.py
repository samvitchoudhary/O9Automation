"""
Check which steps have Python vs JSON scripts
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestStep
import json

def check_steps():
    init_db()
    db = SessionLocal()
    
    try:
        steps = db.query(TestStep).order_by(TestStep.test_case_id, TestStep.step_number).all()
        
        print(f"\n{'='*80}")
        print(f"CHECKING SCRIPT FORMATS FOR ALL STEPS")
        print(f"{'='*80}\n")
        
        issues_found = []
        
        for step in steps:
            print(f"\nStep {step.id} (Step {step.step_number}): {step.description[:50]}...")
            print(f"{'-'*80}")
            
            # Check if has JSON
            has_json = bool(step.selenium_script_json)
            print(f"  Has JSON: {'✓' if has_json else '✗'}")
            
            if has_json:
                # Validate JSON
                try:
                    commands = json.loads(step.selenium_script_json)
                    if isinstance(commands, list):
                        print(f"  ✓ JSON is valid list with {len(commands)} commands")
                        if commands:
                            print(f"    First: {commands[0].get('action', 'N/A')}")
                            
                            # Check for Python code in JSON
                            json_str = step.selenium_script_json.lower()
                            python_indicators = ['import ', 'from ', 'driver = webdriver', 'def ', 'class ']
                            found_python = [ind for ind in python_indicators if ind in json_str]
                            if found_python:
                                print(f"  ✗ WARNING: Python code detected in JSON!")
                                print(f"    Found: {found_python}")
                                issues_found.append({
                                    'step_id': step.id,
                                    'step_number': step.step_number,
                                    'issue': 'Python code in JSON',
                                    'indicators': found_python
                                })
                    else:
                        print(f"  ✗ JSON is not a list! Type: {type(commands)}")
                        issues_found.append({
                            'step_id': step.id,
                            'step_number': step.step_number,
                            'issue': f'JSON is not a list (got {type(commands).__name__})'
                        })
                except Exception as e:
                    print(f"  ✗ JSON parse error: {e}")
                    issues_found.append({
                        'step_id': step.id,
                        'step_number': step.step_number,
                        'issue': f'JSON parse error: {str(e)}'
                    })
            else:
                print(f"  ⚠ WARNING: No JSON commands! This step will fail.")
                issues_found.append({
                    'step_id': step.id,
                    'step_number': step.step_number,
                    'issue': 'No JSON commands'
                })
            
            # Check if has Python
            has_python = bool(step.selenium_script)
            print(f"  Has Python: {'✓' if has_python else '✗'}")
        
        print(f"\n{'='*80}")
        if issues_found:
            print(f"⚠ ISSUES FOUND: {len(issues_found)}")
            print(f"{'='*80}")
            for issue in issues_found:
                print(f"  Step {issue['step_id']} (Step {issue['step_number']}): {issue['issue']}")
        else:
            print(f"✓ ALL STEPS HAVE VALID JSON COMMANDS")
        print(f"{'='*80}\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_steps()
