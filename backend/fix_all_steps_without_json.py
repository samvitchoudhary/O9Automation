"""
Fix all steps that don't have JSON commands by regenerating them
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestStep
from app.services.ai_selenium_generator import generate_selenium_script
import json

def fix_all_steps():
    init_db()
    db = SessionLocal()
    
    try:
        # Find all steps without JSON
        steps_without_json = db.query(TestStep).filter(
            (TestStep.selenium_script_json == None) | 
            (TestStep.selenium_script_json == '')
        ).all()
        
        if not steps_without_json:
            print("\n✓ All steps have JSON commands!")
            return
        
        print(f"\n{'='*80}")
        print(f"FIXING STEPS WITHOUT JSON COMMANDS")
        print(f"{'='*80}")
        print(f"Found {len(steps_without_json)} steps without JSON")
        print(f"{'='*80}\n")
        
        fixed_count = 0
        error_count = 0
        
        for step in steps_without_json:
            try:
                print(f"\nFixing Step {step.id} (Step {step.step_number}): {step.description[:50]}...")
                
                # Regenerate the script
                result = generate_selenium_script(
                    step_description=step.description,
                    expected_result=step.expected_result,
                    step_number=step.step_number
                )
                
                # Validate
                if 'selenium_script_json' not in result:
                    print(f"  ✗ AI did not return JSON")
                    error_count += 1
                    continue
                
                commands = json.loads(result['selenium_script_json'])
                if not isinstance(commands, list):
                    print(f"  ✗ Invalid JSON format")
                    error_count += 1
                    continue
                
                # Update
                step.selenium_script = result['selenium_script']
                step.selenium_script_json = result['selenium_script_json']
                
                print(f"  ✓ Fixed! Generated {len(commands)} commands")
                fixed_count += 1
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                error_count += 1
                continue
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ Fixed {fixed_count} steps")
        if error_count > 0:
            print(f"✗ {error_count} steps had errors")
        print(f"{'='*80}\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_all_steps()
