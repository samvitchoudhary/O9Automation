# O9 Automation Platform

An AI-powered test automation platform for O9 Supply Chain Planning, built for Mondelez. This system allows non-technical supply chain users to create, manage, and execute automated tests using natural language.

## Features

- **Natural Language Test Generation**: Convert plain English descriptions into automated test scripts
- **AI-Powered Script Creation**: Uses Claude API to generate Selenium automation scripts
- **Inline Editing**: Edit test steps directly and regenerate scripts
- **Real-time Execution**: Watch tests run with live browser screenshots
- **Mock O9 Environment**: Test automation without access to production O9

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLite (development) / PostgreSQL (production)
- Anthropic Claude Sonnet 4 API
- Selenium WebDriver
- WebSocket (FastAPI WebSocket)

### Frontend
- React + Vite
- Tailwind CSS
- Socket.IO Client

## Project Structure

```
O9Automation/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── websocket_handler.py
│   │   └── services/
│   │       ├── ai_service.py
│   │       ├── ai_selenium_generator.py
│   │       ├── selenium_executor.py
│   │       └── selenium_service.py
│   ├── instance/
│   │   └── test_cases.db
│   ├── requirements.txt
│   ├── .env
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TestStepExecutor.jsx
│   │   │   ├── TestCaseDetail.jsx
│   │   │   └── ...
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── mock-o9-website/
│   ├── index.html
│   ├── dashboard.html
│   ├── forecast.html
│   └── css/
├── .gitignore
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

4. **Create .env file**:
   ```bash
   # Create backend/.env file with:
   ANTHROPIC_API_KEY=your_api_key_here
   O9_MOCK_URL=http://localhost:3001
   ```

5. **Initialize database**:
   ```bash
   python run.py
   # Database will be created automatically in instance/ folder
   ```

6. **Run backend**:
   ```bash
   python run.py
   # Server will start on http://localhost:8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run frontend**:
   ```bash
   npm run dev
   # App will start on http://localhost:5173
   ```

### Mock O9 Website Setup (for testing)

1. **Navigate to mock website directory**:
   ```bash
   cd mock-o9-website
   ```

2. **Serve the website**:
   ```bash
   # Option 1: Python
   python3 -m http.server 3001
   
   # Option 2: Node.js
   npx http-server -p 3001
   ```

3. **Access at**: http://localhost:3001

## Usage

1. **Create Test Case**: Navigate to the dashboard and create a new test case
2. **Add Test Steps**: Describe each test step in natural language
3. **Generate Scripts**: Click "Generate Script" to create automation
4. **Edit Steps**: Click "Edit Step" to modify descriptions
5. **Regenerate**: Click "Regenerate Script" after editing
6. **Run Tests**: Click "Run Step" to execute automation
7. **View Results**: See execution status and screenshots in real-time

## API Endpoints

### Test Cases
- `GET /api/test-cases` - List all test cases
- `POST /api/test-cases` - Create new test case
- `GET /api/test-cases/<id>` - Get test case details
- `PUT /api/test-cases/<id>` - Update test case
- `DELETE /api/test-cases/<id>` - Delete test case

### Test Steps
- `GET /api/test-cases/<id>/steps` - Get all steps for a test case
- `POST /api/test-cases/<id>/steps` - Create new step
- `PUT /api/test-cases/<id>/steps/<step_id>` - Update step
- `DELETE /api/test-cases/<id>/steps/<step_id>` - Delete step
- `POST /api/test-steps/<id>/generate-selenium` - Generate automation script

### WebSocket Events
- `execute_step` - Execute a single test step
- `status_update` - Real-time execution status
- `progress` - Execution progress updates
- `screenshot` - Live browser screenshots
- `execution_complete` - Step execution finished

## Architecture

### Test Generation Flow
```
User Input (Natural Language)
    ↓
Claude API (Anthropic)
    ↓
JSON Commands (for execution) + Python Script (for display)
    ↓
Selenium WebDriver
    ↓
Browser Automation
    ↓
Results + Screenshots
```

### Execution Flow
```
User clicks "Run Step"
    ↓
WebSocket event triggered
    ↓
Backend initializes Chrome browser
    ↓
Executes JSON commands sequentially
    ↓
Sends real-time updates (progress, screenshots)
    ↓
Returns final status (passed/failed/error)
    ↓
Saves results to database
```

## Configuration

### Backend (.env)
```
ANTHROPIC_API_KEY=your_key_here
O9_MOCK_URL=http://localhost:3001
DATABASE_URL=sqlite:///instance/test_cases.db
```

### Frontend
- API URL: http://localhost:8000
- WebSocket: ws://localhost:8000

## Development Notes

- **ChromeDriver**: Managed automatically by Selenium Manager (4.6+)
- **Database**: SQLite for development, PostgreSQL for production
- **AI Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Browser**: Headless Chrome for automation
- **JSON-Only Execution**: System only executes JSON commands, never Python scripts

## Known Issues

- ChromeDriver may require manual installation on some systems
- WebSocket connections need CORS configuration for different origins
- Database migrations not automated (manual schema updates needed)

## Future Enhancements

- [ ] Production deployment configuration
- [ ] PostgreSQL migration
- [ ] User authentication and multi-tenancy
- [ ] Test scheduling and CI/CD integration
- [ ] Advanced reporting and analytics
- [ ] Element locator recorder tool
- [ ] Actual O9 integration (replacing mock)

## License

Proprietary - Mondelez International

## Contact

For questions or support, contact the development team.

---

**Note**: This is an internal tool for Mondelez. Do not share API keys or sensitive information.
