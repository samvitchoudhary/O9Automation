"""
Find large files that need refactoring

This script identifies files that exceed recommended line counts:
- 300-500 lines: Consider splitting
- 500+ lines: Definitely should split

Usage:
    python find_large_files.py
"""
import os
from pathlib import Path

def count_lines(filepath):
    """Count lines in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def count_functions(filepath):
    """Count function definitions in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count def statements
            return len([line for line in content.split('\n') if line.strip().startswith('def ')])
    except:
        return 0

def count_classes(filepath):
    """Count class definitions in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count class statements
            return len([line for line in content.split('\n') if line.strip().startswith('class ')])
    except:
        return 0

def main():
    print("=" * 80)
    print("FINDING LARGE FILES (>300 lines)")
    print("=" * 80)
    
    # Find Python files
    files = list(Path('.').rglob('*.py'))
    
    # Exclude venv and __pycache__
    files = [f for f in files if 'venv' not in str(f) and '__pycache__' not in str(f)]
    
    large_files = []
    for filepath in files:
        lines = count_lines(filepath)
        if lines > 300:
            functions = count_functions(filepath)
            classes = count_classes(filepath)
            large_files.append((str(filepath), lines, functions, classes))
    
    # Sort by size
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print("\n📊 Files that should be refactored:")
    print("-" * 80)
    print(f"{'File':<50} {'Lines':<8} {'Functions':<10} {'Classes':<8}")
    print("-" * 80)
    
    for filepath, lines, functions, classes in large_files:
        status = "🔴 CRITICAL" if lines > 500 else "🟡 REVIEW"
        print(f"{status} {filepath:<45} {lines:<8} {functions:<10} {classes:<8}")
    
    print("\n💡 Refactoring Guidelines:")
    print("  • 300-500 lines: Consider splitting into smaller modules")
    print("  • 500+ lines: Definitely should split")
    print("  • Each file should have ONE clear responsibility")
    print("  • Aim for 100-300 lines per file")
    print("\n📋 Suggested Refactoring:")
    print("-" * 80)
    
    for filepath, lines, functions, classes in large_files:
        if lines > 500:
            print(f"\n  {filepath}:")
            print(f"    - {lines} lines, {functions} functions, {classes} classes")
            print(f"    - Consider splitting into:")
            print(f"      • Connection handling")
            print(f"      • Business logic")
            print(f"      • Error handling")
            print(f"      • Utility functions")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
