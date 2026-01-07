"""
Test script for Selenium generation
"""
import logging
from app.services.ai_selenium_generator import generate_selenium_script

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("Testing Selenium script generation...")
print("=" * 60)

try:
    result = generate_selenium_script(
        step_description="Login to the o9 tenant\n\nUsing the URL, Username, and Password, the user can log into the o9 front-end User Interface.",
        expected_result="Login successful"
    )
    
    print("✓ Generation successful!")
    print("\nPython Script (first 300 chars):")
    print(result['selenium_script'][:300])
    print("\nJSON Script (first 300 chars):")
    print(result['selenium_script_json'][:300])
    
except Exception as e:
    print(f"✗ Generation failed: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)

