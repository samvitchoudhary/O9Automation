"""
Fix existing test steps that have navigate actions when they shouldn't
Removes navigate actions from Step 2+ scripts
"""
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db, get_db
from app.models import TestStep

# Initialize database
init_db()

# Create a database session
db_session = next(get_db())

# Get all steps with JSON scripts
steps = db_session.query(TestStep).filter(TestStep.selenium_script_json.isnot(None)).all()

print("=" * 80)
print("FIXING NAVIGATE ACTIONS IN STEP 2+")
print("=" * 80)

fixed_count = 0

for step in steps:
    if not step.selenium_script_json:
        continue
    
    try:
        commands = json.loads(step.selenium_script_json)
        modified = False
        
        # Check if this is Step 2+ and has navigate action
        if step.step_number > 1:
            # Remove all navigate actions
            original_count = len(commands)
            commands = [cmd for cmd in commands if cmd.get('action') != 'navigate']
            
            if len(commands) < original_count:
                removed = original_count - len(commands)
                print(f"\nStep {step.step_number} (ID: {step.id}):")
                print(f"  Removed {removed} navigate action(s)")
                print(f"  Commands: {original_count} → {len(commands)}")
                
                if len(commands) == 0:
                    print(f"  ⚠️  WARNING: No commands remaining after removing navigate!")
                    print(f"  Skipping this step - it needs to be regenerated")
                    continue
                
                modified = True
        
        if modified:
            step.selenium_script_json = json.dumps(commands, indent=2)
            fixed_count += 1
            print(f"  ✓ Fixed")
    
    except json.JSONDecodeError as e:
        print(f"\nStep {step.step_number} (ID: {step.id}): Invalid JSON - {e}")
    except Exception as e:
        print(f"\nStep {step.step_number} (ID: {step.id}): Error - {e}")

if fixed_count > 0:
    db_session.commit()
    print("\n" + "=" * 80)
    print(f"✓ Fixed {fixed_count} test step(s)")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print("No steps needed fixing")
    print("=" * 80)

db_session.close()
print("Done!")

