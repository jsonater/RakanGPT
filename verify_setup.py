#!/usr/bin/env python3
"""
RakanGPT Configuration and Test Script
Verify that everything is set up correctly
"""

import os
import sys
import json
from pathlib import Path

def check_python():
    """Check Python version"""
    print("✓ Python Check")
    print(f"  Version: {sys.version.split()[0]}")
    if sys.version_info >= (3, 8):
        print("  Status: ✅ OK (3.8 or higher required)")
        return True
    else:
        print("  Status: ❌ FAIL (Python 3.8+ required)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n✓ Dependencies Check")
    
    required = {
        'flask': 'Flask',
        'anthropic': 'Anthropic',
        'language_tool_python': 'Language Tool',
        'requests': 'Requests',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for package, name in required.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages with:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True

def check_api_key():
    """Check if API key is configured"""
    print("\n✓ API Key Check")
    
    # Check .env file
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if api_key:
        print(f"  API Key: Found ({len(api_key)} characters)")
        if api_key.startswith('sk-ant-'):
            print("  Status: ✅ OK (Valid format)")
            return True
        else:
            print("  Status: ⚠️  WARNING (Format doesn't match expected)")
            return False
    else:
        print("  API Key: NOT SET")
        print("  Status: ❌ FAIL")
        print("\n  To set your API key:")
        print("  1. Get your key from https://console.anthropic.com")
        print("  2. Create or edit .env file in this directory")
        print("  3. Add: ANTHROPIC_API_KEY=your-key-here")
        return False

def check_backend_code():
    """Check if backend.py exists and is valid"""
    print("\n✓ Backend Code Check")
    
    if os.path.exists('backend.py'):
        print("  backend.py: Found")
        try:
            with open('backend.py', 'r') as f:
                content = f.read()
                if 'Flask' in content and 'claude' in content.lower():
                    print("  Status: ✅ OK (Valid Flask/Claude setup)")
                    return True
        except Exception as e:
            print(f"  Status: ❌ FAIL ({e})")
            return False
    else:
        print("  backend.py: NOT FOUND")
        return False

def check_csharp_code():
    """Check if C# project exists"""
    print("\n✓ C# Project Check")
    
    files_needed = ['RakanGPT.cs', 'RakanGPT.csproj']
    all_found = True
    
    for filename in files_needed:
        if os.path.exists(filename):
            print(f"  {filename}: Found ✅")
        else:
            print(f"  {filename}: NOT FOUND ❌")
            all_found = False
    
    return all_found

def check_configuration():
    """Check project configuration"""
    print("\n✓ Configuration Check")
    
    configs = {
        '.env': '.env file (API credentials)',
        'requirements.txt': 'Python dependencies',
        'RakanGPT.csproj': 'C# project config',
        'backend.py': 'Python backend',
        'RakanGPT.cs': 'C# frontend'
    }
    
    all_found = True
    for file, desc in configs.items():
        if os.path.exists(file):
            print(f"  ✅ {desc}")
        else:
            print(f"  ❌ {desc} - NOT FOUND")
            all_found = False
    
    return all_found

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("  RakanGPT Configuration Checker")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python),
        ("Dependencies", check_dependencies),
        ("API Configuration", check_api_key),
        ("Backend Code", check_backend_code),
        ("C# Project", check_csharp_code),
        ("Project Files", check_configuration)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*50)
    print("  Summary")
    print("="*50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed\n")
    
    if passed == total:
        print("🎉 Everything looks good! You can run:")
        print("   1. Start backend:  python backend.py")
        print("   2. Start frontend: dotnet run")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
