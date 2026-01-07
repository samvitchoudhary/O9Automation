"""
Test script generation to verify format specifier fix
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db
from app.services.ai_selenium_generator import generate_selenium_script

# Initialize database
init_db()

print("=" * 80)
print("TESTING SCRIPT GENERATION")
print("=" * 80)

try:
    print("\n1. Testing Step 1 (Login) generation...")
    result = generate_selenium_script(
        step_description="Login to the O9 tenant",
        expected_result="Login successful and main O9 dashboard loads",
        step_number=1
    )
    
    print("✓ Generation successful!")
    print(f"  Python script length: {len(result['selenium_script'])} chars")
    print(f"  JSON script length: {len(result['selenium_script_json'])} chars")
    
    # Parse and show JSON preview
    import json
    json_commands = json.loads(result['selenium_script_json'])
    print(f"  Number of JSON commands: {len(json_commands)}")
    if json_commands:
        print(f"  First command: {json_commands[0].get('action')}")
        if json_commands[0].get('action') == 'navigate':
            print(f"    URL: {json_commands[0].get('url')}")
    
    print("\n2. Testing Step 2 (Navigation) generation...")
    result2 = generate_selenium_script(
        step_description="Navigate to Demand Analyst > System Forecast > Generate Forecast > Details",
        expected_result="Forecast analysis page loads with widgets and filters",
        step_number=2
    )
    
    print("✓ Generation successful!")
    print(f"  Python script length: {len(result2['selenium_script'])} chars")
    print(f"  JSON script length: {len(result2['selenium_script_json'])} chars")
    
    json_commands2 = json.loads(result2['selenium_script_json'])
    print(f"  Number of JSON commands: {len(json_commands2)}")
    if json_commands2:
        first_action = json_commands2[0].get('action')
        print(f"  First command: {first_action}")
        if first_action == 'navigate':
            print(f"    ⚠️  WARNING: Step 2 should NOT have navigate action!")
        else:
            print(f"    ✓ Correct: Step 2 starts with {first_action} (no navigate)")
    
    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED - No format specifier errors!")
    print("=" * 80)
    
except ValueError as e:
    if "Invalid format specifier" in str(e):
        print(f"\n✗ Format specifier error detected: {e}")
        print("  This means there are still unescaped braces in the prompt!")
        import traceback
        traceback.print_exc()
    else:
        print(f"\n✗ ValueError: {e}")
        import traceback
        traceback.print_exc()
except Exception as e:
    print(f"\n✗ Generation failed: {e}")
    import traceback
    traceback.print_exc()

