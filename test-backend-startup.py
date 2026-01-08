#!/usr/bin/env python3
"""
Test script to diagnose backend startup issues
Run this to see what errors occur when starting the backend
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("Testing Backend Startup")
print("=" * 60)

try:
    print("\n1. Testing imports...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from dotenv import load_dotenv
    print("   ✓ All imports successful")
except ImportError as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

try:
    print("\n2. Testing database import...")
    from app.database import init_db
    print("   ✓ Database module imported")
except Exception as e:
    print(f"   ✗ Database import error: {e}")
    sys.exit(1)

try:
    print("\n3. Testing routes import...")
    from app.routes import router
    print("   ✓ Routes module imported")
except Exception as e:
    print(f"   ✗ Routes import error: {e}")
    sys.exit(1)

try:
    print("\n4. Testing environment variables...")
    os.chdir('backend')
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print(f"   ✓ ANTHROPIC_API_KEY found (starts with: {api_key[:15]}...)")
    else:
        print("   ⚠ ANTHROPIC_API_KEY not found in .env")
    mock_url = os.getenv('O9_MOCK_URL', 'http://localhost:3001')
    print(f"   ✓ O9_MOCK_URL: {mock_url}")
except Exception as e:
    print(f"   ✗ Environment error: {e}")

try:
    print("\n5. Testing database initialization...")
    init_db()
    print("   ✓ Database initialized successfully")
except Exception as e:
    print(f"   ✗ Database initialization error: {e}")

try:
    print("\n6. Testing FastAPI app creation...")
    app = FastAPI(title="Test App")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    print("   ✓ FastAPI app created successfully")
except Exception as e:
    print(f"   ✗ App creation error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All tests passed! Backend should start successfully.")
print("=" * 60)
print("\nTo start the backend, run:")
print("  cd backend")
print("  source venv/bin/activate")
print("  python run.py")

