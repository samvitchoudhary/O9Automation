import sys
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

print("="*80)
print("COROUTINE ERROR DIAGNOSTIC")
print("="*80)

# Test 1: Check if anthropic is installed
print("\n1. Checking Anthropic SDK installation...")
try:
    import anthropic
    print(f"   ✓ Anthropic SDK version: {anthropic.__version__}")
except ImportError as e:
    print(f"   ✗ Anthropic SDK not installed: {e}")
    sys.exit(1)

# Test 2: Check API key
print("\n2. Checking API key...")
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"   ✓ API key found: {api_key[:15]}...")
else:
    print(f"   ✗ API key not found")
    sys.exit(1)

# Test 3: Check which client type is being used
print("\n3. Testing synchronous client...")
try:
    client = anthropic.Anthropic(api_key=api_key)
    print(f"   ✓ Synchronous client created: {type(client)}")
except Exception as e:
    print(f"   ✗ Error creating client: {e}")
    traceback.print_exc()

# Test 4: Try a simple API call
print("\n4. Testing simple API call...")
try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print(f"   ✓ API call succeeded")
    print(f"   Response type: {type(message)}")
    print(f"   Content type: {type(message.content)}")
    print(f"   First content type: {type(message.content[0])}")
    print(f"   Response: {message.content[0].text[:50]}...")
except Exception as e:
    print(f"   ✗ API call failed: {e}")
    traceback.print_exc()

# Test 5: Import and test the actual function
print("\n5. Testing actual generate_selenium_script function...")
try:
    from app.services.ai_selenium_generator import generate_selenium_script
    print(f"   ✓ Function imported successfully")
    print(f"   Function type: {type(generate_selenium_script)}")
    
    # Check if it's a coroutine function
    import inspect
    if inspect.iscoroutinefunction(generate_selenium_script):
        print(f"   ✗ WARNING: Function is defined as async! This is the problem!")
    else:
        print(f"   ✓ Function is synchronous (correct)")
    
except ImportError as e:
    print(f"   ✗ Could not import function: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"   ✗ Error: {e}")
    traceback.print_exc()

# Test 6: Try to actually run the function
print("\n6. Testing actual function execution...")
try:
    result = generate_selenium_script(
        step_description="Test step",
        expected_result="Test result"
    )
    print(f"   ✓ Function executed successfully")
    print(f"   Result type: {type(result)}")
    print(f"   Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
except Exception as e:
    print(f"   ✗ Function execution failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    traceback.print_exc()

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)

