"""
Fix sequential execution for comprehensive test case
Add navigation context to each step so they work independently
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestStep
import json

def fix_sequential_execution(test_case_id=3):
    """Update test steps to include proper navigation context"""
    
    init_db()
    db = SessionLocal()
    
    try:
        # Get test case steps
        steps = db.query(TestStep).filter(TestStep.test_case_id == test_case_id).order_by(TestStep.step_number).all()
        
        if not steps:
            print(f"Error: No steps found for test case {test_case_id}")
            print("Run create_comprehensive_test.py first")
            return False
        
        print(f"\n{'='*80}")
        print(f"FIXING SEQUENTIAL EXECUTION FOR {len(steps)} STEPS (Test Case ID: {test_case_id})")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # STEP 2: Add navigation to dashboard
        # ===================================================================
        if len(steps) >= 2:
            step2 = steps[1]  # Index 1 = Step 2
            step2_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/dashboard.html",
                    "description": "Navigate directly to dashboard"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for dashboard to load"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "dashboard-widgets",
                    "description": "Verify dashboard widgets container exists"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "widget",
                    "description": "Verify at least one widget is present"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "sidebar",
                    "description": "Verify navigation sidebar exists"
                }
            ], indent=2)
            step2.selenium_script_json = step2_json
            print("✓ Step 2: Added dashboard navigation")
        
        # ===================================================================
        # STEP 3: Navigate to dashboard, then expand menu
        # ===================================================================
        if len(steps) >= 3:
            step3 = steps[2]
            step3_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/dashboard.html",
                    "description": "Navigate to dashboard"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                    "description": "Click on Demand Analyst menu item"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait for submenu to expand"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "id",
                    "locator_value": "demand-analyst",
                    "description": "Verify Demand Analyst submenu is visible"
                }
            ], indent=2)
            step3.selenium_script_json = step3_json
            print("✓ Step 3: Added dashboard navigation + Demand Analyst")
        
        # ===================================================================
        # STEP 4: Navigate, expand Demand Analyst, expand System Forecast
        # ===================================================================
        if len(steps) >= 4:
            step4 = steps[3]
            step4_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/dashboard.html",
                    "description": "Navigate to dashboard"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                    "description": "Expand Demand Analyst"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait for submenu"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'System Forecast')]",
                    "description": "Click System Forecast submenu"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait for submenu expansion"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "id",
                    "locator_value": "system-forecast",
                    "description": "Verify System Forecast submenu appears"
                }
            ], indent=2)
            step4.selenium_script_json = step4_json
            print("✓ Step 4: Added full navigation path to System Forecast")
        
        # ===================================================================
        # STEP 5: Full path to Generate Forecast
        # ===================================================================
        if len(steps) >= 5:
            step5 = steps[4]
            step5_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/dashboard.html",
                    "description": "Navigate to dashboard"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                    "description": "Expand Demand Analyst"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'System Forecast')]",
                    "description": "Expand System Forecast"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//a[contains(text(), 'Generate Forecast')]",
                    "description": "Click Generate Forecast option"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait for submenu"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "id",
                    "locator_value": "generate-forecast",
                    "description": "Verify Generate Forecast submenu visible"
                }
            ], indent=2)
            step5.selenium_script_json = step5_json
            print("✓ Step 5: Added full path to Generate Forecast")
        
        # ===================================================================
        # STEP 6: Navigate to Forecast Details page
        # ===================================================================
        if len(steps) >= 6:
            step6 = steps[5]
            step6_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/forecast.html",
                    "description": "Navigate directly to forecast details page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "verify_text",
                    "locator_type": "tag",
                    "locator_value": "h1",
                    "expected_text": "Generate Forecast",
                    "description": "Verify forecast page heading"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "scope-filters",
                    "description": "Verify scope filters section exists"
                }
            ], indent=2)
            step6.selenium_script_json = step6_json
            print("✓ Step 6: Direct navigation to forecast page")
        
        # ===================================================================
        # STEP 7: Navigate to forecast page, apply iteration filter
        # ===================================================================
        if len(steps) >= 7:
            step7 = steps[6]
            step7_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/forecast.html",
                    "description": "Navigate to forecast page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "id",
                    "locator_value": "forecast-iteration",
                    "description": "Click Forecast Iteration dropdown"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//select[@id='forecast-iteration']/option[@value='short-term']",
                    "description": "Select 'Short Term' option"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait after selection"
                }
            ], indent=2)
            step7.selenium_script_json = step7_json
            print("✓ Step 7: Added forecast page navigation + filter")
        
        # ===================================================================
        # STEP 8: Navigate to forecast page, apply region filter
        # ===================================================================
        if len(steps) >= 8:
            step8 = steps[7]
            step8_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/forecast.html",
                    "description": "Navigate to forecast page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "id",
                    "locator_value": "region",
                    "description": "Click Region dropdown"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//select[@id='region']/option[@value='na']",
                    "description": "Select 'North America' option"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait after selection"
                }
            ], indent=2)
            step8.selenium_script_json = step8_json
            print("✓ Step 8: Added forecast page navigation + region filter")
        
        # ===================================================================
        # STEP 9: Navigate to forecast page, verify widgets
        # ===================================================================
        if len(steps) >= 9:
            step9 = steps[8]
            step9_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/forecast.html",
                    "description": "Navigate to forecast page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page and widgets to load"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "review-widget",
                    "description": "Verify Review Widget is present"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "gap-widget",
                    "description": "Verify Gap Widget is present"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "data-table",
                    "description": "Verify data table exists in Gap Widget"
                }
            ], indent=2)
            step9.selenium_script_json = step9_json
            print("✓ Step 9: Added forecast page navigation + widget verification")
        
        # ===================================================================
        # STEP 10: Navigate to BOM Setup
        # ===================================================================
        if len(steps) >= 10:
            step10 = steps[9]
            step10_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/bom-setup.html",
                    "description": "Navigate directly to BOM Setup page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "verify_text",
                    "locator_type": "tag",
                    "locator_value": "h1",
                    "expected_text": "BOM Setup",
                    "description": "Verify BOM Setup page loaded"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "scope-filters",
                    "description": "Verify global filters section"
                }
            ], indent=2)
            step10.selenium_script_json = step10_json
            print("✓ Step 10: Direct navigation to BOM Setup")
        
        # ===================================================================
        # STEP 11: Navigate to BOM, apply filters
        # ===================================================================
        if len(steps) >= 11:
            step11 = steps[10]
            step11_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/bom-setup.html",
                    "description": "Navigate to BOM Setup page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "click",
                    "locator_type": "id",
                    "locator_value": "version-bom",
                    "description": "Click Version dropdown"
                },
                {
                    "action": "click",
                    "locator_type": "xpath",
                    "locator_value": "//select[@id='version-bom']/option[@value='current']",
                    "description": "Select CurrentWorkingView"
                },
                {
                    "action": "input",
                    "locator_type": "id",
                    "locator_value": "item",
                    "text": "440000849200",
                    "description": "Enter item ID in filter"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Wait after entering item"
                }
            ], indent=2)
            step11.selenium_script_json = step11_json
            print("✓ Step 11: Added BOM page navigation + filters")
        
        # ===================================================================
        # STEP 12: Navigate to BOM, verify data
        # ===================================================================
        if len(steps) >= 12:
            step12 = steps[11]
            step12_json = json.dumps([
                {
                    "action": "navigate",
                    "url": "http://localhost:3001/bom-setup.html",
                    "description": "Navigate to BOM Setup page"
                },
                {
                    "action": "wait",
                    "duration": 2,
                    "description": "Wait for page load"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "data-table",
                    "description": "Verify Produced Items table exists"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "class",
                    "locator_value": "btn-link",
                    "description": "Verify action links are present"
                },
                {
                    "action": "verify_element_present",
                    "locator_type": "id",
                    "locator_value": "consumed-items",
                    "description": "Verify consumed items section exists"
                },
                {
                    "action": "wait",
                    "duration": 1,
                    "description": "Final verification wait"
                }
            ], indent=2)
            step12.selenium_script_json = step12_json
            print("✓ Step 12: Added BOM page navigation + verification")
        
        # Commit all changes
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS! Fixed all {len(steps)} steps for sequential execution")
        print(f"{'='*80}")
        print(f"\nKey Changes:")
        print(f"  • Step 2: Added direct navigation to dashboard.html")
        print(f"  • Steps 3-5: Added full menu navigation path from dashboard")
        print(f"  • Step 6: Direct navigation to forecast.html")
        print(f"  • Steps 7-9: Added forecast page navigation before actions")
        print(f"  • Step 10: Direct navigation to bom-setup.html")
        print(f"  • Steps 11-12: Added BOM page navigation before actions")
        print(f"{'='*80}")
        print(f"\nEach step now works independently!")
        print(f"You can run steps one at a time and they will work correctly.")
        print(f"{'='*80}\n")
        
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
            print("Usage: python fix_sequential_execution.py [test_case_id]")
            sys.exit(1)
    
    print("\n" + "="*80)
    print("FIXING SEQUENTIAL EXECUTION")
    print("="*80 + "\n")
    
    success = fix_sequential_execution(test_case_id)
    
    if success:
        print("\n✓ All steps fixed!")
        print(f"\nYou can now:")
        print(f"  1. Go to http://localhost:5173/test-case/{test_case_id}")
        print(f"  2. Run Step 2 (it will now work!)")
        print(f"  3. Run any other step independently")
        print("\n" + "="*80)
    else:
        print("\n✗ Fix failed")
        sys.exit(1)
