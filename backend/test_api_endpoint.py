import sys
import traceback
from app.database import init_db, get_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus
from sqlalchemy.orm import Session

print("="*80)
print("API ENDPOINT DIAGNOSTIC")
print("="*80)

# Initialize database
init_db()

# Get database session
db = next(get_db())

print("\n1. Creating test data...")
try:
    # Create a test case
    test_case = TestCase(
        name="Diagnostic Test Case",
        description="Testing selenium generation",
        status=TestCaseStatus.DRAFT
    )
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    print(f"   ✓ Test case created: ID {test_case.id}")
    
    # Create a test step
    test_step = TestStep(
        test_case_id=test_case.id,
        step_number=1,
        description="Login to the system",
        expected_result="User is logged in",
        status=TestStepStatus.NOT_STARTED
    )
    db.add(test_step)
    db.commit()
    db.refresh(test_step)
    print(f"   ✓ Test step created: ID {test_step.id}")
    
except Exception as e:
    print(f"   ✗ Error creating test data: {e}")
    traceback.print_exc()
    db.close()
    sys.exit(1)

print(f"\n2. Testing the generate_selenium_script service directly...")
try:
    from app.services.ai_selenium_generator import generate_selenium_script
    
    result = generate_selenium_script(
        test_step.description,
        test_step.expected_result
    )
    print(f"   ✓ Service function works")
    print(f"   Result keys: {list(result.keys())}")
    print(f"   Result type: {type(result)}")
    
except Exception as e:
    print(f"   ✗ Service function error: {e}")
    print(f"   Error type: {type(e).__name__}")
    traceback.print_exc()

print(f"\n3. Testing the API route logic (simulating endpoint call)...")
try:
    # Simulate what the API endpoint does
    step = db.query(TestStep).filter(TestStep.id == test_step.id).first()
    print(f"   ✓ Retrieved step from database")
    
    # Generate scripts
    from app.services.ai_selenium_generator import generate_selenium_script
    scripts = generate_selenium_script(step.description, step.expected_result)
    print(f"   ✓ Generated scripts")
    print(f"   Scripts type: {type(scripts)}")
    print(f"   Scripts keys: {list(scripts.keys())}")
    
    # Update step
    step.selenium_script = scripts['selenium_script']
    step.selenium_script_json = scripts['selenium_script_json']
    db.commit()
    print(f"   ✓ Updated step in database")
    
    print(f"\n   SUCCESS! The full flow works.")
    
except Exception as e:
    print(f"   ✗ API route logic error: {e}")
    print(f"   Error type: {type(e).__name__}")
    traceback.print_exc()

print(f"\n4. Testing via FastAPI test client...")
try:
    from fastapi.testclient import TestClient
    from run import app
    
    client = TestClient(app)
    
    response = client.post(
        f'/api/test-steps/{test_step.id}/generate-selenium'
    )
    print(f"   Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ API endpoint works!")
        print(f"   Response keys: {list(data.keys())}")
    else:
        print(f"   ✗ API endpoint returned error")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ✗ Test client error: {e}")
    print(f"   Error type: {type(e).__name__}")
    traceback.print_exc()

# Cleanup
print(f"\n5. Cleaning up test data...")
try:
    db.delete(test_step)
    db.delete(test_case)
    db.commit()
    print(f"   ✓ Cleaned up")
except Exception as e:
    print(f"   ✗ Cleanup error: {e}")

db.close()

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)

