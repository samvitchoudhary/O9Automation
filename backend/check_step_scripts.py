"""
Check what scripts are stored for each test step
This helps verify that JSON scripts are correct and don't have navigate for Step 2+
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

# Get all steps ordered by step number
steps = db_session.query(TestStep).order_by(TestStep.step_number).all()

print("=" * 80)
print("TEST STEP SCRIPTS VERIFICATION")
print("=" * 80)

for step in steps:
    print(f"\n{'='*80}")
    print(f"Step {step.step_number}: {step.description[:60] if step.description else 'N/A'}")
    print(f"{'='*80}")
    
    if step.selenium_script_json:
        try:
            commands = json.loads(step.selenium_script_json)
            print(f"✓ Has JSON script")
            print(f"  Number of commands: {len(commands)}")
            
            if commands:
                first_cmd = commands[0]
                print(f"  First command: {first_cmd.get('action')}")
                print(f"  Description: {first_cmd.get('description', 'N/A')[:50]}")
                
                if first_cmd.get('action') == 'navigate':
                    url = first_cmd.get('url', 'N/A')
                    print(f"  Navigate URL: {url}")
                    if step.step_number > 1:
                        print(f"  ⚠️  WARNING: Step {step.step_number} should NOT have navigate action!")
                    else:
                        print(f"  ✓ Correct: Step 1 should have navigate")
                else:
                    if step.step_number == 1:
                        print(f"  ⚠️  WARNING: Step 1 should have navigate action!")
                    else:
                        print(f"  ✓ Correct: Step {step.step_number} correctly has no navigate")
                
                # Show all commands
                print(f"\n  All commands:")
                for i, cmd in enumerate(commands[:10], 1):  # Show first 10
                    action = cmd.get('action', 'unknown')
                    desc = cmd.get('description', '')[:40]
                    print(f"    {i}. {action:12} - {desc}")
                
                if len(commands) > 10:
                    print(f"    ... and {len(commands) - 10} more commands")
            
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON: {e}")
            print(f"  JSON preview: {step.selenium_script_json[:200]}...")
        except Exception as e:
            print(f"✗ Error parsing: {e}")
    else:
        print("✗ No JSON script")
    
    if step.selenium_script:
        print(f"\n  Has Python script (for display): {len(step.selenium_script)} chars")
        if 'driver.get(' in step.selenium_script and step.step_number > 1:
            print(f"  ⚠️  Python script has driver.get() - this is OK for display, but JSON should not have navigate")

db_session.close()
print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)

