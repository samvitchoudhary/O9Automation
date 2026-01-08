"""
Create comprehensive Mock O9 test case with all features
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import TestCase, TestStep, TestStepStatus, ExecutionStatus, TestCaseStatus
import json
from datetime import datetime

def create_comprehensive_test_case():
    init_db()
    db = SessionLocal()
    
    try:
        print(f"\n{'='*80}")
        print(f"CREATING COMPREHENSIVE MOCK O9 TEST CASE")
        print(f"{'='*80}\n")
        
        # Create test case
        tc = TestCase(
            name="Mock O9 - Complete Feature Test Suite",
            description="Comprehensive test covering all Mock O9 features: Dashboard, Demand Analysis, Forecast Analysis, Inventory Management, Supply Planning, and BOM Setup. Auto-login is built-in.",
            status=TestCaseStatus.APPROVED,
            requirements="Mock O9 running on http://localhost:3001. Backend auto-executes Step 1 (login) before all other steps.",
            assigned_to="Test Automation Team"
        )
        
        db.add(tc)
        db.flush()  # Get the ID
        
        print(f"✓ Created test case: {tc.name}")
        print(f"  ID: {tc.id}")
        print(f"\nAdding test steps...\n")
        
        steps = []
        
        # ================================================================
        # STEP 1: Login (Foundation for auto-login)
        # ================================================================
        login_json = json.dumps([
            {
                "action": "navigate",
                "url": "http://localhost:3001",
                "description": "Navigate to Mock O9 login page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait for page load"
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
                "description": "Wait for login to complete"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Welcome to O9 Platform",
                "description": "Verify dashboard loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=1,
            description="Login to Mock O9 Platform\n\nNavigate to http://localhost:3001 and authenticate with testuser/password123. This step is automatically executed before all other steps.",
            expected_result="User successfully logs in and sees dashboard with 'Welcome to O9 Platform' heading",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Login to Mock O9\n# This step is auto-executed before all other steps",
            selenium_script_json=login_json
        ))
        print("✓ Step 1: Login")
        
        # ================================================================
        # STEP 2: Verify Dashboard Widgets
        # ================================================================
        dashboard_json = json.dumps([
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
                "locator_value": "sidebar",
                "description": "Verify sidebar present"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "widget",
                "description": "Verify at least one widget"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=2,
            description="Verify Dashboard Loads with Widgets\n\nAfter login (auto-executed), verify dashboard displays with widgets and sidebar.",
            expected_result="Dashboard displays with widgets container, sidebar, and at least one widget visible",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify dashboard widgets",
            selenium_script_json=dashboard_json
        ))
        print("✓ Step 2: Verify Dashboard")
        
        # ================================================================
        # STEP 3: Expand Demand Analyst Menu
        # ================================================================
        demand_analyst_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
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
                "description": "Verify menu expanded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=3,
            description="Expand Demand Analyst Menu\n\nAfter login, expand the Demand Analyst menu to reveal submenu options.",
            expected_result="Demand Analyst submenu expands and shows System Forecast and other options",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Expand Demand Analyst",
            selenium_script_json=demand_analyst_json
        ))
        print("✓ Step 3: Expand Demand Analyst")
        
        # ================================================================
        # STEP 4: Navigate to Forecast Page
        # ================================================================
        forecast_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
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
                "locator_value": "//a[contains(@onclick, 'system-forecast')]",
                "description": "Click System Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'generate-forecast')]",
                "description": "Click Generate Forecast"
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
                "description": "Wait for page load"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "Generate Forecast",
                "description": "Verify forecast page loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=4,
            description="Navigate to System Forecast Page\n\nAfter login, navigate through menu: Demand Analyst → System Forecast → Generate Forecast → Details.",
            expected_result="System Forecast page loads with 'Generate Forecast' heading and filters",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to forecast",
            selenium_script_json=forecast_json
        ))
        print("✓ Step 4: Navigate to Forecast")
        
        # ================================================================
        # STEP 5: Verify Forecast Filters
        # ================================================================
        forecast_filters_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
                "description": "Navigate to page"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'system-forecast')]",
                "description": "System Forecast"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'generate-forecast')]",
                "description": "Generate Forecast"
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
                "description": "Details"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "forecast-iteration",
                "description": "Verify forecast iteration filter"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "region",
                "description": "Verify region filter"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=5,
            description="Verify Forecast Page Filters Display\n\nAfter login, navigate to forecast page and verify filters are present.",
            expected_result="Forecast iteration and region filters are visible on the page",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify filters",
            selenium_script_json=forecast_filters_json
        ))
        print("✓ Step 5: Verify Forecast Filters")
        
        # ================================================================
        # STEP 6: Navigate to Forecast Analysis
        # ================================================================
        forecast_analysis_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
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
                "locator_value": "//a[@href='forecast-analysis.html']",
                "description": "Click Forecast Analysis"
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
                "expected_text": "Forecast Analysis - Advanced View",
                "description": "Verify page loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=6,
            description="Navigate to Forecast Analysis Page\n\nAfter login, navigate: Demand Analyst → Forecast Analysis.",
            expected_result="Forecast Analysis page loads with 'Forecast Analysis - Advanced View' heading",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to forecast analysis",
            selenium_script_json=forecast_analysis_json
        ))
        print("✓ Step 6: Navigate to Forecast Analysis")
        
        # ================================================================
        # STEP 7: Verify KPI Cards on Forecast Analysis
        # ================================================================
        kpi_cards_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast-analysis.html']",
                "description": "Go to analysis"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "forecast-accuracy",
                "description": "Verify Forecast Accuracy KPI"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "bias",
                "description": "Verify Bias KPI"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "mape",
                "description": "Verify MAPE KPI"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "total-volume",
                "description": "Verify Total Volume KPI"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=7,
            description="Verify KPI Cards on Forecast Analysis\n\nAfter login, navigate to Forecast Analysis and verify all KPI cards display.",
            expected_result="All four KPI cards are visible: Forecast Accuracy, Bias, MAPE, and Total Volume",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify KPIs",
            selenium_script_json=kpi_cards_json
        ))
        print("✓ Step 7: Verify KPI Cards")
        
        # ================================================================
        # STEP 8: Test Time Period Filter on Forecast Analysis
        # ================================================================
        time_period_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Demand Analyst']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='forecast-analysis.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "id",
                "locator_value": "time-period",
                "description": "Click time period dropdown"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//select[@id='time-period']/option[@value='last-quarter']",
                "description": "Select Last Quarter"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after selection"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=8,
            description="Change Time Period Filter on Forecast Analysis\n\nAfter login, navigate to Forecast Analysis and change time period to 'Last Quarter'.",
            expected_result="Time period filter changes to 'Last Quarter'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Test time filter",
            selenium_script_json=time_period_json
        ))
        print("✓ Step 8: Test Time Period Filter")
        
        # ================================================================
        # STEP 9: Navigate to Inventory Management
        # ================================================================
        inventory_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Inventory Planning']/parent::a",
                "description": "Expand Inventory Planning"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='inventory.html']",
                "description": "Click Inventory Management"
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
                "expected_text": "Inventory Management",
                "description": "Verify page loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=9,
            description="Navigate to Inventory Management Page\n\nAfter login, navigate: Inventory Planning → Inventory Management.",
            expected_result="Inventory Management page loads with 'Inventory Management' heading",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to inventory",
            selenium_script_json=inventory_json
        ))
        print("✓ Step 9: Navigate to Inventory")
        
        # ================================================================
        # STEP 10: Verify Inventory KPI Cards
        # ================================================================
        inventory_kpis_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Inventory Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='inventory.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "kpi-cards",
                "description": "Verify KPI cards container"
            },
            {
                "action": "verify_element_present",
                "locator_type": "xpath",
                "locator_value": "//h3[text()='Total Items']",
                "description": "Verify Total Items KPI"
            },
            {
                "action": "verify_element_present",
                "locator_type": "xpath",
                "locator_value": "//h3[text()='Low Stock Alerts']",
                "description": "Verify Low Stock KPI"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=10,
            description="Verify Inventory KPI Cards Display\n\nAfter login, navigate to Inventory Management and verify KPI cards display.",
            expected_result="KPI cards show Total Items, Total Value, Low Stock Alerts, and Out of Stock",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify inventory KPIs",
            selenium_script_json=inventory_kpis_json
        ))
        print("✓ Step 10: Verify Inventory KPIs")
        
        # ================================================================
        # STEP 11: Filter Inventory by Warehouse
        # ================================================================
        filter_warehouse_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Inventory Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='inventory.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "id",
                "locator_value": "warehouse",
                "description": "Click warehouse dropdown"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//select[@id='warehouse']/option[@value='WH-003']",
                "description": "Select Warehouse 003"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after selection"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=11,
            description="Filter Inventory by Warehouse\n\nAfter login, navigate to Inventory Management and filter by Warehouse 003.",
            expected_result="Warehouse filter set to 'Warehouse 003 - Chicago'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Filter by warehouse",
            selenium_script_json=filter_warehouse_json
        ))
        print("✓ Step 11: Filter by Warehouse")
        
        # ================================================================
        # STEP 12: Verify Inventory Status Badges
        # ================================================================
        status_badges_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Inventory Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='inventory.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "status-success",
                "description": "Verify In Stock badge"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "status-warning",
                "description": "Verify Low Stock badge"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "status-danger",
                "description": "Verify Out of Stock badge"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=12,
            description="Verify Inventory Status Badges Display\n\nAfter login, navigate to Inventory Management and verify status badges display with different colors.",
            expected_result="Status badges show with different colors: green (In Stock), yellow (Low Stock), red (Out of Stock)",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify badges",
            selenium_script_json=status_badges_json
        ))
        print("✓ Step 12: Verify Status Badges")
        
        # ================================================================
        # STEP 13: Navigate to Supply Planning
        # ================================================================
        supply_planning_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Supply Master Planning']/parent::a",
                "description": "Expand Supply Planning"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait for submenu"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='supply-planning.html']",
                "description": "Click Production Schedule"
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
                "expected_text": "Supply Planning - Production Schedule",
                "description": "Verify page loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=13,
            description="Navigate to Supply Planning Page\n\nAfter login, navigate: Supply Master Planning → Production Schedule.",
            expected_result="Supply Planning page loads with 'Supply Planning - Production Schedule' heading",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to supply planning",
            selenium_script_json=supply_planning_json
        ))
        print("✓ Step 13: Navigate to Supply Planning")
        
        # ================================================================
        # STEP 14: Verify Production Schedule Table
        # ================================================================
        production_schedule_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Supply Master Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='supply-planning.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "verify_element_present",
                "locator_type": "id",
                "locator_value": "production-schedule",
                "description": "Verify schedule table exists"
            },
            {
                "action": "verify_element_present",
                "locator_type": "xpath",
                "locator_value": "//td[text()='PO-1001']",
                "description": "Verify order PO-1001"
            },
            {
                "action": "verify_element_present",
                "locator_type": "class",
                "locator_value": "status-success",
                "description": "Verify On Track status"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=14,
            description="Verify Production Schedule Table\n\nAfter login, navigate to Supply Planning and verify production schedule table displays.",
            expected_result="Production schedule table displays with orders (PO-1001, etc.) and status badges",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify schedule",
            selenium_script_json=production_schedule_json
        ))
        print("✓ Step 14: Verify Production Schedule")
        
        # ================================================================
        # STEP 15: Test Planning Horizon Filter
        # ================================================================
        planning_horizon_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Supply Master Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[@href='supply-planning.html']",
                "description": "Go to page"
            },
            {
                "action": "wait",
                "duration": 2,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "id",
                "locator_value": "planning-horizon",
                "description": "Click planning horizon dropdown"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//select[@id='planning-horizon']/option[@value='3-months']",
                "description": "Select 3 Months"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after selection"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=15,
            description="Change Planning Horizon Filter\n\nAfter login, navigate to Supply Planning and change planning horizon to '3 Months'.",
            expected_result="Planning horizon filter changes to '3 Months'",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Test planning filter",
            selenium_script_json=planning_horizon_json
        ))
        print("✓ Step 15: Test Planning Horizon")
        
        # ================================================================
        # STEP 16: Navigate to BOM Setup
        # ================================================================
        bom_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Supply Master Planning']/parent::a",
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
                "locator_value": "//a[contains(@onclick, 'manage-network')]",
                "description": "Click Manage Network"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'manufacturing-network')]",
                "description": "Click Manufacturing Network"
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
                "description": "Wait for page load"
            },
            {
                "action": "verify_text",
                "locator_type": "tag",
                "locator_value": "h1",
                "expected_text": "BOM Setup",
                "description": "Verify page loaded"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=16,
            description="Navigate to BOM Setup Page\n\nAfter login, navigate: Supply Master Planning → Manage Network → Manufacturing Network → BOM Setup.",
            expected_result="BOM Setup page loads with 'BOM Setup' heading",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Navigate to BOM",
            selenium_script_json=bom_json
        ))
        print("✓ Step 16: Navigate to BOM Setup")
        
        # ================================================================
        # STEP 17: Verify BOM Table
        # ================================================================
        bom_table_json = json.dumps([
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait after login"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//span[text()='Supply Master Planning']/parent::a",
                "description": "Navigate"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'manage-network')]",
                "description": "Manage Network"
            },
            {
                "action": "wait",
                "duration": 1,
                "description": "Wait"
            },
            {
                "action": "click",
                "locator_type": "xpath",
                "locator_value": "//a[contains(@onclick, 'manufacturing-network')]",
                "description": "Manufacturing"
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
                "description": "BOM Setup"
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
                "description": "Verify BOM table exists"
            },
            {
                "action": "verify_element_present",
                "locator_type": "xpath",
                "locator_value": "//th[text()='Item']",
                "description": "Verify table headers"
            }
        ], indent=2)
        
        steps.append(TestStep(
            test_case_id=tc.id,
            step_number=17,
            description="Verify BOM Table Display\n\nAfter login, navigate to BOM Setup and verify BOM table displays with data.",
            expected_result="BOM table displays with headers and component data",
            status=TestStepStatus.NOT_STARTED,
            execution_status=ExecutionStatus.NOT_RUN,
            selenium_script="# Verify BOM table",
            selenium_script_json=bom_table_json
        ))
        print("✓ Step 17: Verify BOM Table")
        
        # Add all steps to database
        for step in steps:
            db.add(step)
        
        db.commit()
        
        print(f"\n{'='*80}")
        print(f"✓ SUCCESSFULLY CREATED {len(steps)} TEST STEPS")
        print(f"{'='*80}")
        print(f"\nTest Case Summary:")
        print(f"  ID: {tc.id}")
        print(f"  Name: {tc.name}")
        print(f"  Total Steps: {len(steps)}")
        print(f"\nFeatures Covered:")
        print(f"  • Basic: Login, Dashboard verification")
        print(f"  • Demand Analysis: Menu navigation, Forecast pages")
        print(f"  • Forecast Analysis: KPIs, charts, filters")
        print(f"  • Inventory: KPIs, filters, status badges")
        print(f"  • Supply Planning: Production schedule, filters")
        print(f"  • BOM Setup: Table verification")
        print(f"\nKey Features:")
        print(f"  ✓ All steps use JSON-only format")
        print(f"  ✓ Auto-login built-in (Step 1)")
        print(f"  ✓ Correct XPath selectors")
        print(f"  ✓ Complete navigation paths")
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
    create_comprehensive_test_case()
