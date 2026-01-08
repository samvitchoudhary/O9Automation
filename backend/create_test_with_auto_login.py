"""
Create comprehensive test case with auto-login feature
Backend automatically prepends Step 1 (login) to every step
So steps 2-12 only contain their specific actions
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
import json

def create_test_with_auto_login():
    """Create test where backend auto-prepends login to each step"""
    
    init_db()
    db = SessionLocal()
    
    try:
        tc = TestCase(
            name="Mock O9 - Auto-Login Test",
            description="Comprehensive test with automatic login. Backend prepends Step 1 (login) to every step automatically, so each step only contains its specific actions.",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 running on http://localhost:3001. Backend auto-executes login before each step.",
            assigned_to="Test Automation Team"
        )
        db.add(tc)
        db.flush()
        
        print(f"\n{'='*80}")
        print(f"Creating Test Case with Auto-Login Feature")
        print(f"Test Case ID: {tc.id}")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # STEP 1: Login (This will be auto-prepended to all other steps)
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
                "description": "Wait for authentication and redirect"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Welcome to O9 Platform",
                "description": "Verify successful login - dashboard loaded"
            }
        ], indent=2)
        
        step1 = TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to O9 Platform\n\nNavigate to http://localhost:3001 and authenticate with testuser/password123. This step will be automatically executed before every other step.",
            expected_result="User authenticates successfully and reaches dashboard with 'Welcome to O9 Platform' heading visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Auto-prepended to all steps\nfrom selenium import webdriver\ndriver = webdriver.Chrome()\ndriver.get('http://localhost:3001')",
            selenium_script_json=step1_json
        )
        db.add(step1)
        print("✓ Step 1: Login (Auto-prepended to all steps)")
        
        # ===================================================================
        # STEP 2: Verify Dashboard (No login needed - auto-prepended)
        # ===================================================================
        step2_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
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
                "locator_value": "widget",
                "description": "Verify at least one widget"
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
            description="Verify Dashboard Components\n\nAfter login (auto-executed), verify all essential dashboard UI components are present.",
            expected_result="Dashboard displays with widgets container, individual widgets, and navigation sidebar all visible.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only - login auto-executed\nwidgets = driver.find_element(By.CLASS_NAME, 'dashboard-widgets')",
            selenium_script_json=step2_json
        )
        db.add(step2)
        print("✓ Step 2: Verify Dashboard")
        
        # ===================================================================
        # STEP 3: Expand Demand Analyst Menu
        # ===================================================================
        step3_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
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
                "description": "Wait for submenu"
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
            description="Expand Demand Analyst Menu\n\nAfter login, expand the Demand Analyst menu to reveal submenu options.",
            expected_result="Demand Analyst submenu expands, showing System Forecast and other options.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only\ndemand = driver.find_element(By.XPATH, '//a[contains(text(), \"Demand Analyst\")]')",
            selenium_script_json=step3_json
        )
        db.add(step3)
        print("✓ Step 3: Expand Demand Analyst")
        
        # ===================================================================
        # STEP 4: Navigate to System Forecast
        # ===================================================================
        step4_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
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
                "description": "Click System Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
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
            description="Navigate to System Forecast Submenu\n\nAfter login, navigate: Demand Analyst → System Forecast.",
            expected_result="System Forecast submenu expands with Generate Forecast option.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step4_json
        )
        db.add(step4)
        print("✓ Step 4: System Forecast")
        
        # ===================================================================
        # STEP 5: Navigate to Generate Forecast
        # ===================================================================
        step5_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
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
                "description": "Wait"
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
            description="Navigate to Generate Forecast\n\nAfter login, navigate: Demand Analyst → System Forecast → Generate Forecast.",
            expected_result="Generate Forecast submenu expands showing Details link.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step5_json
        )
        db.add(step5)
        print("✓ Step 5: Generate Forecast")
        
        # ===================================================================
        # STEP 6: Navigate to Forecast Details
        # ===================================================================
        step6_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
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
                "description": "Expand Generate Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast.html']",
                "description": "Click Details link"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for forecast page load"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Generate Forecast",
                "description": "Verify forecast page heading"
            }
        ], indent=2)
        
        step6 = TestStep(
            test_case_id=tc.id,
            step_number=6,
            description="Navigate to Forecast Details Page\n\nAfter login, navigate through menu to forecast.html page.",
            expected_result="Forecast page loads with 'Generate Forecast' heading and scope filters.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step6_json
        )
        db.add(step6)
        print("✓ Step 6: Forecast Details")
        
        # ===================================================================
        # STEP 7: Apply Forecast Iteration Filter
        # ===================================================================
        step7_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                "description": "Navigate to forecast page"
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
                "description": "Expand Generate Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast.html']",
                "description": "Go to forecast page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page"
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
            description="Apply Forecast Iteration Filter\n\nAfter login, navigate to forecast page and select 'Short Term' iteration.",
            expected_result="Forecast Iteration dropdown opens and 'Short Term' is selected.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step7_json
        )
        db.add(step7)
        print("✓ Step 7: Iteration Filter")
        
        # ===================================================================
        # STEP 8: Apply Region Filter
        # ===================================================================
        step8_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                "description": "Navigate to forecast"
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
                "description": "Expand Generate Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast.html']",
                "description": "Go to forecast page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
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
                "description": "Select North America"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            }
        ], indent=2)
        
        step8 = TestStep(
            test_case_id=tc.id,
            step_number=8,
            description="Apply Region Filter\n\nAfter login, navigate to forecast page and select 'North America' region.",
            expected_result="Region dropdown opens and 'North America' is selected.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step8_json
        )
        db.add(step8)
        print("✓ Step 8: Region Filter")
        
        # ===================================================================
        # STEP 9: Verify Forecast Widgets
        # ===================================================================
        step9_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Demand Analyst')]",
                "description": "Navigate to forecast"
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
                "description": "Expand Generate Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast.html']",
                "description": "Go to forecast page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for widgets"
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
                "description": "Verify data table"
            }
        ], indent=2)
        
        step9 = TestStep(
            test_case_id=tc.id,
            step_number=9,
            description="Verify Forecast Widgets\n\nAfter login, navigate to forecast page and verify widgets display.",
            expected_result="Review Widget and Gap Widget visible with data table.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step9_json
        )
        db.add(step9)
        print("✓ Step 9: Verify Widgets")
        
        # ===================================================================
        # STEP 10: Navigate to BOM Setup
        # ===================================================================
        step10_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Supply Master Planning')]",
                "description": "Expand Supply Planning"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manage Network')]",
                "description": "Expand Manage Network"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manufacturing Network')]",
                "description": "Expand Manufacturing Network"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='bom-setup.html']",
                "description": "Click BOM Setup"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for BOM page"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "BOM Setup",
                "description": "Verify BOM Setup heading"
            }
        ], indent=2)
        
        step10 = TestStep(
            test_case_id=tc.id,
            step_number=10,
            description="Navigate to BOM Setup\n\nAfter login, navigate: Supply Master Planning → Manage Network → Manufacturing Network → BOM Setup.",
            expected_result="BOM Setup page loads with heading and filters.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step10_json
        )
        db.add(step10)
        print("✓ Step 10: BOM Setup")
        
        # ===================================================================
        # STEP 11: Apply BOM Filters
        # ===================================================================
        step11_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Supply Master Planning')]",
                "description": "Navigate to BOM"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manage Network')]",
                "description": "Expand Manage Network"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manufacturing Network')]",
                "description": "Expand Manufacturing"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='bom-setup.html']",
                "description": "Go to BOM page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
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
                "description": "Enter item ID"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            }
        ], indent=2)
        
        step11 = TestStep(
            test_case_id=tc.id,
            step_number=11,
            description="Apply BOM Filters\n\nAfter login, navigate to BOM Setup and apply Version and Item filters.",
            expected_result="Version set to CurrentWorkingView and item ID entered.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step11_json
        )
        db.add(step11)
        print("✓ Step 11: BOM Filters")
        
        # ===================================================================
        # STEP 12: Verify BOM Data
        # ===================================================================
        step12_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Supply Master Planning')]",
                "description": "Navigate to BOM"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manage Network')]",
                "description": "Expand"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(text(), 'Manufacturing Network')]",
                "description": "Expand"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='bom-setup.html']",
                "description": "Go to BOM"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
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
                "description": "Verify action links"
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
            description="Verify BOM Data\n\nAfter login, navigate to BOM Setup and verify data table displays correctly.",
            expected_result="Produced Items table visible with action links and consumed items section.",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Display only",
            selenium_script_json=step12_json
        )
        db.add(step12)
        print("✓ Step 12: Verify BOM Data")
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS! Created test case with auto-login feature")
        print(f"{'='*80}")
        print(f"Test Case ID: {tc.id}")
        print(f"{'='*80}")
        print(f"\nAuto-Login Feature:")
        print(f"  ✓ Backend automatically prepends Step 1 (login) to all steps")
        print(f"  ✓ Steps 2-12 only contain their specific actions")
        print(f"  ✓ Every step gets fresh authentication automatically")
        print(f"  ✓ No need to manually add login to each step")
        print(f"{'='*80}")
        print(f"\nAccess: http://localhost:5173/test-case/{tc.id}")
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
    print("CREATING TEST CASE WITH AUTO-LOGIN FEATURE")
    print("="*80 + "\n")
    
    test_id = create_test_with_auto_login()
    
    if test_id:
        print("\n✓ Test case created!")
        print(f"\nNext steps:")
        print(f"  1. Restart backend: cd backend && python run.py")
        print(f"  2. Open: http://localhost:5173/test-case/{test_id}")
        print(f"  3. Run ANY step - login is automatic!")
        print(f"\n" + "="*80)
    else:
        sys.exit(1)
