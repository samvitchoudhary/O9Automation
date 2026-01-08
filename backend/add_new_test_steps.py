"""
Add test steps for new Mock O9 features
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestStepStatus, ExecutionStatus
import json

def add_new_test_steps():
    init_db()
    db = SessionLocal()
    
    try:
        # Get test case ID 3 (the fixed test case)
        tc = db.query(TestCase).filter(TestCase.id == 3).first()
        
        if not tc:
            print("Test case 3 not found! Creating new test case...")
            from app.models import TestCaseStatus
            tc = TestCase(
                name="Mock O9 - Fixed Menu Navigation Test",
                description="Test case with properly targeted selectors for Mock O9 website structure.",
                status=TestCaseStatus.APPROVED,
                requirements="Mock O9 running on http://localhost:3001",
                assigned_to="Test Automation Team"
            )
            db.add(tc)
            db.flush()
        
        # Get the current max step number
        max_step = db.query(TestStep).filter(
            TestStep.test_case_id == tc.id
        ).order_by(TestStep.step_number.desc()).first()
        
        next_step_num = (max_step.step_number + 1) if max_step else 1
        
        print(f"\n{'='*80}")
        print(f"Adding New Test Steps to Test Case: {tc.name}")
        print(f"Starting at Step {next_step_num}")
        print(f"{'='*80}\n")
        
        # ===================================================================
        # NEW STEP: Navigate to Forecast Analysis
        # ===================================================================
        forecast_analysis_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait after login"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Expand Demand Analyst"},
            {"action": "wait", "duration": 1, "description": "Wait for submenu"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast-analysis.html']", "description": "Click Forecast Analysis"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Forecast Analysis - Advanced View", "description": "Verify page loaded"}
        ], indent=2)
        
        step_fa = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Navigate to Forecast Analysis Page",
            expected_result="Forecast Analysis page loads with KPI cards and chart",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to forecast analysis",
            selenium_script_json=forecast_analysis_json
        )
        db.add(step_fa)
        print(f"✓ Step {next_step_num}: Navigate to Forecast Analysis")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Verify KPI Cards on Forecast Analysis
        # ===================================================================
        verify_kpis_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait after login"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate to page"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast-analysis.html']", "description": "Go to analysis"},
            {"action": "wait", "duration": 2, "description": "Wait for load"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "forecast-accuracy", "description": "Verify Forecast Accuracy KPI"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "bias", "description": "Verify Bias KPI"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "mape", "description": "Verify MAPE KPI"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "total-volume", "description": "Verify Total Volume KPI"}
        ], indent=2)
        
        step_kpis = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Verify KPI Cards Display on Forecast Analysis",
            expected_result="All four KPI cards are visible with correct IDs",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify KPIs",
            selenium_script_json=verify_kpis_json
        )
        db.add(step_kpis)
        print(f"✓ Step {next_step_num}: Verify KPI Cards")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Change Time Period Filter
        # ===================================================================
        time_period_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Demand Analyst']/parent::a", "description": "Navigate"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='forecast-analysis.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "click", "locator_type": "id", "locator_value": "time-period", "description": "Click time period dropdown"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//select[@id='time-period']/option[@value='last-quarter']", "description": "Select Last Quarter"},
            {"action": "wait", "duration": 1, "description": "Wait after selection"}
        ], indent=2)
        
        step_time = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Change Time Period Filter on Forecast Analysis",
            expected_result="Time period dropdown changes to 'Last Quarter'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Change time period",
            selenium_script_json=time_period_json
        )
        db.add(step_time)
        print(f"✓ Step {next_step_num}: Change Time Period Filter")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Navigate to Inventory Management
        # ===================================================================
        inventory_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Inventory Planning']/parent::a", "description": "Expand Inventory Planning"},
            {"action": "wait", "duration": 1, "description": "Wait for submenu"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='inventory.html']", "description": "Click Inventory Management"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Inventory Management", "description": "Verify page loaded"}
        ], indent=2)
        
        step_inv = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Navigate to Inventory Management Page",
            expected_result="Inventory Management page loads with filters and table",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to inventory",
            selenium_script_json=inventory_json
        )
        db.add(step_inv)
        print(f"✓ Step {next_step_num}: Navigate to Inventory Management")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Filter Inventory by Warehouse
        # ===================================================================
        filter_warehouse_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Inventory Planning']/parent::a", "description": "Navigate"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='inventory.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "click", "locator_type": "id", "locator_value": "warehouse", "description": "Click warehouse dropdown"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//select[@id='warehouse']/option[@value='WH-001']", "description": "Select Warehouse 001"},
            {"action": "wait", "duration": 1, "description": "Wait after selection"}
        ], indent=2)
        
        step_filter = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Filter Inventory by Warehouse",
            expected_result="Warehouse filter set to 'Warehouse 001 - New York'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Filter by warehouse",
            selenium_script_json=filter_warehouse_json
        )
        db.add(step_filter)
        print(f"✓ Step {next_step_num}: Filter by Warehouse")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Verify Inventory Status Badges
        # ===================================================================
        verify_badges_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Inventory Planning']/parent::a", "description": "Navigate"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='inventory.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "status-success", "description": "Verify 'In Stock' badge exists"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "status-warning", "description": "Verify 'Low Stock' badge exists"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "status-danger", "description": "Verify 'Out of Stock' badge exists"}
        ], indent=2)
        
        step_badges = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Verify Inventory Status Badges Display",
            expected_result="Status badges with different colors are visible in the table",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify status badges",
            selenium_script_json=verify_badges_json
        )
        db.add(step_badges)
        print(f"✓ Step {next_step_num}: Verify Status Badges")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Navigate to Supply Planning
        # ===================================================================
        supply_planning_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Supply Master Planning']/parent::a", "description": "Expand Supply Planning"},
            {"action": "wait", "duration": 1, "description": "Wait for submenu"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='supply-planning.html']", "description": "Click Production Schedule"},
            {"action": "wait", "duration": 2, "description": "Wait for page load"},
            {"action": "verify_text", "locator_type": "tag", "locator_value": "h1", "expected_text": "Supply Planning - Production Schedule", "description": "Verify page loaded"}
        ], indent=2)
        
        step_supply = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Navigate to Supply Planning Page",
            expected_result="Supply Planning page loads with production schedule",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to supply planning",
            selenium_script_json=supply_planning_json
        )
        db.add(step_supply)
        print(f"✓ Step {next_step_num}: Navigate to Supply Planning")
        next_step_num += 1
        
        # ===================================================================
        # NEW STEP: Verify Production Schedule Table
        # ===================================================================
        verify_schedule_json = json.dumps([
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//span[text()='Supply Master Planning']/parent::a", "description": "Navigate"},
            {"action": "wait", "duration": 1, "description": "Wait"},
            {"action": "click", "locator_type": "xpath", "locator_value": "//a[@href='supply-planning.html']", "description": "Go to page"},
            {"action": "wait", "duration": 2, "description": "Wait"},
            {"action": "verify_element_present", "locator_type": "id", "locator_value": "production-schedule", "description": "Verify schedule table exists"},
            {"action": "verify_element_present", "locator_type": "xpath", "locator_value": "//td[text()='PO-1001']", "description": "Verify order PO-1001 in table"},
            {"action": "verify_element_present", "locator_type": "class", "locator_value": "status-success", "description": "Verify 'On Track' status"}
        ], indent=2)
        
        step_schedule = TestStep(
            test_case_id=tc.id,
            step_number=next_step_num,
            description="Verify Production Schedule Table",
            expected_result="Production schedule table displays with orders and statuses",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify schedule table",
            selenium_script_json=verify_schedule_json
        )
        db.add(step_schedule)
        print(f"✓ Step {next_step_num}: Verify Production Schedule")
        next_step_num += 1
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ Successfully added {next_step_num - (max_step.step_number + 1 if max_step else 1)} new test steps")
        print(f"{'='*80}")
        print(f"\nNew features covered:")
        print(f"  • Forecast Analysis with KPIs and charts")
        print(f"  • Inventory Management with filtering")
        print(f"  • Supply Planning with production schedule")
        print(f"{'='*80}")
        print(f"\nTest Case ID: {tc.id}")
        print(f"Total Steps: {next_step_num - 1}")
        print(f"{'='*80}\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_new_test_steps()
