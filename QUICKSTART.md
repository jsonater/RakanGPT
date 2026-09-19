# RakanGPT Quick Start Guide

Get up and running with RakanGPT in 5 minutes!

## What is RakanGPT?

RakanGPT is an AI-powered writing assistant that helps you:
- ✍️ Write professional essays
- 📧 Compose polished emails
- ✨ Improve your writing
- 🔍 Check grammar automatically

It uses Claude AI from Anthropic and provides both Python and C# interfaces.

## Prerequisites

You need:
1. **Python 3.8+** - Download from https://www.python.org
2. **.NET 6.0+** - Download from https://dotnet.microsoft.com
3. **Claude API Key** - Get free from https://console.anthropic.com

## Installation (5 minutes)

### On Linux/macOS:

```bash
# 1. Navigate to the RakanGPT folder
cd ~/RakanGPT

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run the setup
./setup.sh

# 4. Edit .env and add your API key
nano .env

# 5. Done! Run the app
```

### On Windows:

```bash
# 1. Navigate to the RakanGPT folder
cd C:\Users\YourUser\RakanGPT

# 2. Run the setup script
setup.bat

# 3. Edit .env in Notepad and add your API key

# 4. Done! Run the app
```

## Running RakanGPT

### Step 1: Start the Python Backend

**Linux/macOS:**
```bash
source venv/bin/activate
python backend.py
```

**Windows:**
```bash
venv\Scripts\activate.bat
python backend.py
```

You should see:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

### Step 2: Start the C# Frontend (in a new terminal)

**Linux/macOS:**
```bash
cd ~/RakanGPT
dotnet run
```

**Windows:**
```bash
cd C:\Users\YourUser\RakanGPT
dotnet run
```

You'll see a menu with options like:
```
1. Generate Essay
2. Generate Email
3. Improve Text
4. Check Grammar
5. View Available Styles
6. Exit
```

## Common Tasks

### Write an Essay

```
Menu > 1. Generate Essay
Topic: The Impact of Social Media on Society
Style: formal
Length: medium
Check grammar: y
```

### Write a Professional Email

```
Menu > 2. Generate Email
Recipient: Project Manager
Purpose: Project Status Update
Tone: professional
```

### Check Your Writing

```
Menu > 4. Check Grammar
Paste your text
Let it check for issues
```

## Troubleshooting

### "Backend is not running"
→ Make sure you ran `python backend.py` first in the terminal

### "ANTHROPIC_API_KEY not found"
→ Create `.env` file with your Claude API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE
   ```

### "Command not found: python"
→ Install Python from https://www.python.org

### "Command not found: dotnet"
→ Install .NET from https://dotnet.microsoft.com

### Module installation errors
→ Make sure you're in the virtual environment:
   ```
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate.bat # Windows
   ```

## Next Steps

1. **Read the full README.md** for all features and options
2. **Check the API endpoints** if you want to integrate with other apps
3. **Try the Python client** for programmatic access

## Using the Python Client

You can also use RakanGPT from Python:

```python
from RakanGPT import RakanGPT

api = RakanGPT()

# Generate an essay
essay = api.generate_essay("Climate Change", style="formal")
print(essay['essay'])

# Generate an email
email = api.generate_email(
    purpose="Meeting request",
    recipient="Manager",
    key_points=["Q4 planning", "Budget review"]
)
print(email['email'])
```

## Tips for Best Results

🎯 **Essay Writing:**
- Be specific with your topic
- Use "formal" style for academic work
- Choose "long" for comprehensive coverage

📧 **Email Writing:**
- List key points for better structure
- Use "professional" tone for work emails
- Keep it concise

✨ **Text Improvement:**
- Use "clarity" for better readability
- Use "grammar" for error fixing
- Use "style" for more engaging writing

## Support & Documentation

- Full documentation: See `README.md`
- API reference: See `backend.py`
- Python client: See `RakanGPT.py`

## Performance Tips

- Keep essays to "medium" length for faster generation
- Grammar checking adds ~2 seconds
- The backend needs internet access (for Claude API calls)

## Features at a Glance

| Feature | Capabilities |
|---------|--------------|
| **Essays** | Academic, any topic, 3 lengths, 5 styles |
| **Emails** | Professional, any purpose, 5 tones |
| **Text Tools** | Grammar check, improve clarity/style |
| **Export** | Save to .txt files |

## You're All Set! 🎉

Start writing amazing essays and emails! Questions? Check `README.md` for detailed information.

---
**Happy writing!** ✍️
