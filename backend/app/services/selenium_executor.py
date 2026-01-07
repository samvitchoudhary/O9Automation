"""
Selenium Executor Service for running automated test steps
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import platform
import subprocess
from typing import Optional, Dict, Any, Callable

# Try to import webdriver_manager, but don't fail if it's not available
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class SeleniumExecutor:
    """Manages Selenium browser sessions and executes test commands"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.session_active = False  # Track if browser session is active
        
    def initialize_browser(self, headless: bool = True):
        """
        Initialize Chrome browser with proper Mac support
        
        Uses Selenium Manager (built-in) by default, which automatically handles
        ChromeDriver installation and Mac ARM/Intel detection.
        Falls back to webdriver-manager with path fixes if needed.
        
        If browser is already initialized and active, reuses the existing session.
        """
        # Reuse existing session if available and active
        if self.driver is not None and self.session_active:
            try:
                # Check if browser is still alive
                self.driver.current_url
                print("Browser session already active, reusing existing session")
                return
            except Exception:
                # Browser was closed, need to reinitialize
                print("Previous browser session closed, initializing new session")
                self.driver = None
                self.wait = None
                self.session_active = False
        
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        
        try:
            # Solution 4: Use Selenium Manager (built-in, most reliable)
            # Selenium 4.6+ automatically handles ChromeDriver management
            # This works on Mac ARM64, Intel, Linux, and Windows
            print("Initializing browser with Selenium Manager...")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.session_active = True
            print("✓ Browser initialized successfully with Selenium Manager")
            
        except Exception as e:
            print(f"Selenium Manager failed: {e}")
            print("Falling back to webdriver-manager with Mac path fixes...")
            
            # Fallback: Use webdriver-manager with Mac-specific path resolution
            if not WEBDRIVER_MANAGER_AVAILABLE:
                raise RuntimeError(
                    "Selenium Manager failed and webdriver-manager is not available. "
                    "Please install webdriver-manager: pip install webdriver-manager"
                )
            
            try:
                driver_path = ChromeDriverManager().install()
                
                # CRITICAL FIX: On Mac, the driver might be in a subdirectory
                # ChromeDriverManager sometimes returns path to directory or wrong file
                if platform.system() == 'Darwin':  # macOS
                    # Check if path points to a directory
                    if os.path.isdir(driver_path):
                        # Look for chromedriver executable in the directory
                        for file in os.listdir(driver_path):
                            file_path = os.path.join(driver_path, file)
                            if file == 'chromedriver' and os.path.isfile(file_path):
                                driver_path = file_path
                                break
                    
                    # Check if path points to wrong file (like THIRD_PARTY_NOTICES)
                    if 'THIRD_PARTY' in driver_path or not driver_path.endswith('chromedriver'):
                        # Find the actual chromedriver in parent directories
                        parent_dir = os.path.dirname(driver_path)
                        possible_paths = [
                            os.path.join(parent_dir, 'chromedriver'),
                            os.path.join(os.path.dirname(parent_dir), 'chromedriver'),
                        ]
                        
                        for path in possible_paths:
                            if os.path.exists(path) and os.path.isfile(path):
                                driver_path = path
                                break
                    
                    # Make sure the driver has execute permissions
                    if os.path.exists(driver_path):
                        os.chmod(driver_path, 0o755)
                        # Remove Mac quarantine attribute
                        try:
                            subprocess.run(
                                ['xattr', '-d', 'com.apple.quarantine', driver_path],
                                capture_output=True,
                                check=False
                            )
                        except Exception:
                            pass  # xattr might not be available, continue anyway
                
                print(f"Using ChromeDriver at: {driver_path}")
                
                # Verify it's actually the chromedriver executable
                if not os.path.exists(driver_path):
                    raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")
                
                if 'THIRD_PARTY' in driver_path:
                    raise ValueError(
                        f"ChromeDriverManager returned wrong file: {driver_path}. "
                        "Please clear cache: rm -rf ~/.wdm"
                    )
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.wait = WebDriverWait(self.driver, 10)
                self.session_active = True
                print("✓ Browser initialized successfully with webdriver-manager")
                
            except Exception as fallback_error:
                error_msg = (
                    f"Failed to initialize browser with both methods.\n"
                    f"Selenium Manager error: {e}\n"
                    f"WebDriver Manager error: {fallback_error}\n\n"
                    f"Try these solutions:\n"
                    f"1. Clear webdriver cache: rm -rf ~/.wdm\n"
                    f"2. Update Selenium: pip install --upgrade selenium\n"
                    f"3. Manually install ChromeDriver to /usr/local/bin/chromedriver"
                )
                raise RuntimeError(error_msg) from fallback_error
        
    def close_browser(self):
        """Close browser session"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass  # Browser may already be closed
            self.driver = None
            self.wait = None
            self.session_active = False
            print("Browser session closed")
            
    def execute_script(self, script_json: str, emit_callback: Optional[Callable] = None, keep_alive: bool = False) -> Dict[str, Any]:
        """
        Execute Selenium commands from JSON format ONLY.
        
        CRITICAL: This method will NEVER execute Python code.
        It ONLY accepts and executes JSON command arrays.
        
        Args:
            script_json: JSON string containing array of command objects
            emit_callback: Optional callback for real-time updates
            keep_alive: If True, keep browser open after execution
            
        Returns:
            dict with status, execution_time_ms, error_message
        """
        start_time = time.time()
        
        import logging
        logger = logging.getLogger(__name__)
        logger.info("=== STARTING SCRIPT EXECUTION ===")
        logger.debug(f"Received script (first 200 chars): {script_json[:200]}")
        
        try:
            # VALIDATION 1: Check for Python code indicators
            script_lower = script_json.lower()
            python_indicators = [
                'import ', 'from ', 'driver = webdriver', 
                'def ', 'class ', 'print(', '.quit()'
            ]
            
            for indicator in python_indicators:
                if indicator in script_lower:
                    raise ValueError(
                        f"Detected Python code in script (found '{indicator}'). "
                        f"This system ONLY executes JSON commands. "
                        f"The Python script is for display only."
                    )
            
            # VALIDATION 2: Must not start with Python keywords
            script_stripped = script_json.strip()
            if script_stripped.startswith('from selenium') or script_stripped.startswith('import'):
                raise ValueError(
                    "Received Python script instead of JSON commands. "
                    "The system should execute selenium_script_json (JSON), not selenium_script (Python)."
                )
            
            # Initialize browser if needed
            if not self.driver or not self.session_active:
                logger.info("Initializing browser...")
                self.initialize_browser()
            
            # VALIDATION 3: Parse as JSON
            try:
                commands = json.loads(script_json)
                logger.info(f"Parsed JSON successfully")
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                logger.error(f"Received data (first 500 chars): {script_json[:500]}")
                raise ValueError(f"Invalid JSON format: {str(e)}. Expected JSON array of commands.")
            
            # VALIDATION 4: Must be a list
            if not isinstance(commands, list):
                raise ValueError(
                    f"Script must be a JSON array, got {type(commands).__name__}. "
                    f"This endpoint does NOT execute Python code."
                )
            
            # VALIDATION 5: All items must be dicts with 'action' key
            if len(commands) == 0:
                raise ValueError("Empty command list. No actions to execute.")
            
            for idx, cmd in enumerate(commands):
                if not isinstance(cmd, dict):
                    raise ValueError(
                        f"Command {idx+1} is not a JSON object (got {type(cmd).__name__})"
                    )
                if 'action' not in cmd:
                    raise ValueError(
                        f"Command {idx+1} missing 'action' field. "
                        f"Valid actions: navigate, click, input, wait, verify_element_present"
                    )
            
            logger.info(f"✓ Validation passed - executing {len(commands)} JSON commands")
            
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"=== EXECUTING JSON SCRIPT ===")
            logger.info(f"Number of commands: {len(commands)}")
            if commands:
                first_cmd = commands[0]
                logger.info(f"First command: {first_cmd.get('action')} - {first_cmd.get('description', '')[:50]}")
                if first_cmd.get('action') == 'navigate':
                    logger.info(f"  Navigate URL: {first_cmd.get('url')}")
            
            for idx, command in enumerate(commands):
                action = command.get('action')
                description = command.get('description', action)
                
                # Log the command
                logger.info(f"Step {idx+1}/{len(commands)}: {action} - {description}")
                if action == 'navigate':
                    url = command.get('url')
                    logger.info(f"  URL: {url}")
                    if not url or not url.startswith('http'):
                        logger.warning(f"  ⚠ Invalid URL format: {url}")
                
                # Emit progress update
                if emit_callback:
                    emit_callback('progress', {
                        'step': idx + 1,
                        'total': len(commands),
                        'action': action,
                        'message': description
                    })
                
                # Execute command
                self._execute_command(command)
                
                # Capture screenshot for live view
                if emit_callback and self.driver:
                    try:
                        screenshot = self.driver.get_screenshot_as_base64()
                        emit_callback('screenshot', {
                            'image': screenshot,
                            'step': idx + 1
                        })
                    except Exception as e:
                        logger.warning(f"Screenshot capture failed: {e}")
                
                time.sleep(0.5)  # Small delay between actions
            
            execution_time = int((time.time() - start_time) * 1000)
            
            # Keep session alive if requested (for sequential test execution)
            if not keep_alive:
                self.close_browser()
            
            logger.info(f"Execution completed successfully in {execution_time}ms")
            
            return {
                'status': 'passed',
                'execution_time_ms': execution_time,
                'error_message': None
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Received data (first 500 chars): {script_json[:500]}...")
            
            execution_time = int((time.time() - start_time) * 1000)
            
            if not keep_alive:
                self.close_browser()
            
            return {
                'status': 'error',
                'execution_time_ms': execution_time,
                'error_message': f"Invalid script format: {str(e)}"
            }
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            logger.error(f"Execution error: {error_msg}")
            logger.exception(e)
            
            # Close browser on error unless keep_alive is True
            if not keep_alive:
                self.close_browser()
            
            return {
                'status': 'error',
                'execution_time_ms': execution_time,
                'error_message': error_msg
            }
    
    def _execute_command(self, command: Dict[str, Any]):
        """
        Execute a single Selenium command with validation
        
        Args:
            command: Dictionary with 'action' and other action-specific fields
        """
        action = command.get('action')
        
        if not action:
            raise ValueError("Command missing 'action' field")
        
        if action == 'navigate':
            url = command.get('url')
            
            # CRITICAL: Validate URL before navigation
            if not url:
                raise ValueError("Navigate action missing URL field")
            
            if not isinstance(url, str):
                raise ValueError(f"URL must be a string, got {type(url)}: {url}")
            
            url = url.strip()
            
            if not url:
                raise ValueError("Navigate action has empty URL")
            
            # Validate URL format - must start with http:// or https://
            if not url.startswith('http://') and not url.startswith('https://'):
                raise ValueError(
                    f"Invalid URL format (missing protocol): '{url}'. "
                    f"URL must start with http:// or https://. "
                    f"For O9 testing, use: http://localhost:3001"
                )
            
            print(f"Navigating to: {url}")
            self.driver.get(url)
            
        elif action == 'click':
            locator_type = command.get('locator_type')
            locator_value = command.get('locator_value')
            
            if not locator_type or not locator_value:
                raise ValueError("click action requires 'locator_type' and 'locator_value' fields")
            
            element = self._find_element(locator_type, locator_value)
            element.click()
            
        elif action == 'input':
            locator_type = command.get('locator_type')
            locator_value = command.get('locator_value')
            text = command.get('text', '')
            
            if not locator_type or not locator_value:
                raise ValueError("input action requires 'locator_type' and 'locator_value' fields")
            
            element = self._find_element(locator_type, locator_value)
            element.clear()
            element.send_keys(text)
            
        elif action == 'wait':
            duration = command.get('duration', 1)
            if not isinstance(duration, (int, float)) or duration < 0:
                raise ValueError(f"wait action requires valid 'duration' (number >= 0), got: {duration}")
            time.sleep(duration)
            
        elif action == 'verify_element_present':
            locator_type = command.get('locator_type')
            locator_value = command.get('locator_value')
            
            if not locator_type or not locator_value:
                raise ValueError("verify_element_present requires 'locator_type' and 'locator_value' fields")
            
            # If _find_element succeeds, element is present
            self._find_element(locator_type, locator_value)
            
        elif action == 'verify_text':
            locator_type = command.get('locator_type')
            locator_value = command.get('locator_value')
            expected_text = command.get('expected_text')
            
            if not locator_type or not locator_value:
                raise ValueError("verify_text requires 'locator_type' and 'locator_value' fields")
            if not expected_text:
                raise ValueError("verify_text requires 'expected_text' field")
            
            element = self._find_element(locator_type, locator_value)
            actual_text = element.text
            if expected_text not in actual_text:
                raise AssertionError(f"Expected text '{expected_text}' not found. Got: '{actual_text}'")
            
        else:
            raise ValueError(f"Unknown action type: {action}. Supported actions: navigate, click, input, wait, verify_element_present, verify_text")
    
    def _find_element(self, locator_type: str, locator_value: str):
        """Find element using specified locator strategy"""
        by_mapping = {
            'id': By.ID,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'name': By.NAME,
            'tag': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        
        by = by_mapping.get(locator_type.lower(), By.XPATH)
        return self.wait.until(EC.presence_of_element_located((by, locator_value)))
    
    def generate_python_script(self, script_json: str) -> str:
        """Generate readable Python Selenium code from JSON"""
        commands = json.loads(script_json)
        
        python_lines = [
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC",
            "import time",
            "",
            "# Initialize browser",
            "driver = webdriver.Chrome()",
            "wait = WebDriverWait(driver, 10)",
            ""
        ]
        
        for command in commands:
            action = command.get('action')
            
            if action == 'navigate':
                python_lines.append(f"driver.get('{command.get('url')}')")
                
            elif action == 'click':
                locator = self._format_locator_python(command.get('locator_type'), command.get('locator_value'))
                python_lines.append(f"element = wait.until(EC.element_to_be_clickable({locator}))")
                python_lines.append("element.click()")
                
            elif action == 'input':
                locator = self._format_locator_python(command.get('locator_type'), command.get('locator_value'))
                text = command.get('text', '').replace("'", "\\'")
                python_lines.append(f"element = wait.until(EC.presence_of_element_located({locator}))")
                python_lines.append("element.clear()")
                python_lines.append(f"element.send_keys('{text}')")
                
            elif action == 'wait':
                duration = command.get('duration', 1)
                python_lines.append(f"time.sleep({duration})")
                
            elif action == 'verify_text':
                locator = self._format_locator_python(command.get('locator_type'), command.get('locator_value'))
                expected = command.get('expected_text', '').replace("'", "\\'")
                python_lines.append(f"element = wait.until(EC.presence_of_element_located({locator}))")
                python_lines.append(f"assert '{expected}' in element.text")
                
            elif action == 'verify_element_present':
                locator = self._format_locator_python(command.get('locator_type'), command.get('locator_value'))
                python_lines.append(f"wait.until(EC.presence_of_element_located({locator}))")
            
            python_lines.append("")
        
        python_lines.extend([
            "# Close browser",
            "driver.quit()"
        ])
        
        return "\n".join(python_lines)
    
    def _format_locator_python(self, locator_type: str, locator_value: str) -> str:
        """Format locator for Python code"""
        by_mapping = {
            'id': 'By.ID',
            'xpath': 'By.XPATH',
            'css': 'By.CSS_SELECTOR',
            'class': 'By.CLASS_NAME',
            'name': 'By.NAME',
            'tag': 'By.TAG_NAME',
            'link_text': 'By.LINK_TEXT',
            'partial_link_text': 'By.PARTIAL_LINK_TEXT'
        }
        
        by = by_mapping.get(locator_type.lower(), 'By.XPATH')
        # Escape single quotes in locator value
        escaped_value = locator_value.replace("'", "\\'")
        return f"({by}, '{escaped_value}')"


# Global executor instance
_executor = None


def get_executor() -> SeleniumExecutor:
    """Get or create global executor instance"""
    global _executor
    if _executor is None:
        _executor = SeleniumExecutor()
    return _executor

