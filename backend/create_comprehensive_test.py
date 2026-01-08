"""
Create a comprehensive 8-12 step test case for Mock O9 Platform
This test case covers the complete workflow from login to data export
All steps are guaranteed to work with the Mock O9 website
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
import json

def create_comprehensive_test():
    """Create a complete 12-step test case for O9 Platform"""
    
    init_db()
    db = SessionLocal()
    
    try:
        # Check if test already exists
        existing = db.query(TestCase).filter(
            TestCase.name == "Mock O9 - Complete Workflow Test"
        ).first()
        
        if existing:
            print(f"Test case already exists: ID {existing.id}")
            print("Delete it first if you want to recreate it")
            return existing.id
        
        # Create test case
        tc = TestCase(
            name="Mock O9 - Complete Workflow Test",
            description="Comprehensive end-to-end test of O9 Platform including login, navigation, forecast generation, filter application, BOM setup, and data validation. This test covers 12 steps across all major modules.",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 website running on http://localhost:3001",
            assigned_to="Test Automation Team"
        )
        db.add(tc)
        db.flush()
        
        print(f"\n{'='*80}")
        print(f"Creating comprehensive test case: {tc.name}")
        print(f"Test Case ID: {tc.id}")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # STEP 1: Login to O9 Platform
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
                "description": "Wait for page to fully load"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "username",
                "description": "Verify username field exists"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "password",
                "description": "Verify password field exists"
            },
            {
                "action": "input",
                "locator_type": "id",
                "locator_value": "username",
                "text": "testuser",
                "description": "Enter username: testuser"
            },
            {
                "action": "input",
                "locator_type": "id",
                "locator_value": "password",
                "text": "password123",
                "description": "Enter password: password123"
            },
            {
                "action": "click",
                "locator_type": "id",
                "locator_value": "login-button",
                "description": "Click the login button"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for login redirect"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Welcome to O9 Platform",
                "description": "Verify successful login and dashboard display"
            }
        ], indent=2)
        
        step1 = TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to O9 Platform\n\nNavigate to the O9 login page at http://localhost:3001 and authenticate using valid credentials (testuser / password123). Verify successful redirect to the main dashboard with the welcome message displayed.",
            expected_result="User successfully logs into the O9 platform. The dashboard page loads and displays 'Welcome to O9 Platform' heading. Navigation menu is visible on the left side.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\n# System executes JSON commands\nfrom selenium import webdriver\ndriver = webdriver.Chrome()\ndriver.get('http://localhost:3001')\nusername = driver.find_element(By.ID, 'username')\nusername.send_keys('testuser')\npassword = driver.find_element(By.ID, 'password')\npassword.send_keys('password123')\nlogin_btn = driver.find_element(By.ID, 'login-button')\nlogin_btn.click()",
            selenium_script_json=step1_json
        )
        db.add(step1)
        print("✓ Step 1: Login")
        
        # ===================================================================
        # STEP 2: Verify Dashboard Widgets
        # ===================================================================
        step2_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for dashboard to fully render"
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
        
        step2 = TestStep(
            test_case_id=tc.id,
            step_number=2,
            description="Verify Dashboard Components\n\nOn the dashboard page, verify that all essential UI components are present including the dashboard widgets container, individual widgets displaying metrics, and the navigation sidebar with menu options.",
            expected_result="Dashboard displays properly with all widgets visible (Demand Planning, Supply Planning, Inventory). Navigation sidebar is present with expandable menu structure. All UI elements are rendered correctly.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nfrom selenium.webdriver.common.by import By\nwidgets = driver.find_element(By.CLASS_NAME, 'dashboard-widgets')\nassert widgets.is_displayed()\nsidebar = driver.find_element(By.CLASS_NAME, 'sidebar')\nassert sidebar.is_displayed()",
            selenium_script_json=step2_json
        )
        db.add(step2)
        print("✓ Step 2: Verify Dashboard")
        
        # ===================================================================
        # STEP 3: Navigate to Demand Analyst Menu
        # ===================================================================
        step3_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait before navigation"
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
        
        step3 = TestStep(
            test_case_id=tc.id,
            step_number=3,
            description="Navigate to Demand Analyst Module\n\nFrom the dashboard, locate the Demand Analyst menu item in the left navigation sidebar and click it to expand the submenu. Verify that the submenu appears with options for System Forecast and other demand planning functions.",
            expected_result="Demand Analyst submenu expands successfully, displaying nested menu options including 'System Forecast' and other demand planning modules. Submenu remains open and visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\ndemand = driver.find_element(By.XPATH, \"//a[contains(text(), 'Demand Analyst')]\")\ndemand.click()\ntime.sleep(1)\nsubmenu = driver.find_element(By.ID, 'demand-analyst')\nassert 'active' in submenu.get_attribute('class')",
            selenium_script_json=step3_json
        )
        db.add(step3)
        print("✓ Step 3: Expand Demand Analyst")
        
        # ===================================================================
        # STEP 4: Navigate to System Forecast
        # ===================================================================
        step4_json = json.dumps([
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
        
        step4 = TestStep(
            test_case_id=tc.id,
            step_number=4,
            description="Expand System Forecast Submenu\n\nWithin the Demand Analyst menu, click on the 'System Forecast' option to expand its nested submenu. This should reveal additional options including 'Generate Forecast'.",
            expected_result="System Forecast submenu expands, showing nested options. 'Generate Forecast' option becomes visible and clickable within the expanded submenu structure.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nsystem_forecast = driver.find_element(By.XPATH, \"//a[contains(text(), 'System Forecast')]\")\nsystem_forecast.click()\ntime.sleep(1)",
            selenium_script_json=step4_json
        )
        db.add(step4)
        print("✓ Step 4: Expand System Forecast")
        
        # ===================================================================
        # STEP 5: Navigate to Generate Forecast
        # ===================================================================
        step5_json = json.dumps([
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
        
        step5 = TestStep(
            test_case_id=tc.id,
            step_number=5,
            description="Expand Generate Forecast Options\n\nClick on 'Generate Forecast' within the System Forecast submenu to reveal the final level of navigation options, including the 'Details' page link.",
            expected_result="Generate Forecast submenu expands successfully. 'Details' link becomes visible as a navigation option. Menu structure maintains proper hierarchy with all parent menus still expanded.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\ngenerate = driver.find_element(By.XPATH, \"//a[contains(text(), 'Generate Forecast')]\")\ngenerate.click()\ntime.sleep(1)",
            selenium_script_json=step5_json
        )
        db.add(step5)
        print("✓ Step 5: Expand Generate Forecast")
        
        # ===================================================================
        # STEP 6: Navigate to Forecast Details Page
        # ===================================================================
        step6_json = json.dumps([
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Details')]",
                "description": "Click Details link to navigate to forecast page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page navigation and load"
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
        
        step6 = TestStep(
            test_case_id=tc.id,
            step_number=6,
            description="Navigate to Forecast Details Page\n\nClick the 'Details' link under Generate Forecast to navigate to the main forecast analysis page. Verify that the page loads successfully with the heading 'Generate Forecast - Details' and that the scope filters section is present.",
            expected_result="Forecast Details page loads successfully. Page heading displays 'Generate Forecast - Details'. Scope filters section is visible with dropdowns for Forecast Iteration, Channel, Region, and Version. Review and Gap widgets are present on the page.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\ndetails = driver.find_element(By.XPATH, \"//a[contains(text(), 'Details')]\")\ndetails.click()\ntime.sleep(2)\nassert 'forecast.html' in driver.current_url",
            selenium_script_json=step6_json
        )
        db.add(step6)
        print("✓ Step 6: Navigate to Forecast Details")
        
        # ===================================================================
        # STEP 7: Apply Forecast Iteration Filter
        # ===================================================================
        step7_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for page elements to stabilize"
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
        
        step7 = TestStep(
            test_case_id=tc.id,
            step_number=7,
            description="Apply Forecast Iteration Filter\n\nOn the Forecast Details page, locate the 'Forecast Iteration' dropdown in the scope filters section. Click the dropdown and select 'Short Term' from the available options.",
            expected_result="Forecast Iteration dropdown opens successfully and displays all available options (Short Term, Mid Term, Long Term). 'Short Term' is selected successfully. The dropdown value updates to reflect the selection.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\niteration = driver.find_element(By.ID, 'forecast-iteration')\niteration.click()\nshort_term = driver.find_element(By.XPATH, \"//select[@id='forecast-iteration']/option[@value='short-term']\")\nshort_term.click()",
            selenium_script_json=step7_json
        )
        db.add(step7)
        print("✓ Step 7: Select Forecast Iteration")
        
        # ===================================================================
        # STEP 8: Apply Region Filter
        # ===================================================================
        step8_json = json.dumps([
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
        
        step8 = TestStep(
            test_case_id=tc.id,
            step_number=8,
            description="Apply Region Filter\n\nContinuing with filter selection, locate the 'Region' dropdown in the scope filters section. Click it and select 'North America' from the available regional options.",
            expected_result="Region dropdown opens and displays all available regions (North America, Europe, Asia). 'North America' is selected successfully. The filter value updates to show the selected region.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nregion = driver.find_element(By.ID, 'region')\nregion.click()\nna = driver.find_element(By.XPATH, \"//select[@id='region']/option[@value='na']\")\nna.click()",
            selenium_script_json=step8_json
        )
        db.add(step8)
        print("✓ Step 8: Select Region")
        
        # ===================================================================
        # STEP 9: Verify Widgets Display
        # ===================================================================
        step9_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for widgets to render"
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
        
        step9 = TestStep(
            test_case_id=tc.id,
            step_number=9,
            description="Verify Forecast Widgets Display\n\nAfter applying filters, verify that both the Review Widget and Gap Widget are properly displayed on the page. Check that the Gap Widget contains a data table with forecast information.",
            expected_result="Both widgets are visible and properly rendered. Review Widget displays with a chart placeholder. Gap Widget shows a data table with columns for Item, Forecast, Last Cycle, and Gap %. Sample data is visible in the table.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nreview = driver.find_element(By.CLASS_NAME, 'review-widget')\nassert review.is_displayed()\ngap = driver.find_element(By.CLASS_NAME, 'gap-widget')\nassert gap.is_displayed()",
            selenium_script_json=step9_json
        )
        db.add(step9)
        print("✓ Step 9: Verify Widgets")
        
        # ===================================================================
        # STEP 10: Navigate to BOM Setup (Supply Planning)
        # ===================================================================
        step10_json = json.dumps([
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), '← Back to Dashboard')]",
                "description": "Click back to dashboard link"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for dashboard to load"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Supply Master Planning')]",
                "description": "Expand Supply Master Planning menu"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manage Network')]",
                "description": "Expand Manage Network submenu"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manufacturing Network')]",
                "description": "Expand Manufacturing Network submenu"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'BOM Setup')]",
                "description": "Click BOM Setup link"
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
            }
        ], indent=2)
        
        step10 = TestStep(
            test_case_id=tc.id,
            step_number=10,
            description="Navigate to BOM Setup Page\n\nReturn to the dashboard and navigate through Supply Master Planning > Manage Network > Manufacturing Network > BOM Setup. Verify that the BOM Setup page loads successfully with global filters and the Produced Items table.",
            expected_result="BOM Setup page loads successfully with heading 'BOM Setup'. Global filters section displays with Version and Item input fields. Produced Items table is visible showing sample BOM data. Actions column contains links to view consumed items.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nback = driver.find_element(By.XPATH, \"//a[contains(text(), 'Back to Dashboard')]\")\nback.click()\ntime.sleep(2)\nsupply = driver.find_element(By.XPATH, \"//a[contains(text(), 'Supply Master Planning')]\")\nsupply.click()",
            selenium_script_json=step10_json
        )
        db.add(step10)
        print("✓ Step 10: Navigate to BOM Setup")
        
        # ===================================================================
        # STEP 11: Apply BOM Filters
        # ===================================================================
        step11_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for page stabilization"
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
        
        step11 = TestStep(
            test_case_id=tc.id,
            step_number=11,
            description="Apply BOM Global Filters\n\nOn the BOM Setup page, apply global filters by selecting 'CurrentWorkingView' from the Version dropdown and entering item ID '440000849200' in the Item input field. This filters the BOM data to show only relevant items.",
            expected_result="Version filter successfully set to 'CurrentWorkingView'. Item ID '440000849200' is entered in the Item field. The filters are ready to be applied to retrieve BOM configuration data.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\nversion = driver.find_element(By.ID, 'version-bom')\nversion.click()\ncurrent = driver.find_element(By.XPATH, \"//select[@id='version-bom']/option[@value='current']\")\ncurrent.click()\nitem = driver.find_element(By.ID, 'item')\nitem.send_keys('440000849200')",
            selenium_script_json=step11_json
        )
        db.add(step11)
        print("✓ Step 11: Apply BOM Filters")
        
        # ===================================================================
        # STEP 12: Verify BOM Data and Complete Test
        # ===================================================================
        step12_json = json.dumps([
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
        
        step12 = TestStep(
            test_case_id=tc.id,
            step_number=12,
            description="Verify BOM Data Display and Complete Test\n\nVerify that the Produced Items table displays correctly with item IDs, descriptions, locations, and action links. Confirm that the consumed items section is present and ready to display linked material data when action links are clicked. This completes the comprehensive workflow test.",
            expected_result="Produced Items table displays with sample BOM data including items 440000849200 and 440000870300. Each row has a 'View Consumed' link in the Actions column. Consumed Items section is present below the table. All UI elements are properly rendered. Test completes successfully covering the full O9 workflow from login through forecast analysis to BOM setup.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Python script for display only\ntable = driver.find_element(By.CLASS_NAME, 'data-table')\nassert table.is_displayed()\nlinks = driver.find_elements(By.CLASS_NAME, 'btn-link')\nassert len(links) > 0\ndriver.quit()",
            selenium_script_json=step12_json
        )
        db.add(step12)
        print("✓ Step 12: Verify BOM Data")
        
        # Commit everything
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS! Created comprehensive test case with 12 steps")
        print(f"{'='*80}")
        print(f"Test Case ID: {tc.id}")
        print(f"Test Case Name: {tc.name}")
        print(f"Total Steps: 12")
        print(f"{'='*80}")
        print(f"\nTest Coverage:")
        print(f"  ✓ Step 1-2:   Authentication and Dashboard Verification")
        print(f"  ✓ Step 3-6:   Multi-level Menu Navigation (Demand Analyst)")
        print(f"  ✓ Step 7-9:   Filter Application and Widget Verification")
        print(f"  ✓ Step 10-12: Supply Planning Module and BOM Setup")
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
    print("CREATING COMPREHENSIVE O9 TEST CASE")
    print("="*80 + "\n")
    
    test_id = create_comprehensive_test()
    
    if test_id:
        print("\n✓ Test case created successfully!")
        print(f"\nNext steps:")
        print(f"  1. Ensure Mock O9 is running: cd mock-o9-website && python -m http.server 3001")
        print(f"  2. Ensure backend is running: cd backend && python run.py")
        print(f"  3. Ensure frontend is running: cd frontend && npm run dev")
        print(f"  4. Open: http://localhost:5173/test-case/{test_id}")
        print(f"  5. Click 'Run Step' on each step and watch it work!")
        print(f"\n" + "="*80)
    else:
        print("\n✗ Failed to create test case")
        sys.exit(1)
