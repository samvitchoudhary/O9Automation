"""
AI Service for generating Selenium scripts from test step descriptions
"""
import os
import json
import logging
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


def generate_selenium_script(step_description: str, expected_result: str, step_number: int = 1) -> dict:
    """
    Generate Selenium script from test step description using Claude API
    
    Args:
        step_description: Description of the test step
        expected_result: Expected result of the step
        step_number: Step number in the test case (1 = first step, 2+ = subsequent steps)
    
    Returns:
        dict with 'selenium_script' (Python) and 'selenium_script_json' (JSON commands)
    """
    
    logger.info(f"Starting Selenium script generation for step {step_number}: {step_description[:50]}...")
    
    try:
        # Check API key exists
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        logger.debug(f"API Key found: {api_key[:10]}...")
        
        client = Anthropic(api_key=api_key)
        
        # Get mock O9 URL from environment or use default
        mock_url = os.getenv('O9_MOCK_URL', 'http://localhost:3001')
        
        # Determine if this is Step 1 (login) or Step 2+ (sequential)
        is_first_step = step_number == 1
        
        # Also check if description mentions login
        is_login = 'login' in step_description.lower() or 'authenticate' in step_description.lower() or 'sign in' in step_description.lower()
        
        # Step 1 should always have navigate, Step 2+ should never have navigate
        should_include_navigate = is_first_step or is_login
        
        # CRITICAL: Use regular string (not f-string) to avoid format specifier errors with JSON braces
        # We'll replace {MOCK_URL} placeholder manually
        system_prompt = """You are a Selenium test automation expert.

Your task: Convert a test step description into Selenium commands.

## Output Format

You must return a JSON object with exactly this structure:

{
  "json_script": [array of command objects],
  "python_script": "python code as a string"
}

## JSON Commands

The json_script array contains command objects. Each command has:
- action: The type of action
- Other fields depending on the action type

### Available Commands:

1. navigate - Go to a URL
{
  "action": "navigate",
  "url": "http://localhost:3001",
  "description": "Navigate to page"
}

2. click - Click an element
{
  "action": "click",
  "locator_type": "id",
  "locator_value": "button-id",
  "description": "Click button"
}

3. input - Type text into a field
{
  "action": "input",
  "locator_type": "id",
  "locator_value": "field-id",
  "text": "text to type",
  "description": "Enter text"
}

4. wait - Pause for a duration
{
  "action": "wait",
  "duration": 2,
  "description": "Wait 2 seconds"
}

5. verify_element_present - Check if element exists
{
  "action": "verify_element_present",
  "locator_type": "class",
  "locator_value": "element-class",
  "description": "Verify element is present"
}

6. verify_text - Verify text is present in element
{
  "action": "verify_text",
  "locator_type": "xpath",
  "locator_value": "//div[@class='message']",
  "expected_text": "Success",
  "description": "Verify success message"
}

### Locator Types:
- id
- xpath  
- css
- class
- name
- tag
- link_text
- partial_link_text

## Rules

1. For LOGIN steps: Start with a navigate command to {MOCK_URL}
2. For other steps: Do NOT include navigate - assume already on the page
3. Use simple locators (id, class) when possible
4. Add wait commands after navigation and clicks
5. Verify expected results with verify_element_present or verify_text

## Example for Login

{
  "json_script": [
    {"action": "navigate", "url": "{MOCK_URL}", "description": "Go to O9"},
    {"action": "input", "locator_type": "id", "locator_value": "username", "text": "testuser", "description": "Enter username"},
    {"action": "input", "locator_type": "id", "locator_value": "password", "text": "password123", "description": "Enter password"},
    {"action": "click", "locator_type": "id", "locator_value": "login-button", "description": "Click login"},
    {"action": "wait", "duration": 2, "description": "Wait for login"},
    {"action": "verify_element_present", "locator_type": "class", "locator_value": "main-content", "description": "Verify dashboard"}
  ],
  "python_script": "# Login script\\ndriver.get('{MOCK_URL}')\\nusername = driver.find_element(By.ID, 'username')\\nusername.send_keys('testuser')\\npassword = driver.find_element(By.ID, 'password')\\npassword.send_keys('password123')\\nlogin_btn = driver.find_element(By.ID, 'login-button')\\nlogin_btn.click()\\ndriver.quit()"
}

## Important

- Return ONLY the JSON object
- Do NOT include markdown code blocks
- Do NOT include explanatory text
- The python_script is for display only - it can be simpler/incomplete
- The json_script is what gets executed - it must be complete and correct
- For non-login steps, do NOT include navigate action"""

        # Replace {MOCK_URL} placeholder with actual URL (using string replace, not format)
        system_prompt = system_prompt.replace('{MOCK_URL}', mock_url)

        # Determine if this is Step 1 (login) or Step 2+ (sequential)
        is_first_step = step_number == 1
        
        # Build user message with context
        if should_include_navigate:
            step_context = f"This is Step {step_number} (login/initial step). Include a navigate action to {mock_url} as the FIRST command."
        else:
            step_context = f"This is Step {step_number} (a subsequent step after login). DO NOT include any navigate action. Start directly with click or input actions."
        
        user_prompt = f"""Test Step: {step_description}

Expected Result: {expected_result}

Context: {step_context}

Generate the Selenium commands for this step."""

        logger.debug("Sending request to Claude API...")
        
        # Synchronous call - NO await (using sync Anthropic client)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0.3,  # Lower temperature for more consistent code
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        
        logger.debug(f"Received response from Claude API")
        logger.debug(f"Message type: {type(message)}")
        
        # Access message content directly (synchronous - no await needed)
        # Check if message is a coroutine (shouldn't be with sync client, but defensive check)
        if hasattr(message, '__await__'):
            raise RuntimeError("Received coroutine instead of message object. Ensure you're using anthropic.Anthropic (sync) not AsyncAnthropic (async)")
        
        # Access content safely
        if not hasattr(message, 'content'):
            raise ValueError(f"Message object missing 'content' attribute. Message type: {type(message)}")
        
        if not message.content:
            raise ValueError("Message content is empty")
        
        if not isinstance(message.content, list):
            raise ValueError(f"Message content is not a list. Got: {type(message.content)}")
        
        if len(message.content) == 0:
            raise ValueError("Message content list is empty")
        
        # Get the first content block
        first_content = message.content[0]
        
        if not hasattr(first_content, 'text'):
            raise ValueError(f"Content block missing 'text' attribute. Content type: {type(first_content)}")
        
        response_text = first_content.text
        
        logger.debug(f"Response text (first 200 chars): {response_text[:200]}")
        
        # Clean up response - remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
            logger.info("Successfully parsed AI response")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"AI returned invalid JSON: {str(e)}")
        
        # Validate response structure
        if 'json_script' not in result or 'python_script' not in result:
            logger.error(f"Response missing required fields. Got: {list(result.keys())}")
            raise ValueError("AI response missing required fields (json_script or python_script)")
        
        # CRITICAL: Verify JSON script for non-login steps doesn't have navigate
        json_commands = result['json_script']
        if not should_include_navigate and json_commands:
            # Check if first command is navigate
            if json_commands[0].get('action') == 'navigate':
                logger.warning(f"Step {step_number} has navigate action but shouldn't. Removing it...")
                # Remove the navigate command
                json_commands = [cmd for cmd in json_commands if cmd.get('action') != 'navigate']
                if not json_commands:
                    raise ValueError("After removing navigate action, no commands remain. Step may need regeneration.")
                logger.info(f"Removed navigate action. Remaining commands: {len(json_commands)}")
        
        # Validate JSON script is a list
        if not isinstance(json_commands, list):
            raise ValueError(f"json_script must be a list, got {type(json_commands)}")
        
        logger.info(f"Generated {len(json_commands)} JSON commands for step {step_number}")
        if json_commands:
            logger.info(f"First command: {json_commands[0].get('action')}")
        
        return {
            'selenium_script': result['python_script'],
            'selenium_script_json': json.dumps(json_commands, indent=2)
        }
        
    except ValueError as e:
        # Re-raise ValueError (these are our validation errors)
        raise
    except Exception as e:
        from anthropic import APIError
        
        if isinstance(e, APIError):
            logger.error(f"Anthropic API Error: {type(e).__name__} - {str(e)}")
            error_detail = str(e)
            raise Exception(f"Anthropic API Error: {error_detail}")
        elif isinstance(e, json.JSONDecodeError):
            logger.error(f"JSON Parse Error: {e}")
            logger.error(f"Response was: {response_text if 'response_text' in locals() else 'No response'}")
            raise Exception(f"Failed to parse AI response: {str(e)}")
        else:
            logger.error(f"Unexpected error in generate_selenium_script: {type(e).__name__} - {str(e)}")
            logger.exception(e)  # Log full traceback
            raise Exception(f"Script generation error: {str(e)}")

