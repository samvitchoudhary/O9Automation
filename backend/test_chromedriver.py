"""
ChromeDriver Diagnostic Script
Run this to diagnose ChromeDriver issues on Mac
"""
import os
import platform
import sys

print("=" * 60)
print("CHROMEDRIVER DIAGNOSTIC")
print("=" * 60)

print(f"\nPlatform: {platform.system()}")
print(f"Machine: {platform.machine()}")
print(f"Python: {sys.version}")

# Test 1: Check Selenium version
print("\n1. Checking Selenium version...")
try:
    import selenium
    print(f"   Selenium version: {selenium.__version__}")
    if hasattr(selenium, 'webdriver'):
        print("   ✓ Selenium webdriver module available")
except ImportError:
    print("   ✗ Selenium not installed")
    sys.exit(1)

# Test 2: Try Selenium Manager (built-in)
print("\n2. Testing Selenium Manager (built-in)...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("   Attempting to initialize browser with Selenium Manager...")
    driver = webdriver.Chrome(options=options)
    print("   ✓ Browser initialized successfully with Selenium Manager!")
    print(f"   ChromeDriver path: {driver.service.path}")
    driver.quit()
    print("   ✓ Browser closed successfully")
    
except Exception as e:
    print(f"   ✗ Selenium Manager failed: {e}")
    print(f"   Error type: {type(e).__name__}")

# Test 3: Check webdriver-manager (if available)
print("\n3. Testing webdriver-manager...")
try:
    from webdriver_manager.chrome import ChromeDriverManager
    
    print("   webdriver-manager is available")
    driver_path = ChromeDriverManager().install()
    print(f"   Path returned: {driver_path}")
    print(f"   Is file: {os.path.isfile(driver_path)}")
    print(f"   Is directory: {os.path.isdir(driver_path)}")
    print(f"   Exists: {os.path.exists(driver_path)}")
    
    if os.path.isdir(driver_path):
        print(f"   Directory contents:")
        for item in os.listdir(driver_path):
            full_path = os.path.join(driver_path, item)
            is_file = os.path.isfile(full_path)
            is_executable = os.access(full_path, os.X_OK) if is_file else False
            print(f"     - {item} (file: {is_file}, executable: {is_executable})")
    elif os.path.isfile(driver_path):
        is_executable = os.access(driver_path, os.X_OK)
        print(f"   File is executable: {is_executable}")
        if 'THIRD_PARTY' in driver_path:
            print(f"   ⚠ WARNING: Path points to THIRD_PARTY_NOTICES file!")
            print(f"   This is the root cause of the exec format error.")
            print(f"   Solution: Clear cache with: rm -rf ~/.wdm")
    
except ImportError:
    print("   webdriver-manager not installed (this is OK if using Selenium Manager)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Check manual ChromeDriver installation
print("\n4. Checking for manual ChromeDriver installation...")
manual_paths = [
    '/usr/local/bin/chromedriver',
    '/opt/homebrew/bin/chromedriver',
    os.path.expanduser('~/bin/chromedriver'),
]

found_manual = False
for path in manual_paths:
    if os.path.exists(path):
        is_executable = os.access(path, os.X_OK)
        print(f"   Found: {path} (executable: {is_executable})")
        found_manual = True

if not found_manual:
    print("   No manual ChromeDriver installation found")

# Test 5: Check Chrome version
print("\n5. Checking Chrome version...")
chrome_paths = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
]

chrome_found = False
for chrome_path in chrome_paths:
    if os.path.exists(chrome_path):
        try:
            result = subprocess.run(
                [chrome_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"   Chrome version: {result.stdout.strip()}")
                chrome_found = True
        except Exception as e:
            pass

if not chrome_found:
    print("   Could not detect Chrome version (Chrome may not be installed)")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("\nRecommended solution:")
print("  Use Selenium Manager (built-in) - it's the simplest and most reliable")
print("  If that fails, clear webdriver-manager cache:")
print("    rm -rf ~/.wdm")
print("\nFor manual installation:")
print("  1. Download from: https://googlechromelabs.github.io/chrome-for-testing/")
print("  2. Extract and move to /usr/local/bin/")
print("  3. Make executable: chmod +x /usr/local/bin/chromedriver")
print("  4. Remove quarantine: xattr -d com.apple.quarantine /usr/local/bin/chromedriver")
print("=" * 60)

