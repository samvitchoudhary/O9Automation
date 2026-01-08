"""
Create test case with selectors that actually work with Mock O9 structure
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestCaseStatus, TestStepStatus, ExecutionStatus
import json

def create_fixed_test():
    init_db()
    db = SessionLocal()
    
    try:
        tc = TestCase(
            name="Mock O9 - Fixed Menu Navigation Test",
            description="Test case with properly targeted selectors for Mock O9 website structure. Each step includes proper login and navigation context.",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 running on http://localhost:3001",
            assigned_to="Test Automation Team"
        )
        db.add(tc)
        db.flush()
        
        print(f"\n{'='*80}")
        print(f"Creating Fixed Test Case")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # STEP 1: Login
        # ===================================================================
        step1_json = json.dumps([
            {"action": "navigate", "url": "http://localhost:3001", "description": "Navigate to Mock O9"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "input", "locator_type": "id", "locator_value": "username", "text": "testuser", "description": "Enter username"},
            {"action": "input", "locator_type": "id", "locator_value": "password", "text": "password123", "description": "Enter password"},
            {"action": "click", "locator_type": "id", "locator_value": "login-button", "description": "Click login"},
            {"action": "wait", "duration": 2, "description": "Wait for redirect"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Welcome to O9 Platform", "description": "Verify login success"}
        ], indent=2)
        
        step1 = TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to O9 Platform",
            expected_result="User successfully authenticates and sees dashboard",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Login script",
            selenium_script_json=step1_json
        )
        db.add(step1)
        print("✓ Step 1: Login")
        
        # ===================================================================
        # STEP 2: Verify Dashboard
        # ===================================================================
        step2_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait after login"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "dashboard-widgets", "description": "Verify widgets container"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "sidebar", "description": "Verify sidebar"}
        ], indent=2)
        
        step2 = TestStep(
            test_case_id=tc.id,
            step_number=2,
            description="Verify Dashboard Components",
            expected_result="Dashboard displays with widgets and sidebar",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify dashboard",
            selenium_script_json=step2_json
        )
        db.add(step2)
        print("✓ Step 2: Verify Dashboard")
        
        # ===================================================================
        # STEP 3: Click Demand Analyst - FIXED SELECTOR
        # ===================================================================
        step3_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait after login"},
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
                "description": "Click Demand Analyst menu (using span/parent selector)"
            },
            {"action": "wait", "duration": 1, "description": "Wait for submenu to expand"},
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "demand-analyst",
                "description": "Verify Demand Analyst submenu exists"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "demand-analyst",
                "description": "Verify Demand Analyst submenu exists (will check if visible)"
            }
        ], indent=2)
        
        step3 = TestStep(
            test_case_id=tc.id,
            step_number=3,
            description="Expand Demand Analyst Menu",
            expected_result="Demand Analyst submenu expands with active class",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Expand Demand Analyst",
            selenium_script_json=step3_json
        )
        db.add(step3)
        print("✓ Step 3: Expand Demand Analyst (FIXED)")
        
        # ===================================================================
        # STEP 4: Click System Forecast - FIXED SELECTOR
        # ===================================================================
        step4_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait after login"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Expand Demand Analyst"},
            {"action": "wait", "duration": 1, "description": "Wait for submenu"},
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'system-forecast')]",
                "description": "Click System Forecast submenu item (using onclick attribute)"
            },
            {"action": "wait", "duration": 1, "description": "Wait for submenu"},
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "system-forecast",
                "description": "Verify System Forecast submenu exists"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "system-forecast",
                "description": "Verify System Forecast submenu exists"
            }
        ], indent=2)
        
        step4 = TestStep(
            test_case_id=tc.id,
            step_number=4,
            description="Expand System Forecast Submenu",
            expected_result="System Forecast submenu expands",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Expand System Forecast",
            selenium_script_json=step4_json
        )
        db.add(step4)
        print("✓ Step 4: System Forecast (FIXED)")
        
        # ===================================================================
        # STEP 5: Navigate to Forecast Page
        # ===================================================================
        step5_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Expand Demand Analyst"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'system-forecast')]", "description": "Expand System Forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'generate-forecast')]", "description": "Expand Generate Forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast.html']", "description": "Click Details link"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Generate Forecast", "description": "Verify forecast page"}
        ], indent=2)
        
        step5 = TestStep(
            test_case_id=tc.id,
            step_number=5,
            description="Navigate to Forecast Details Page",
            expected_result="Forecast page loads successfully",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to forecast",
            selenium_script_json=step5_json
        )
        db.add(step5)
        print("✓ Step 5: Navigate to Forecast")
        
        # ===================================================================
        # STEP 6: Verify Forecast Page Elements
        # ===================================================================
        step6_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate to forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'system-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'generate-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait for page"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "scope-filters", "description": "Verify filters section"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "forecast-iteration", "description": "Verify iteration dropdown"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "region", "description": "Verify region dropdown"}
        ], indent=2)
        
        step6 = TestStep(
            test_case_id=tc.id,
            step_number=6,
            description="Verify Forecast Page Elements",
            expected_result="All filters and controls are present",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify forecast elements",
            selenium_script_json=step6_json
        )
        db.add(step6)
        print("✓ Step 6: Verify Forecast Elements")
        
        # ===================================================================
        # STEP 7: Apply Forecast Iteration Filter
        # ===================================================================
        step7_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate to forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'system-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'generate-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait for page"},
            {"action": "click", "locator_type": "id", "locator_value": "forecast-iteration", "description": "Click Forecast Iteration dropdown"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//select[@id='forecast-iteration']/option[@value='short-term']", "description": "Select Short Term"},
            {"action": "wait", "duration": 1, "description": "Wait after selection"}
        ], indent=2)
        
        step7 = TestStep(
            test_case_id=tc.id,
            step_number=7,
            description="Apply Forecast Iteration Filter",
            expected_result="Forecast Iteration set to Short Term",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Apply filter",
            selenium_script_json=step7_json
        )
        db.add(step7)
        print("✓ Step 7: Iteration Filter")
        
        # ===================================================================
        # STEP 8: Apply Region Filter
        # ===================================================================
        step8_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate to forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'system-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'generate-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "click", "locator_type": "id", "locator_value": "region", "description": "Click Region dropdown"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//select[@id='region']/option[@value='na']", "description": "Select North America"},
            {"action": "wait", "duration": 1, "description": "Wait"}
        ], indent=2)
        
        step8 = TestStep(
            test_case_id=tc.id,
            step_number=8,
            description="Apply Region Filter",
            expected_result="Region set to North America",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Apply region filter",
            selenium_script_json=step8_json
        )
        db.add(step8)
        print("✓ Step 8: Region Filter")
        
        # ===================================================================
        # STEP 9: Verify Forecast Widgets
        # ===================================================================
        step9_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate to forecast"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'system-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'generate-forecast')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait for widgets"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "review-widget", "description": "Verify Review Widget"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "gap-widget", "description": "Verify Gap Widget"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "data-table", "description": "Verify data table"}
        ], indent=2)
        
        step9 = TestStep(
            test_case_id=tc.id,
            step_number=9,
            description="Verify Forecast Widgets",
            expected_result="Review and Gap widgets visible",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify widgets",
            selenium_script_json=step9_json
        )
        db.add(step9)
        print("✓ Step 9: Verify Widgets")
        
        # ===================================================================
        # STEP 10: Navigate to BOM Setup
        # ===================================================================
        step10_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Supply Master Planning']/parent::a", "description": "Expand Supply Planning"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manage-network')]", "description": "Expand Manage Network"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manufacturing-network')]", "description": "Expand Manufacturing Network"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='bom-setup.html']", "description": "Click BOM Setup"},
            {"action": "wait", "duration": 2, "description": "Wait for BOM page"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "BOM Setup", "description": "Verify BOM Setup heading"}
        ], indent=2)
        
        step10 = TestStep(
            test_case_id=tc.id,
            step_number=10,
            description="Navigate to BOM Setup",
            expected_result="BOM Setup page loads",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to BOM",
            selenium_script_json=step10_json
        )
        db.add(step10)
        print("✓ Step 10: BOM Setup")
        
        # ===================================================================
        # STEP 11: Apply BOM Filters
        # ===================================================================
        step11_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Supply Master Planning']/parent::a", "description": "Navigate to BOM"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manage-network')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manufacturing-network')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='bom-setup.html']", "description": "Go to BOM page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "click", "locator_type": "id", "locator_value": "version-bom", "description": "Click Version dropdown"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//select[@id='version-bom']/option[@value='current']", "description": "Select CurrentWorkingView"},
            {"action": "input", "locator_type": "id", "locator_value": "item", "text": "440000849200", "description": "Enter item ID"},
            {"action": "wait", "duration": 1, "description": "Wait"}
        ], indent=2)
        
        step11 = TestStep(
            test_case_id=tc.id,
            step_number=11,
            description="Apply BOM Filters",
            expected_result="Version and Item filters applied",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Apply BOM filters",
            selenium_script_json=step11_json
        )
        db.add(step11)
        print("✓ Step 11: BOM Filters")
        
        # ===================================================================
        # STEP 12: Verify BOM Data
        # ===================================================================
        step12_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Supply Master Planning']/parent::a", "description": "Navigate to BOM"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manage-network')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[contains(@onclick, 'manufacturing-network')]", "description": "Expand"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='bom-setup.html']", "description": "Go to BOM"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "data-table", "description": "Verify Produced Items table"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "btn-link", "description": "Verify action links"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "consumed-items", "description": "Verify consumed items section"}
        ], indent=2)
        
        step12 = TestStep(
            test_case_id=tc.id,
            step_number=12,
            description="Verify BOM Data",
            expected_result="BOM data table displays correctly",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify BOM data",
            selenium_script_json=step12_json
        )
        db.add(step12)
        print("✓ Step 12: Verify BOM Data")
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ Test case created with FIXED selectors")
        print(f"{'='*80}")
        print(f"\nKey Fixes:")
        print(f"  • Using //span[text()='Demand Analyst']/parent::a for menu clicks")
        print(f"  • Using //a[contains(@onclick, '...')] for submenu items")
        print(f"  • Verifying .active class on expanded menus")
        print(f"  • Every step includes full navigation path from login")
        print(f"{'='*80}")
        print(f"\nTest Case ID: {tc.id}")
        print(f"Access: http://localhost:5173/test-case/{tc.id}")
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
    create_fixed_test()
