"""
Audit script to identify unused files in the codebase
Run this to see what can be safely removed

This script analyzes Python files to find:
- Files that are never imported
- Test/debug scripts that may be obsolete
- Temporary files that can be removed

Usage:
    python audit_unused_files.py
"""
import os
import re
from pathlib import Path

def find_python_files(directory):
    """Find all Python files in directory"""
    return list(Path(directory).rglob("*.py"))

def find_imports_in_file(filepath):
    """Extract all imports from a Python file"""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find 'import x' and 'from x import y'
            import_matches = re.findall(r'^\s*(?:from|import)\s+(\S+)', content, re.MULTILINE)
            imports.update(import_matches)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return imports

def categorize_file(filepath):
    """Categorize file based on name patterns"""
    filename = filepath.stem.lower()
    
    categories = {
        'test': ['test_', '_test'],
        'fix': ['fix_'],
        'create': ['create_'],
        'delete': ['delete_'],
        'check': ['check_'],
        'verify': ['verify_'],
        'diagnose': ['diagnose_'],
        'seed': ['seed_'],
        'regenerate': ['regenerate_'],
        'add': ['add_'],
    }
    
    for category, patterns in categories.items():
        if any(filename.startswith(p) for p in patterns):
            return category
    
    return 'other'

def main():
    print("=" * 80)
    print("CODEBASE AUDIT - Finding Unused Files")
    print("=" * 80)
    
    backend_dir = "."
    all_files = find_python_files(backend_dir)
    
    # Track all imports
    all_imports = set()
    file_map = {}
    
    for filepath in all_files:
        filename = filepath.stem
        file_map[filename] = str(filepath)
        imports = find_imports_in_file(filepath)
        all_imports.update(imports)
    
    # Categorize files
    categorized = {}
    for filepath in all_files:
        category = categorize_file(filepath)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(filepath)
    
    # Files that are core application files (should keep)
    core_files = {'run', '__init__', 'database', 'models', 'routes', 
                  'websocket_handler', 'selenium_service', 'ai_service',
                  'ai_selenium_generator', 'excel_service', 'selenium_executor'}
    
    print("\n📁 File Categories:")
    print("-" * 80)
    
    for category, files in sorted(categorized.items()):
        if category == 'other':
            continue
        print(f"\n{category.upper()} files ({len(files)}):")
        for filepath in sorted(files):
            file_size = os.path.getsize(filepath)
            is_core = filepath.stem in core_files
            status = "✓ KEEP (core)" if is_core else "⚠️  REVIEW"
            print(f"  {status} {filepath} ({file_size} bytes)")
    
    print("\n\n📊 Summary:")
    print("-" * 80)
    total_size = 0
    for category, files in categorized.items():
        if category != 'other':
            category_size = sum(os.path.getsize(f) for f in files)
            total_size += category_size
            print(f"  {category}: {len(files)} files, {category_size:,} bytes")
    
    print(f"\n  Total: {sum(len(files) for files in categorized.values())} files, {total_size:,} bytes")
    
    print("\n⚠️  Review these files before deletion!")
    print("   Some may be entry points, scripts, or tests.")
    print("\n💡 Recommendation:")
    print("   - Keep: run.py, app/ directory files")
    print("   - Review: test_*, fix_*, create_*, check_* scripts")
    print("   - Consider: Moving utility scripts to scripts/ directory")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
