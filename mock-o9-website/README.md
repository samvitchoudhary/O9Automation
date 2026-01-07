# Mock O9 Website for Selenium Testing

## Overview

This is a simple mock O9 website that mimics the O9 interface so you can test your Selenium automation scripts without access to the real O9 platform. This allows you to verify that the "Run Step" functionality works correctly.

## Setup

### Option A: Using Python (Recommended)

```bash
cd mock-o9-website
python -m http.server 3001
```

### Option B: Using Node.js http-server

```bash
npm install -g http-server
cd mock-o9-website
http-server -p 3001
```

### Option C: Using VS Code Live Server

- Install "Live Server" extension
- Right-click `index.html`
- Select "Open with Live Server"
- Configure port to 3001 if needed

## Access the Site

Once the server is running, access the site at:

**http://localhost:3001**

## Test Credentials

- **Username**: `testuser` (or any username)
- **Password**: `password123` (or any password)

The login accepts any non-empty username and password for testing purposes.

## Pages Available

- **Login**: `http://localhost:3001/index.html`
- **Dashboard**: `http://localhost:3001/dashboard.html`
- **Forecast**: `http://localhost:3001/forecast.html`
- **BOM Setup**: `http://localhost:3001/bom-setup.html`

## Navigation Structure

The mock site includes a navigation structure that matches common O9 patterns:

- **Demand Analyst**
  - System Forecast
    - Generate Forecast
      - Details (forecast.html)
- **Supply Master Planning**
  - Manage Network
    - Manufacturing Network
      - BOM Setup (bom-setup.html)
- **Inventory Planning**
  - Analysis
  - Reports

## Features

### Login Page
- Username field (id="username")
- Password field (id="password")
- Login button (id="login-button")
- Redirects to dashboard on successful login

### Dashboard
- Welcome message
- Navigation menu with expandable submenus
- Dashboard widgets showing mock metrics

### Forecast Page
- Scope filters (Forecast Iteration, Channel, Region, Version)
- Review Widget with chart placeholder
- Gap Widget with data table
- Apply Filters button

### BOM Setup Page
- Global filters (Version, Item)
- Produced Items table
- Consumed Items section (updates when clicking "View Consumed" links)
- Load button

## Testing Your Selenium Scripts

Your generated Selenium scripts should be able to:

1. Navigate to `http://localhost:3001`
2. Enter credentials in the login form
3. Click the login button
4. Verify redirect to dashboard
5. Navigate through the menu structure
6. Interact with filters and widgets
7. Verify page elements and data

## Example Selenium Script

When generating Selenium scripts for "Login to O9", the AI should generate something like:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Navigate to O9 (using mock for testing)
driver.get('http://localhost:3001')

# Enter username
username_field = driver.find_element(By.ID, 'username')
username_field.send_keys('testuser')

# Enter password
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys('password123')

# Click login button
login_button = driver.find_element(By.ID, 'login-button')
login_button.click()

# Wait for dashboard to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'main-content'))
)

# Verify login successful
assert 'dashboard' in driver.current_url

driver.quit()
```

## Modifying for Your Tests

To match your specific test cases, you can:

- Add more pages by creating new HTML files
- Add more form elements with specific IDs
- Add more widgets and data tables
- Customize the navigation structure
- Add more realistic data
- Add success/error messages
- Add loading spinners
- Add search functionality
- Add export buttons

## Integration with Your App

Update your Selenium script generation to use `http://localhost:3001` as the base URL for testing. The mock site provides all the essential UI elements needed to test your automation scripts.

## Notes

- The site uses `sessionStorage` to maintain login state
- All pages check authentication and redirect to login if not authenticated
- The navigation menu supports expandable submenus
- All form elements have proper IDs for Selenium targeting
- The site is responsive and works in different screen sizes

