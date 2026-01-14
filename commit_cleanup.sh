#!/bin/bash

# Script to commit cleaned codebase to GitHub
# Run this script from the repository root

set -e  # Exit on error

echo "=========================================="
echo "Committing Cleaned Codebase to GitHub"
echo "=========================================="
echo ""

# Navigate to repository root
cd "$(dirname "$0")"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check current status
echo "📊 Current git status:"
git status --short
echo ""

# Verify .gitignore is working
echo "🔍 Checking for files that should be ignored..."
if [ -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env exists (should be ignored by .gitignore)"
fi
if [ -f "backend/test_cases.db" ]; then
    echo "⚠️  Warning: backend/test_cases.db exists (should be ignored by .gitignore)"
fi
echo ""

# Check what will be added (respecting .gitignore)
echo "📦 Files that will be staged (respecting .gitignore):"
git add --dry-run . 2>&1 | grep -E "^add|^create" | head -20
echo ""

# Ask for confirmation
read -p "Continue with staging all changes? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Commit cancelled."
    exit 0
fi

# Stage all changes (respects .gitignore)
echo ""
echo "📦 Staging all changes..."
git add .

# Verify what's staged
echo ""
echo "✅ Staged files:"
git status --short
echo ""

# Count changes
MODIFIED=$(git diff --cached --name-only | wc -l | tr -d ' ')
echo "📊 Total files staged: $MODIFIED"
echo ""

# Ask for final confirmation
read -p "Create commit with these changes? (yes/no): " confirm_commit

if [ "$confirm_commit" != "yes" ]; then
    echo "❌ Commit cancelled. Files are staged but not committed."
    echo "   Run 'git reset' to unstage if needed."
    exit 0
fi

# Create commit
echo ""
echo "💾 Creating commit..."
git commit -m "refactor: Complete codebase cleanup and documentation

Major Changes:
==============

Code Organization:
- Split websocket_handler.py (746 lines) into modular components
  - app/websocket/connection.py: Connection lifecycle management
  - app/websocket/test_execution.py: Test execution logic
  - app/websocket/test_generation.py: Test case generation
- Removed duplicate code and functions
- Improved code organization and maintainability

Documentation:
- Added comprehensive docstrings to all functions
- Added file headers with module descriptions
- Created backend/app/websocket/README.md with module documentation
- Created CLEANUP_SUMMARY.md documenting all changes
- Created CLEANUP_CHECKLIST.md for future cleanup tasks

Code Quality:
- Improved error handling across all modules
- Standardized logging patterns
- Removed commented-out code
- Fixed inconsistent naming

UI Improvements:
- Added Mondelez branding (logo, colors, header, footer)
- Made logo clickable (returns to dashboard)
- Implemented conditional navigation (+ button on dashboard)
- Professional header and footer design
- Added ViewScriptModal component for JSON command viewing

Utility Scripts:
- Added audit_unused_files.py to identify unused files
- Added find_large_files.py to identify files needing refactoring

Files Added:
- backend/app/websocket/ module (4 files)
- backend/audit_unused_files.py
- backend/find_large_files.py
- frontend/src/components/Header.jsx, Header.css
- frontend/src/components/Footer.jsx, Footer.css
- frontend/src/components/ViewScriptModal.jsx, ViewScriptModal.css
- frontend/src/App.css
- Documentation files (CLEANUP_*.md)

Files Modified:
- backend/app/websocket_handler.py (now compatibility shim)
- backend/app/routes.py (updated imports)
- frontend/src/App.jsx (added Header/Footer)
- frontend/src/components/TestStepExecutor.jsx (ViewScriptModal integration)
- frontend/src/index.css (Mondelez colors)
- frontend/tailwind.config.js (Mondelez theme)

Breaking Changes:
- None - All existing functionality preserved via backward compatibility

Tested:
- ✅ Backend runs without errors
- ✅ Frontend runs without errors
- ✅ All features functional
- ✅ WebSocket connections stable
- ✅ Imports work correctly (backward compatible)"

# Check if commit was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Commit created successfully!"
    echo ""
    
    # Show commit summary
    echo "📝 Commit details:"
    git log -1 --stat --oneline
    echo ""
    
    # Ask about pushing
    read -p "Push to GitHub? (yes/no): " confirm_push
    
    if [ "$confirm_push" == "yes" ]; then
        echo ""
        echo "🚀 Pushing to GitHub..."
        git push origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "=========================================="
            echo "✅ Successfully pushed to GitHub!"
            echo "=========================================="
            echo ""
            echo "View your changes at:"
            echo "https://github.com/samvitchoudhary/O9Automation"
            echo ""
        else
            echo ""
            echo "❌ Push failed. Please resolve any errors above."
            echo "Common issues:"
            echo "  - Need to pull first: git pull origin main"
            echo "  - Authentication: Check SSH keys or use HTTPS"
            echo "  - Remote URL: git remote -v"
        fi
    else
        echo ""
        echo "📦 Commit created but not pushed."
        echo "   Push manually with: git push origin main"
    fi
else
    echo ""
    echo "❌ Commit failed. Please check the error above."
    exit 1
fi
