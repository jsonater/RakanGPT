# Project Files Overview

## Core Application Files

### Python Backend
- **backend.py** - Flask REST API backend
  - Handles essay generation
  - Handles email generation
  - Text improvement services
  - Grammar checking integration
  - Uses Claude API for AI capabilities

- **RakanGPT.py** - Python API client library
  - Simple Python interface to use RakanGPT programmatically
  - Examples and usage patterns included
  - Can be imported into other Python projects

### C# Frontend
- **RakanGPT.cs** - Console application
  - Interactive menu-driven interface
  - Communicates with Python backend
  - Handles all user interactions
  - Saves output to files

- **RakanGPT.csproj** - C# project configuration
  - .NET 6.0+ project definition
  - Specifies dependencies (Newtonsoft.Json)
  - Build and runtime configuration

## Configuration Files

- **.env.example** - Environment template
  - Shows what configuration is needed
  - Copy to .env and add your API key

- **requirements.txt** - Python dependencies
  - Flask 3.0.0
  - Anthropic SDK
  - Language Tool for grammar checking
  - Requests and python-dotenv

## Setup & Run Scripts

- **setup.sh** - Linux/macOS setup script
  - Automated environment setup
  - Installs dependencies
  - Builds C# project

- **setup.bat** - Windows setup script
  - Windows version of setup
  - Same functionality as setup.sh

## Documentation

- **README.md** - Complete documentation
  - Features and capabilities
  - Installation instructions
  - API endpoints reference
  - Troubleshooting guide
  - Usage examples

- **QUICKSTART.md** - Get started in 5 minutes
  - Quick installation
  - Running the application
  - Common tasks
  - Simple troubleshooting

- **FILES.md** - This file
  - Project structure overview

## Utilities & Examples

- **verify_setup.py** - Configuration checker
  - Verifies Python installation
  - Checks dependencies
  - Validates API key setup
  - Confirms all files are in place

- **Examples.cs** - C# usage examples
  - Example: Generate essay
  - Example: Generate email
  - Example: Check grammar
  - Shows how to integrate into other C# projects

## Project Structure

```
RakanGPT/
├── Core Application
│   ├── backend.py                 # Python Flask backend
│   ├── RakanGPT.py               # Python client library
│   ├── RakanGPT.cs               # C# console frontend
│   └── RakanGPT.csproj           # C# project file
│
├── Configuration
│   ├── .env.example              # Environment template
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # (Create this with your API key)
│
├── Setup Scripts
│   ├── setup.sh                  # Linux/macOS setup
│   └── setup.bat                 # Windows setup
│
├── Documentation
│   ├── README.md                 # Full documentation
│   ├── QUICKSTART.md             # 5-minute quick start
│   └── FILES.md                  # This file
│
└── Utilities
    ├── verify_setup.py           # Configuration checker
    └── Examples.cs               # C# usage examples
```

## How to Get Started

1. **Initial Setup** (one time)
   ```bash
   # Linux/macOS
   chmod +x setup.sh
   ./setup.sh

   # Windows
   setup.bat
   ```

2. **Add Your API Key**
   - Edit `.env` file
   - Add your Claude API key from https://console.anthropic.com

3. **Verify Everything Works**
   ```bash
   python verify_setup.py
   ```

4. **Run the Application**
   - Terminal 1: `python backend.py`
   - Terminal 2: `dotnet run`

## File Sizes & Complexity

| File | Type | Lines | Purpose |
|------|------|-------|---------|
| backend.py | Python | ~350 | Main AI backend |
| RakanGPT.cs | C# | ~400 | Console UI |
| RakanGPT.py | Python | ~100 | Client library |
| setup.sh | Bash | ~70 | Setup automation |
| Examples.cs | C# | ~120 | Usage examples |

## Dependencies

### Python Dependencies
- flask (3.0.0) - Web framework
- anthropic (0.13.0) - Claude API SDK
- language-tool-python (2.7.1) - Grammar checking
- python-dotenv (1.0.0) - Environment variables
- requests (2.31.0) - HTTP client

### .NET Dependencies
- Newtonsoft.Json (13.0.3) - JSON serialization
- .NET 6.0+ runtime

## Important Notes

1. **API Key Required**
   - Get from https://console.anthropic.com
   - Add to `.env` file before running

2. **Two Processes**
   - Backend (Python) must run first
   - Frontend (C#) connects to backend
   - Run each in separate terminal

3. **Port Configuration**
   - Backend uses http://localhost:5000
   - C# connects to this port
   - Change in backend.py if needed

4. **Features Included**
   - ✅ Essay generation with 5 writing styles
   - ✅ Email generation with multiple tones
   - ✅ Text improvement tools
   - ✅ Grammar checking
   - ✅ File saving
   - ✅ Batch processing ready

## Next Steps

1. Read `QUICKSTART.md` for quick start
2. Read `README.md` for full documentation
3. Run `python verify_setup.py` to check setup
4. Start the backend and frontend
5. Try generating your first essay!

---

**Project created**: September 2026
**Framework**: Python Flask + C# .NET
**AI Model**: Claude (Anthropic)
**Status**: Ready to use
