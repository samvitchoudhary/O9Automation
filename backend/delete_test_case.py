"""
Delete existing test case to start fresh
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase

def delete_test_case(test_case_id=3):
    """Delete a test case and all its steps"""
    
    init_db()
    db = SessionLocal()
    
    try:
        # Find the test case
        test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        
        if not test_case:
            print(f"Test case {test_case_id} not found")
            return False
        
        print(f"\n{'='*80}")
        print(f"DELETING TEST CASE")
        print(f"{'='*80}")
        print(f"ID: {test_case.id}")
        print(f"Name: {test_case.name}")
        print(f"Steps: {len(test_case.steps)}")
        print(f"{'='*80}\n")
        
        # Auto-confirm for script execution
        print("Auto-confirming deletion...")
        
        # Delete (cascade will delete all steps automatically)
        db.delete(test_case)
        db.commit()
        
        print(f"\n✓ Test case {test_case_id} deleted successfully")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    # Allow test case ID as command line argument
    test_case_id = 3  # Default to comprehensive test case
    if len(sys.argv) > 1:
        try:
            test_case_id = int(sys.argv[1])
        except ValueError:
            print(f"Invalid test case ID: {sys.argv[1]}")
            print("Usage: python delete_test_case.py [test_case_id]")
            sys.exit(1)
    
    success = delete_test_case(test_case_id)
    if success:
        print("\n✓ Test case deleted. Ready to create new one.")
    else:
        print("\n✗ Deletion failed")
        sys.exit(1)
