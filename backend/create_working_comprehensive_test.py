"""
Create a comprehensive 12-step test case where EVERY step is fully independent
Each step includes complete navigation context and doesn't depend on previous steps
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
import json

def create_independent_test():
    """Create a complete test where every step is independent"""
    
    init_db()
    db = SessionLocal()
    
    try:
        # Create test case
        tc = TestCase(
            name="Mock O9 - Independent Steps Test",
            description="Comprehensive test where each step is fully independent and includes complete navigation context. Every step can be run individually without dependencies.",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 running on http://localhost:3001",
            assigned_to="Test Automation Team"
        )
        db.add(tc)
        db.flush()
        
        print(f"\n{'='*80}")
        print(f"Creating Independent Test Case: {tc.name}")
        print(f"Test Case ID: {tc.id}")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # STEP 1: Login (Independent)
        # ===================================================================
        step1_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001",
                "description": "Navigate to Mock O9 login page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page to load"
            },
            {
                "action": "input",
                "locator_type": "id",
                "locator_value": "username",
                "text": "testuser",
                "description": "Enter username"
            },
            {
                "action": "input",
                "locator_type": "id",
                "locator_value": "password",
                "text": "password123",
                "description": "Enter password"
            },
            {
                "action": "click",
                "locator_type": "id",
                "locator_value": "login-button",
                "description": "Click login button"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for redirect"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Welcome to O9 Platform",
                "description": "Verify successful login"
            }
        ], indent=2)
        
        step1 = TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to O9 Platform\n\nNavigate to http://localhost:3001 and login with testuser/password123. Verify successful authentication and redirect to dashboard.",
            expected_result="User successfully authenticates and reaches the dashboard with 'Welcome to O9 Platform' heading visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only - JSON commands execute\nfrom selenium import webdriver\ndriver = webdriver.Chrome()\ndriver.get('http://localhost:3001')",
            selenium_script_json=step1_json
        )
        db.add(step1)
        print("✓ Step 1: Login (Independent)")
        
        # ===================================================================
        # STEP 2: Verify Dashboard (Independent - navigates directly)
        # ===================================================================
        step2_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/dashboard.html",
                "description": "Navigate directly to dashboard"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page to load"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Welcome to O9 Platform",
                "description": "Verify dashboard heading"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "dashboard-widgets",
                "description": "Verify widgets container"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "sidebar",
                "description": "Verify navigation sidebar"
            }
        ], indent=2)
        
        step2 = TestStep(
            test_case_id=tc.id,
            step_number=2,
            description="Verify Dashboard Components\n\nNavigate directly to dashboard and verify all essential UI components are present: heading, widgets container, individual widgets, and navigation sidebar.",
            expected_result="Dashboard displays with 'Welcome to O9 Platform' heading, dashboard-widgets container, and navigation sidebar all visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/dashboard.html')\nheading = driver.find_element(By.TAG_NAME, 'h1')",
            selenium_script_json=step2_json
        )
        db.add(step2)
        print("✓ Step 2: Verify Dashboard (Independent)")
        
        # ===================================================================
        # STEP 3: Expand Demand Analyst Menu (Independent)
        # ===================================================================
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
                "description": "Click Demand Analyst menu"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu expansion"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "demand-analyst",
                "description": "Verify submenu visible"
            }
        ], indent=2)
        
        step3 = TestStep(
            test_case_id=tc.id,
            step_number=3,
            description="Expand Demand Analyst Menu\n\nNavigate to dashboard and expand the Demand Analyst menu item to reveal its submenu options.",
            expected_result="Demand Analyst submenu expands successfully, showing nested menu options including System Forecast.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/dashboard.html')\ndemand = driver.find_element(By.XPATH, '//a[contains(text(), \"Demand Analyst\")]')",
            selenium_script_json=step3_json
        )
        db.add(step3)
        print("✓ Step 3: Expand Demand Analyst (Independent)")
        
        # ===================================================================
        # STEP 4: Navigate to System Forecast (Independent)
        # ===================================================================
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
                "description": "Click System Forecast"
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
                "description": "Verify System Forecast submenu"
            }
        ], indent=2)
        
        step4 = TestStep(
            test_case_id=tc.id,
            step_number=4,
            description="Navigate to System Forecast Submenu\n\nNavigate to dashboard, expand Demand Analyst menu, then expand System Forecast submenu.",
            expected_result="System Forecast submenu expands, revealing nested options including Generate Forecast.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/dashboard.html')\ntime.sleep(2)",
            selenium_script_json=step4_json
        )
        db.add(step4)
        print("✓ Step 4: System Forecast (Independent)")
        
        # ===================================================================
        # STEP 5: Navigate to Generate Forecast (Independent)
        # ===================================================================
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
                "description": "Click Generate Forecast"
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
                "description": "Verify Generate Forecast submenu"
            }
        ], indent=2)
        
        step5 = TestStep(
            test_case_id=tc.id,
            step_number=5,
            description="Navigate to Generate Forecast Submenu\n\nNavigate through complete menu path: Dashboard → Demand Analyst → System Forecast → Generate Forecast.",
            expected_result="Generate Forecast submenu expands, showing 'Details' link as final navigation option.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/dashboard.html')",
            selenium_script_json=step5_json
        )
        db.add(step5)
        print("✓ Step 5: Generate Forecast (Independent)")
        
        # ===================================================================
        # STEP 6: Navigate to Forecast Details Page (Independent)
        # ===================================================================
        step6_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/forecast.html",
                "description": "Navigate directly to forecast page"
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
                "description": "Verify page heading"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "scope-filters",
                "description": "Verify scope filters section"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "forecast-iteration",
                "description": "Verify forecast iteration dropdown"
            }
        ], indent=2)
        
        step6 = TestStep(
            test_case_id=tc.id,
            step_number=6,
            description="Navigate to Forecast Details Page\n\nDirect navigation to forecast.html. Verify page loads with heading, scope filters, and filter dropdowns.",
            expected_result="Forecast page loads with 'Generate Forecast - Details' heading, scope filters section, and all filter dropdowns visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/forecast.html')",
            selenium_script_json=step6_json
        )
        db.add(step6)
        print("✓ Step 6: Forecast Details (Independent)")
        
        # ===================================================================
        # STEP 7: Apply Forecast Iteration Filter (Independent)
        # ===================================================================
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
                "action": "wait",
                "duration": 0.5,
                "description": "Wait for dropdown"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//select[@id='forecast-iteration']/option[@value='short-term']",
                "description": "Select Short Term"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after selection"
            }
        ], indent=2)
        
        step7 = TestStep(
            test_case_id=tc.id,
            step_number=7,
            description="Apply Forecast Iteration Filter\n\nNavigate to forecast page and select 'Short Term' from the Forecast Iteration dropdown filter.",
            expected_result="Forecast Iteration dropdown opens and 'Short Term' is selected successfully.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/forecast.html')",
            selenium_script_json=step7_json
        )
        db.add(step7)
        print("✓ Step 7: Iteration Filter (Independent)")
        
        # ===================================================================
        # STEP 8: Apply Region Filter (Independent)
        # ===================================================================
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
                "action": "wait",
                "duration": 0.5,
                "description": "Wait for dropdown"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//select[@id='region']/option[@value='na']",
                "description": "Select North America"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after selection"
            }
        ], indent=2)
        
        step8 = TestStep(
            test_case_id=tc.id,
            step_number=8,
            description="Apply Region Filter\n\nNavigate to forecast page and select 'North America' from the Region dropdown filter.",
            expected_result="Region dropdown opens and 'North America' is selected successfully.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/forecast.html')",
            selenium_script_json=step8_json
        )
        db.add(step8)
        print("✓ Step 8: Region Filter (Independent)")
        
        # ===================================================================
        # STEP 9: Verify Forecast Widgets (Independent)
        # ===================================================================
        step9_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/forecast.html",
                "description": "Navigate to forecast page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page and widgets"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "review-widget",
                "description": "Verify Review Widget"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "gap-widget",
                "description": "Verify Gap Widget"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "data-table",
                "description": "Verify data table in Gap Widget"
            }
        ], indent=2)
        
        step9 = TestStep(
            test_case_id=tc.id,
            step_number=9,
            description="Verify Forecast Widgets Display\n\nNavigate to forecast page and verify both Review Widget and Gap Widget are properly displayed with data table.",
            expected_result="Both widgets visible: Review Widget with chart placeholder, Gap Widget with data table showing forecast information.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/forecast.html')",
            selenium_script_json=step9_json
        )
        db.add(step9)
        print("✓ Step 9: Verify Widgets (Independent)")
        
        # ===================================================================
        # STEP 10: Navigate to BOM Setup (Independent)
        # ===================================================================
        step10_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/bom-setup.html",
                "description": "Navigate directly to BOM Setup"
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
                "description": "Verify BOM Setup heading"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "scope-filters",
                "description": "Verify global filters section"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "version-bom",
                "description": "Verify version dropdown"
            }
        ], indent=2)
        
        step10 = TestStep(
            test_case_id=tc.id,
            step_number=10,
            description="Navigate to BOM Setup Page\n\nDirect navigation to bom-setup.html. Verify page loads with heading, global filters, and Produced Items table.",
            expected_result="BOM Setup page loads with 'BOM Setup' heading, global filters section with Version and Item fields, and Produced Items table visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/bom-setup.html')",
            selenium_script_json=step10_json
        )
        db.add(step10)
        print("✓ Step 10: BOM Setup (Independent)")
        
        # ===================================================================
        # STEP 11: Apply BOM Filters (Independent)
        # ===================================================================
        step11_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/bom-setup.html",
                "description": "Navigate to BOM Setup"
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
                "action": "wait",
                "duration": 0.5,
                "description": "Wait for dropdown"
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
                "description": "Enter item ID"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after input"
            }
        ], indent=2)
        
        step11 = TestStep(
            test_case_id=tc.id,
            step_number=11,
            description="Apply BOM Global Filters\n\nNavigate to BOM Setup page and apply filters: select 'CurrentWorkingView' from Version dropdown and enter item ID '440000849200'.",
            expected_result="Version filter set to 'CurrentWorkingView' and item ID '440000849200' entered successfully in Item field.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/bom-setup.html')",
            selenium_script_json=step11_json
        )
        db.add(step11)
        print("✓ Step 11: BOM Filters (Independent)")
        
        # ===================================================================
        # STEP 12: Verify BOM Data (Independent)
        # ===================================================================
        step12_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001/bom-setup.html",
                "description": "Navigate to BOM Setup"
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
                "description": "Verify Produced Items table"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "btn-link",
                "description": "Verify action links present"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "consumed-items",
                "description": "Verify consumed items section"
            }
        ], indent=2)
        
        step12 = TestStep(
            test_case_id=tc.id,
            step_number=12,
            description="Verify BOM Data Display\n\nNavigate to BOM Setup and verify Produced Items table displays correctly with action links and consumed items section.",
            expected_result="Produced Items table displays with sample BOM data. 'View Consumed' links visible in Actions column. Consumed Items section present below table.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndriver.get('http://localhost:3001/bom-setup.html')",
            selenium_script_json=step12_json
        )
        db.add(step12)
        print("✓ Step 12: Verify BOM Data (Independent)")
        
        # Commit all
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS! Created new test case with 12 independent steps")
        print(f"{'='*80}")
        print(f"Test Case ID: {tc.id}")
        print(f"Test Case Name: {tc.name}")
        print(f"{'='*80}")
        print(f"\nKey Features:")
        print(f"  ✓ Every step navigates to the page it needs")
        print(f"  ✓ No dependencies between steps")
        print(f"  ✓ Each step can run independently")
        print(f"  ✓ Direct navigation to pages (steps 6, 10)")
        print(f"  ✓ Full menu paths when needed (steps 3-5)")
        print(f"{'='*80}")
        print(f"\nAccess the test at:")
        print(f"  http://localhost:5173/test-case/{tc.id}")
        print(f"{'='*80}\n")
        
        return tc.id
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("CREATING NEW INDEPENDENT TEST CASE")
    print("="*80 + "\n")
    
    test_id = create_independent_test()
    
    if test_id:
        print("\n✓ Test case created successfully!")
        print(f"\nNext steps:")
        print(f"  1. Ensure Mock O9 is running: cd mock-o9-website && python -m http.server 3001")
        print(f"  2. Ensure backend is running: cd backend && python run.py")
        print(f"  3. Ensure frontend is running: cd frontend && npm run dev")
        print(f"  4. Open: http://localhost:5173/test-case/{test_id}")
        print(f"  5. Run ANY step - they all work independently!")
        print(f"\n" + "="*80)
    else:
        print("\n✗ Failed to create test case")
        sys.exit(1)
