"""
Delete existing test case and regenerate with all features
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep
import json

def delete_test_case(test_case_id=1):
    init_db()
    db = SessionLocal()
    
    try:
        # Find test case
        tc = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        
        if not tc:
            print(f"Test case {test_case_id} not found!")
            return False
        
        print(f"\n{'='*80}")
        print(f"DELETING TEST CASE")
        print(f"{'='*80}")
        print(f"ID: {tc.id}")
        print(f"Name: {tc.name}")
        print(f"Description: {tc.description or 'N/A'}")
        
        # Count steps
        steps = db.query(TestStep).filter(TestStep.test_case_id == tc.id).all()
        print(f"Steps to delete: {len(steps)}")
        print(f"{'='*80}")
        
        # Auto-confirm for script execution
        print("\nAuto-confirming deletion...")
        
        # Delete all steps first
        if steps:
            print(f"\nDeleting {len(steps)} steps...")
            for step in steps:
                db.delete(step)
        
        # Delete test case
        print(f"Deleting test case...")
        db.delete(tc)
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ Test case {test_case_id} deleted successfully!")
        print(f"{'='*80}\n")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error deleting test case: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    delete_test_case()
