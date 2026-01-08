"""
Selenium Service for executing JSON commands
CRITICAL: This service ONLY executes JSON commands, NEVER Python code
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class SeleniumService:
    """Service for executing Selenium JSON commands"""
    
    async def execute_commands(self, commands: list, step_id: int, websocket=None) -> dict:
        """
        Execute a list of JSON Selenium commands
        
        Args:
            commands: List of command dictionaries with 'action' field
            step_id: Test step ID for logging
            websocket: WebSocket connection for live updates
        
        Returns:
            dict: Execution result with status, logs, screenshot
        """
        driver = None
        logs = []
        screenshot_path = None
        
        try:
            # VALIDATION: Ensure we have a list of commands
            if not isinstance(commands, list):
                return {
                    'status': 'failed',
                    'message': f'Commands must be a list, got {type(commands).__name__}',
                    'logs': 'Invalid command format'
                }
            
            if not commands:
                return {
                    'status': 'failed',
                    'message': 'Commands list is empty',
                    'logs': 'No commands to execute'
                }
            
            # VALIDATION: Check first command is a dict with action
            if not isinstance(commands[0], dict) or 'action' not in commands[0]:
                return {
                    'status': 'failed',
                    'message': 'Invalid command format: commands must be dicts with "action" field',
                    'logs': f'First command: {commands[0]}'
                }
            
            print(f"\n{'='*60}")
            print(f"Starting Selenium execution for step {step_id}")
            print(f"Total commands: {len(commands)}")
            print(f"{'='*60}\n")
            
            logs.append(f"=== Selenium Execution Started ===")
            logs.append(f"Step ID: {step_id}")
            logs.append(f"Total commands: {len(commands)}")
            logs.append(f"Timestamp: {datetime.now().isoformat()}")
            logs.append("")
            
            # Initialize WebDriver
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--start-maximized')
            
            # Don't use headless for debugging
            # options.add_argument('--headless')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            logs.append("✓ WebDriver initialized")
            print("✓ WebDriver initialized")
            
            # Send initialization update
            if websocket:
                await websocket.send_message({
                    'type': 'execution_progress',
                    'step_id': step_id,
                    'current': 0,
                    'total': len(commands),
                    'action': 'initialize',
                    'description': 'Browser initialized'
                })
            
            # Execute each command
            for i, command in enumerate(commands, 1):
                action = command.get('action')
                description = command.get('description', 'No description')
                
                log_msg = f"\n[Command {i}/{len(commands)}] {action.upper()}"
                logs.append(log_msg)
                logs.append(f"Description: {description}")
                print(log_msg)
                print(f"  Description: {description}")
                
                # Send progress update via WebSocket
                if websocket:
                    await websocket.send_message({
                        'type': 'execution_progress',
                        'step_id': step_id,
                        'current': i,
                        'total': len(commands),
                        'action': action,
                        'description': description
                    })
                
                try:
                    # Execute the command
                    result = await self._execute_single_command(driver, command)
                    
                    logs.append(f"✓ {result}")
                    print(f"  ✓ {result}")
                    
                    # Take screenshot after each action
                    if action in ['click', 'input', 'navigate']:
                        screenshot_path = self._take_screenshot(driver, step_id, i)
                        
                        if screenshot_path and websocket:
                            await websocket.send_message({
                                'type': 'screenshot_update',
                                'step_id': step_id,
                                'screenshot': screenshot_path
                            })
                    
                except Exception as e:
                    error_msg = f"✗ Command failed: {str(e)}"
                    logs.append(error_msg)
                    print(f"  {error_msg}")
                    
                    # Take error screenshot
                    screenshot_path = self._take_screenshot(driver, step_id, f"error_{i}")
                    
                    return {
                        'status': 'failed',
                        'message': f'Command {i} failed: {str(e)}',
                        'logs': '\n'.join(logs),
                        'screenshot': screenshot_path
                    }
            
            # Final screenshot
            screenshot_path = self._take_screenshot(driver, step_id, 'final')
            
            logs.append("\n=== Execution Complete ===")
            logs.append("Status: PASSED")
            logs.append(f"Executed {len(commands)} commands successfully")
            
            print(f"\n✓ All commands executed successfully!")
            print(f"{'='*60}\n")
            
            return {
                'status': 'passed',
                'message': f'Successfully executed {len(commands)} commands',
                'logs': '\n'.join(logs),
                'screenshot': screenshot_path
            }
            
        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            logs.append(f"\n✗ {error_msg}")
            print(f"\n✗ {error_msg}")
            import traceback
            traceback.print_exc()
            
            if driver:
                screenshot_path = self._take_screenshot(driver, step_id, 'error')
            
            return {
                'status': 'failed',
                'message': error_msg,
                'logs': '\n'.join(logs),
                'screenshot': screenshot_path
            }
            
        finally:
            if driver:
                try:
                    driver.quit()
                    logs.append("\n✓ WebDriver closed")
                    print("✓ WebDriver closed")
                except:
                    pass
    
    async def _execute_single_command(self, driver: webdriver.Chrome, command: dict) -> str:
        """
        Execute a single Selenium command
        
        Args:
            driver: WebDriver instance
            command: Command dictionary
        
        Returns:
            str: Success message
        """
        action = command.get('action')
        
        if action == 'navigate':
            url = command.get('url')
            if not url:
                raise ValueError("Navigate action missing 'url' field")
            driver.get(url)
            return f"Navigated to {url}"
        
        elif action == 'click':
            element = self._find_element(driver, command)
            element.click()
            return f"Clicked element"
        
        elif action == 'input':
            element = self._find_element(driver, command)
            text = command.get('text', '')
            element.clear()
            element.send_keys(text)
            return f"Entered text: {text}"
        
        elif action == 'wait':
            duration = command.get('duration', 1)
            await asyncio.sleep(duration)
            return f"Waited {duration} seconds"
        
        elif action == 'verify_element_present':
            element = self._find_element(driver, command)
            return f"Element verified present"
        
        elif action == 'verify_text':
            element = self._find_element(driver, command)
            expected = command.get('expected_text', '')
            actual = element.text
            
            if expected.lower() in actual.lower():
                return f"Text verified: '{expected}'"
            else:
                raise Exception(f"Text mismatch. Expected: '{expected}', Actual: '{actual}'")
        
        elif action == 'screenshot':
            # Screenshot will be taken automatically
            return "Screenshot captured"
        
        else:
            raise Exception(f"Unknown action: {action}")
    
    def _find_element(self, driver: webdriver.Chrome, command: dict):
        """Find element based on locator type and value"""
        locator_type = command.get('locator_type', 'id')
        locator_value = command.get('locator_value')
        
        if not locator_value:
            raise Exception("No locator_value provided")
        
        by_map = {
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        
        by_type = by_map.get(locator_type)
        if not by_type:
            raise Exception(f"Invalid locator_type: {locator_type}")
        
        wait = WebDriverWait(driver, 10)
        return wait.until(EC.presence_of_element_located((by_type, locator_value)))
    
    def _take_screenshot(self, driver: webdriver.Chrome, step_id: int, suffix: str = '') -> str:
        """Take screenshot and save to disk"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"step_{step_id}_{suffix}_{timestamp}.png"
            
            screenshot_dir = Path(__file__).parent.parent.parent / "screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            
            filepath = screenshot_dir / filename
            driver.save_screenshot(str(filepath))
            
            return str(filepath)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None
