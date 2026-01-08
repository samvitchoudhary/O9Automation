"""
Fix Step 17 by regenerating its script properly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestStep
from app.services.ai_selenium_generator import generate_selenium_script
import json

def fix_step_17():
    init_db()
    db = SessionLocal()
    
    try:
        # Find Step 17 (could be in any test case)
        step = db.query(TestStep).filter(TestStep.step_number == 17).first()
        
        if not step:
            print("Step 17 not found!")
            return
        
        print(f"\n{'='*80}")
        print(f"FIXING STEP 17")
        print(f"{'='*80}")
        print(f"Step ID: {step.id}")
        print(f"Test Case ID: {step.test_case_id}")
        print(f"Description: {step.description}")
        print(f"Expected: {step.expected_result}")
        print(f"{'='*80}\n")
        
        # Regenerate the script
        print("Calling AI to generate JSON commands...")
        result = generate_selenium_script(
            step_description=step.description,
            expected_result=step.expected_result,
            step_number=step.step_number
        )
        
        # Validate the result
        if 'selenium_script_json' not in result:
            raise ValueError("AI did not return selenium_script_json")
        if 'selenium_script' not in result:
            raise ValueError("AI did not return selenium_script")
        
        # Validate JSON
        try:
            commands = json.loads(result['selenium_script_json'])
            if not isinstance(commands, list):
                raise ValueError("JSON commands must be a list")
            print(f"✓ Generated {len(commands)} JSON commands")
            if commands:
                print(f"  First command: {commands[0].get('action')}")
        except Exception as e:
            raise ValueError(f"Invalid JSON generated: {str(e)}")
        
        # Update the step
        step.selenium_script = result['selenium_script']
        step.selenium_script_json = result['selenium_script_json']
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ Step 17 Fixed!")
        print(f"{'='*80}")
        print(f"JSON commands saved: {len(result['selenium_script_json'])} characters")
        print(f"Python display saved: {len(result['selenium_script'])} characters")
        print(f"Commands count: {len(commands)}")
        print(f"{'='*80}\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_step_17()
