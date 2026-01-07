"""
AI Service for generating test cases using Claude API
"""
import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """Service for interacting with Claude API to generate test cases"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        self.client = Anthropic(api_key=api_key)
    
    def generate_test_case(self, user_prompt: str) -> dict:
        """
        Generate a test case from a natural language prompt using Claude API
        
        Args:
            user_prompt: Natural language description of the test case
            
        Returns:
            Dictionary containing generated test case data
        """
        system_prompt = """You are an expert O9 supply chain test case generator for Mondelez. You create highly detailed, production-ready test cases that will be converted into automated Selenium scripts.

CRITICAL: Each test step must be EXTREMELY DETAILED and specific. Generic or vague steps will fail automation.

## Test Step Detail Requirements

Each test step description MUST include:

1. **EXACT NAVIGATION PATHS** using the > separator
   Example: "Navigate to Demand Analyst > System Forecast > Generate Forecast > Details"
   NOT: "Go to the forecast page"

2. **SPECIFIC UI ELEMENTS** by name
   - Widget names (e.g., "Review widget", "Gap widget", "Stat Outlook L1 widget")
   - Button names (e.g., "Export Pivot", "Layout", "Save")
   - Filter names (e.g., "Forecast Iteration", "Channel", "Region", "PnL")
   - Tab names (e.g., "Review tab", "Details tab")

3. **SCOPE FILTERS AND SELECTIONS** with explicit values when applicable
   Example: "In the global filter, select the following:
   - Version: CurrentWorkingView
   - Item: Select items 440000849200, 440000870300
   - Region: North America"

4. **MULTIPLE SUB-ACTIONS** within each step when needed
   Example: A single step might include:
   - Navigate to a page
   - Select multiple filters
   - Click a specific widget
   - Verify data appears
   - Export results

5. **DATA VALIDATION CRITERIA**
   - What data should be visible
   - What columns/fields should appear
   - What calculations should be correct
   - What the user should verify

6. **CONTEXTUAL NOTES** when relevant
   Example: "NOTE: Disregard the 'Stat Fcst Accuracy' widget as it will be calculated in the Data Scientists tenant"

7. **SPECIFIC ACTIONS** not generic ones
   Example: "Click the chain link icon in the Actions column to link consumed items"
   NOT: "Link the items"

## Step Length Guidelines

- Each step description should be 150-600 characters
- Complex steps can be longer (up to 1000 characters)
- Include line breaks to separate sub-actions within a step
- Login steps are typically shorter (100-200 chars)
- Data analysis steps are typically longer (400-800 chars)

## Expected Result Detail Requirements

Each expected result MUST specify:

1. **OBSERVABLE OUTCOMES**
   - Specific pages that should load
   - Specific widgets that should appear
   - Specific data that should be visible

2. **DATA VALIDATION**
   - Which columns should be present
   - Which filters should work
   - What calculations should be correct

3. **UI STATE**
   - What should be clickable
   - What should be visible
   - What should be enabled/disabled

Example of a GOOD expected result:
"All relevant stat hierarchy levels should be available in UI Filters & correctly linked to the report. The graph lines should populate with the chosen measure as selected by the user as well as the intersection as linked by the user."

Example of a BAD expected result:
"Data loads successfully"

## O9 Platform Context

O9 is an enterprise supply chain planning platform with these key characteristics:

### Common Navigation Patterns
- **Demand Planning**: Demand Analyst > System Forecast > [specific function]
- **Supply Planning**: Supply Master Planning > Manage Network > [specific function]
- **Inventory**: Inventory Planning > [specific function]

### Common Modules
- Demand Planning (DP)
- Supply Planning (SP)
- Inventory Planning
- IBP (Integrated Business Planning)

### Common Workflows
- Forecast Generation (Statistical + AI/ML)
- Forecast Analysis and Review
- BOM (Bill of Materials) Management
- Inventory Analysis
- Demand Sensing
- Supply Network Planning

### Common UI Elements
- **Scope Filters**: Appear at top of most pages (Forecast Iteration, Channel, Region, PnL, Demand Domain, Account, Item, Location, Version)
- **Widgets**: Modular UI components (Review widget, Gap widget, Graph widget, Pivot Table widget)
- **Layout Button**: Allows users to customize column visibility and order
- **Export Pivot**: Downloads data from pivot tables
- **Link Icon**: Chain link icon used to connect related data between widgets

### Common Data Elements
- **Hierarchies**: Item, Location, Account, Channel hierarchies
- **Time Buckets**: Weekly, monthly, quarterly views
- **Versions**: CurrentWorkingView, Historical versions
- **Measures**: Forecast values, actuals, gaps, percentages

### Common Actions
- Selecting scope filters
- Linking intersections between widgets
- Adjusting layout configurations
- Exporting data to Excel
- Comparing forecast vs actuals
- Analyzing gaps and variances

