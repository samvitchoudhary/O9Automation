"""
Diagnostic script to check what scripts are stored in the database
Shows Python scripts (for display) vs JSON scripts (for execution)
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import TestStep
from app.database import DATABASE_URL
import json

# Create database session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

print("="*80)
print("STORED SCRIPTS DIAGNOSTIC")
print("="*80)

steps = db.query(TestStep).order_by(TestStep.test_case_id, TestStep.step_number).all()

if not steps:
    print("\nNo test steps found in database.")
    db.close()
    sys.exit(0)

for step in steps:
    print(f"\n{'='*80}")
    print(f"Step {step.step_number} (ID: {step.id}) - Test Case {step.test_case_id}")
    print(f"Description: {step.description[:60] if step.description else 'N/A'}...")
    print(f"{'='*80}")
    
    # Check Python script
    if step.selenium_script:
        print(f"\n📄 PYTHON SCRIPT (for display only):")
        print(f"   Length: {len(step.selenium_script)} characters")
        has_driver_init = 'driver = webdriver.Chrome()' in step.selenium_script
        has_import = 'import' in step.selenium_script or 'from selenium' in step.selenium_script
        print(f"   Contains 'driver = webdriver.Chrome()': {'YES ⚠️' if has_driver_init else 'NO ✓'}")
        print(f"   Contains Python imports: {'YES ⚠️' if has_import else 'NO ✓'}")
        print(f"   First 200 chars: {step.selenium_script[:200]}...")
    else:
        print(f"\n📄 PYTHON SCRIPT: None")
    
    # Check JSON script
    if step.selenium_script_json:
        print(f"\n📋 JSON SCRIPT (for execution):")
        print(f"   Length: {len(step.selenium_script_json)} characters")
        
        try:
            commands = json.loads(step.selenium_script_json)
            print(f"   ✓ Valid JSON")
            print(f"   ✓ Number of commands: {len(commands)}")
            
            if commands:
                first_cmd = commands[0]
                print(f"   First command: {first_cmd.get('action')} - {first_cmd.get('description', 'No description')[:50]}")
                
                # Check for Python code in JSON (shouldn't happen)
                json_str = step.selenium_script_json.lower()
                python_indicators = ['driver = webdriver', 'import ', 'from ', 'def ', 'class ']
                found_indicators = [ind for ind in python_indicators if ind in json_str]
                
                if found_indicators:
                    print(f"   ⚠️  WARNING: JSON contains Python code indicators: {found_indicators}")
                else:
                    print(f"   ✓ No Python code detected in JSON")
                
                # Show all command actions
                actions = [cmd.get('action') for cmd in commands if isinstance(cmd, dict)]
                print(f"   Command actions: {', '.join(actions[:10])}{'...' if len(actions) > 10 else ''}")
                
            else:
                print(f"   ⚠️  WARNING: Empty command list!")
                
        except json.JSONDecodeError as e:
            print(f"   ✗ INVALID JSON: {e}")
            print(f"   First 200 chars: {step.selenium_script_json[:200]}...")
    else:
        print(f"\n📋 JSON SCRIPT: None ⚠️  (Cannot execute without JSON script)")
    
    print(f"\n{'='*80}")

print(f"\n\nSUMMARY:")
print(f"Total steps: {len(steps)}")
steps_with_python = sum(1 for s in steps if s.selenium_script)
steps_with_json = sum(1 for s in steps if s.selenium_script_json)
print(f"Steps with Python script (display): {steps_with_python}/{len(steps)}")
print(f"Steps with JSON script (executable): {steps_with_json}/{len(steps)}")
print(f"Steps ready for execution: {steps_with_json}/{len(steps)}")

db.close()

