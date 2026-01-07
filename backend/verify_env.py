"""
Environment verification script
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("ENVIRONMENT VERIFICATION")
print("=" * 60)

api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key:
    print(f"✓ ANTHROPIC_API_KEY found")
    print(f"  Key starts with: {api_key[:10]}...")
    print(f"  Key length: {len(api_key)} characters")
    
    # Verify it looks like a valid key
    if api_key.startswith('sk-ant-'):
        print(f"  ✓ Key format looks correct")
    else:
        print(f"  ✗ Warning: Key doesn't start with 'sk-ant-'")
else:
    print("✗ ANTHROPIC_API_KEY not found!")
    print("\nPlease ensure:")
    print("1. You have a .env file in the backend directory")
    print("2. The .env file contains: ANTHROPIC_API_KEY=sk-ant-...")
    print("3. The .env file is in the same directory as run.py")

print("=" * 60)