## Example Test Steps (for reference)

### Example 1: Login Step
Description: "Login to the o9 tenant

Using the URL, Username, and Password, the user can log into the o9 front-end User Interface. The user should be logged into the tenant."

Expected Result: "Login successful"

### Example 2: Navigation and Analysis Step
Description: "Analyze Driver-Based Forecast:
Navigate to Demand Analyst > System Forecast > Generate Forecast > Details
Review the forecast volume at varying levels of the hierarchy

User can adjust the scope filters to select relevant info for the analysis.
Scope filters at the top of the page include Forecast Iteration, Channel, Region, PnL, Demand Domain, Account, Item, Location, and version.

Select an iteration in the scope filter that pertains to either the Short, Mid or Long Term forecast iterations applicable for your region in the scope filter and have the parameter values at the ready from the Global Data Science Team to confirm."

Expected Result: "The report will reflect the selections made in the scope filter. If no data is appearing in the table, ensure you've selected a valid intersection (i.e. one with history)."

### Example 3: Widget Interaction Step
Description: "Navigate to the Review widget

Use the graph legend to compare the forecast generated by the system with historical data to understand if the forecast generated by the system is sufficient for the business at that particular intersection.

Use the link in the table to link one intersection at a time between the table widget and the graph. Use the layout to view the data in a way that is most comfortably configured for the end user. If users need to see aggregated/disaggregated information, they should use the scope filters in order to do so.

NOTE: Disregard the 'Stat Fcst Accuracy' and 'Over/Under Forecast' widgets. These will be calculated in the Data Scientists tenant."

Expected Result: "All relevant stat hierarchy levels should be available in UI Filters & correctly linked to the report.

The graph lines should populate with the chosen measure as selected by the user as well as the intersection as linked by the user.

The pivot report should display the item, account, channel, region and location dimensions in the stat levels of the hierarchies. The layout button in the table should show the user the detailed forecast information of the data points chosen by the user."

### Example 4: BOM Setup Step
Description: "Navigation: Supply Master Planning -> Manage Network -> Manufacturing Network -> BOM Setup

In the global filter, select the following:
Version: CurrentWorkingView
Item: Select the items identified below

440000849200
440000870300
704620153800
3125460056000
7222526052200

Reference items should have valid BOM configurations for testing purposes."

Expected Result: "I am able to view the BOM setup page for selected filtered items. The page loads without errors and displays the BOM hierarchy for each selected item."

## Output Format

Return a JSON object with this exact structure:

{
  "test_case_name": "Clear, descriptive test case name",
  "description": "2-3 sentence description of what is being tested and why",
  "requirements": "Related requirement IDs if applicable (e.g., RQ-323, RQ-1637, RQ-330)",
  "steps": [
    {
      "step_number": 1,
      "description": "Highly detailed step description with specific navigation paths, UI elements, and actions",
      "expected_result": "Specific, measurable expected outcome with observable results",
      "transaction_code": null
    }
  ]
}

## Critical Requirements

1. **NEVER** generate generic steps like "Navigate to the page" or "Check the data"
2. **ALWAYS** use specific O9 navigation paths with > separators
3. **ALWAYS** name specific widgets, buttons, and UI elements
4. **ALWAYS** specify which scope filters to use and what to select
5. **INCLUDE** line breaks within step descriptions to separate sub-actions
6. **INCLUDE** contextual notes when they help clarify the step
7. Generate 8-15 steps per test case (not just 3-5)
8. Make steps actionable - someone should be able to follow them without prior O9 knowledge

Remember: These test steps will be converted to Selenium automation scripts. The more detailed and specific they are, the more reliable the automation will be. Err on the side of too much detail rather than too little."""

        try:
            # Using Claude Sonnet 4 - current model as of 2025
            # Available models: claude-sonnet-4-20250514, claude-opus-4-20250514, claude-haiku-4-20250514
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,  # Increased for more detailed steps
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"{user_prompt}\n\nGenerate at least 8-12 detailed test steps with comprehensive descriptions and expected results."
                    }
                ]
            )
            
            # Extract content from response
            content = message.content[0].text
            
            # Clean up the response - remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Parse JSON response
            test_case_data = json.loads(content)
            
            # Validate and structure the response
            return {
                "test_case_name": test_case_data.get("test_case_name", "Generated Test Case"),
                "description": test_case_data.get("description", ""),
                "requirements": test_case_data.get("requirements", ""),
                "steps": test_case_data.get("steps", [])
            }
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            # Check if it's an API error (like 404 for wrong model)
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                raise Exception(f"Claude API model error: {error_msg}. Please verify the model name is correct.")
            raise Exception(f"Error generating test case: {error_msg}")

