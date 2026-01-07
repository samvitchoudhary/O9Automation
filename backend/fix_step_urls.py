"""
Script to fix invalid URLs in existing test step scripts
"""
import os
import json

from app.database import init_db, get_db
from app.models import TestStep

# Initialize database
init_db()

# Get mock URL from environment or use default
mock_url = os.getenv('O9_MOCK_URL', 'http://localhost:3001')

print(f"Fixing URLs in test steps...")
print(f"Using mock URL: {mock_url}")
print("=" * 60)

# Create a database session
db_session = next(get_db())

# Get all steps with selenium scripts
steps = db_session.query(TestStep).filter(TestStep.selenium_script_json.isnot(None)).all()

fixed_count = 0

for step in steps:
    if not step.selenium_script_json:
        continue
        
    try:
        commands = json.loads(step.selenium_script_json)
        modified = False
        
        for command in commands:
            if command.get('action') == 'navigate':
                url = command.get('url')
                
                # Fix bad URLs
                if not url or not url.startswith('http'):
                    print(f"Step {step.id}: Fixing invalid URL '{url}'")
                    command['url'] = mock_url
                    modified = True
                elif url != mock_url and ('localhost' not in url or '3001' not in url):
                    # If it's not the mock URL, update it
                    print(f"Step {step.id}: Updating URL from '{url}' to '{mock_url}'")
                    command['url'] = mock_url
                    modified = True
        
        if modified:
            step.selenium_script_json = json.dumps(commands, indent=2)
            fixed_count += 1
            print(f"  ✓ Updated step {step.id}")
    
    except json.JSONDecodeError as e:
        print(f"Step {step.id}: Invalid JSON - {e}")
    except Exception as e:
        print(f"Step {step.id}: Error - {e}")

if fixed_count > 0:
    db_session.commit()
    print("=" * 60)
    print(f"✓ Fixed {fixed_count} test step(s)")
else:
    print("=" * 60)
    print("No steps needed fixing")

db_session.close()
print("Done!")
