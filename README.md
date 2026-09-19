# RakanGPT - AI Essay & Email Writer

🚀 An intelligent writing assistant powered by Claude AI that generates professional essays and emails with grammar checking.

## Features

✨ **Essay Generation**
- Academic essay writing with customizable styles
- Multiple length options (short, medium, long)
- Style options: formal, casual, creative, business, persuasive
- Built-in grammar checking

📧 **Email Generation**
- Professional email composition
- Multiple tone options
- Support for key points/topics
- Grammar and spell checking

✍️ **Text Improvement**
- Enhance clarity and readability
- Style refinement
- Grammar correction
- Conciseness optimization

🔍 **Grammar Checking**
- Real-time grammar and spelling verification
- Detailed issue detection with suggestions
- Category-based error classification

## Project Structure

```
RakanGPT/
├── backend.py              # Python Flask backend with Claude API integration
├── RakanGPT.cs             # C# console frontend
├── RakanGPT.py             # Python API client library
├── RakanGPT.csproj         # C# project file
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- .NET 6.0 or higher
- Claude API key from [Anthropic](https://console.anthropic.com)

### Step 1: Set Up Python Backend

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Claude API key:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

4. Run the backend server:
```bash
python backend.py
```

The backend will start at `http://localhost:5000`

### Step 2: Set Up C# Frontend

1. Restore NuGet packages:
```bash
dotnet restore
```

2. Build the project:
```bash
dotnet build
```

3. Run the application:
```bash
dotnet run
```

## Usage

### Using the C# Console Application

Launch the application and select from the menu:

1. **Generate Essay** - Create academic essays on any topic
2. **Generate Email** - Compose professional emails
3. **Improve Text** - Enhance existing text
4. **Check Grammar** - Verify grammar and spelling
5. **View Available Styles** - See all writing style options

### Using the Python Client

```python
from RakanGPT import RakanGPT

api = RakanGPT()

# Generate an essay
essay = api.generate_essay(
    topic="The Future of AI",
    style="formal",
    length="medium"
)
print(essay['essay'])

# Generate an email
email = api.generate_email(
    purpose="Project update",
    recipient="Team Lead",
    tone="professional",
    key_points=["Completed phase 1", "On schedule for launch"]
)
print(email['email'])
```

### Using the Python Backend Directly

```bash
curl -X POST http://localhost:5000/generate/essay \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Climate Change",
    "style": "formal",
    "length": "medium",
    "check_grammar": true
  }'
```

## API Endpoints

### Essays
- `POST /generate/essay` - Generate an academic essay
  - Parameters: `topic`, `style`, `length`, `check_grammar`

### Emails
- `POST /generate/email` - Generate a professional email
  - Parameters: `recipient`, `purpose`, `tone`, `key_points`, `check_grammar`

### Text Improvement
- `POST /improve` - Improve existing text
  - Parameters: `text`, `improvement_type`

### Grammar
- `POST /check-grammar` - Check grammar and spelling
  - Parameters: `text`

### Styles
- `GET /styles` - Get available writing styles

### Health
- `GET /health` - Check backend health

## Available Writing Styles

| Style | Description |
|-------|-------------|
| **formal** | Professional, academic tone with sophisticated vocabulary |
| **casual** | Friendly, conversational, easy to read |
| **creative** | Vivid imagery, engaging, expressive |
| **business** | Clear, concise, action-oriented |
| **persuasive** | Compelling arguments, emotional appeal |

## Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` - Your Claude API key (required)
- `FLASK_ENV` - Flask environment (default: development)
- `FLASK_DEBUG` - Enable debug mode (default: True)

### Backend Settings
In `backend.py`, you can customize:
- Model version: Change `claude-3-5-sonnet-20241022` to another Claude model
- Server port: Modify the `port` parameter in `app.run()`
- Response limits: Adjust `max_tokens` values

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify `ANTHROPIC_API_KEY` is set correctly

### C# application crashes
- Make sure the Python backend is running
- Check that you have .NET 6.0 or higher installed
- Ensure Newtonsoft.Json NuGet package is installed

### Grammar checking not working
- Verify `language-tool-python` is installed
- First run may download language data (requires internet)
- Check that English language support is available

### API errors
- Check backend logs for detailed error messages
- Verify your Claude API key is valid
- Ensure you have sufficient API credits

## Example Workflows

### Academic Essay Writing
```
1. Select "Generate Essay"
2. Enter topic: "The Role of Technology in Healthcare"
3. Choose style: "formal"
4. Choose length: "long"
5. Enable grammar checking
6. Review and save the generated essay
```

### Professional Email
```
1. Select "Generate Email"
2. Enter recipient: "HR Manager"
3. Purpose: "Resignation notice"
4. Tone: "professional"
5. Add key points if needed
6. Review and save
```

### Text Polish
```
1. Select "Improve Text"
2. Paste your draft
3. Choose improvement type: "clarity"
4. Review suggestions
5. Use improved version
```

## Performance Tips

- Use the `--length` parameter to control response size and latency
- Grammar checking adds 1-2 seconds; disable if speed is critical
- The backend caches nothing; each request is independent
- Consider batching multiple requests for efficiency

## Limitations

- Maximum essay length: ~1500 words
- Maximum email length: ~500 words
- Grammar checking limited to English
- API rate limits depend on your Anthropic plan
- Creative writing modes may produce less structured output

## Future Enhancements

🔮 Planned features:
- Web UI dashboard
- Multi-language support
- Document export formats (PDF, DOCX)
- Plagiarism detection
- Custom templates
- Citation management
- Conversation history
- Batch processing

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review backend logs
3. Verify API key and configuration
4. Check Anthropic documentation: https://docs.anthropic.com

## Credits

Built with:
- **Claude AI** by Anthropic
- **Flask** for Python backend
- **.NET** for C# frontend
- **Language Tool** for grammar checking

---

**Happy Writing! 🎉**
