"""
Complete script: Delete old test case and create new comprehensive one
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*80)
    print("REGENERATE COMPLETE MOCK O9 TEST CASE")
    print("="*80 + "\n")
    
    # Step 1: Delete existing test case
    print("STEP 1: Deleting existing test case...")
    print("-"*80)
    
    from delete_and_regenerate_test_case import delete_test_case
    success = delete_test_case(test_case_id=1)
    
    if not success:
        print("\nRegeneration cancelled or failed.")
        return
    
    # Step 2: Create new test case
    print("\n\nSTEP 2: Creating new comprehensive test case...")
    print("-"*80)
    
    from create_comprehensive_test_case import create_comprehensive_test_case
    test_case_id = create_comprehensive_test_case()
    
    if test_case_id:
        print("\n" + "="*80)
        print("✓ REGENERATION COMPLETE!")
        print("="*80)
        print("\nNext Steps:")
        print("  1. Restart backend: cd backend && python run.py")
        print(f"  2. Open frontend: http://localhost:5173/test-case/{test_case_id}")
        print("  3. Run Step 1 to test login")
        print("  4. Run remaining steps to test all features")
        print("="*80 + "\n")
    else:
        print("\n✗ Failed to create test case")

if __name__ == "__main__":
    main()
