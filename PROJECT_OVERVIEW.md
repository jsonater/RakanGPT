# RakanGPT - Project Overview

## What is RakanGPT?

**RakanGPT** is an AI-powered writing assistant web application that uses Claude AI (Anthropic) to generate professional essays, emails, and improve text writing.

## Project Type

- **Type:** Python Flask web application
- **Framework:** Flask 3.0.0
- **Python Version:** 3.11+
- **Runtime:** Python
- **Server:** Gunicorn (production) / Flask dev server (development)

## What It Does

### Core Features
1. **Essay Generation** - Generates academic essays with multiple styles (formal, casual, creative, business, persuasive)
2. **Email Generation** - Creates professional emails with customizable tones
3. **Text Improvement** - Enhances text for clarity, grammar, style, and conciseness
4. **Grammar Checking** - Detects spelling and grammar errors with suggestions

### User Interface
- **Web Interface:** Single-page application with tabbed navigation
- **Technology:** HTML5, CSS3, JavaScript (Vanilla)
- **Responsive Design:** Works on desktop, tablet, mobile
- **Real-time Grammar Check:** Live error detection and suggestions

## Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **AI API:** Anthropic Claude (claude-3-5-sonnet-20241022)
- **Grammar Tool:** language-tool-python 2.7.1
- **Server:** Gunicorn 21.2.0
- **Dependencies Manager:** pip with requirements.txt

### Frontend
- **HTML:** Bootstrap-like custom CSS grid
- **CSS:** Responsive, modern styling with CSS variables
- **JavaScript:** Vanilla JS (no frameworks), fetch API for backend calls

### Deployment
- **Container Ready:** No Docker required
- **Environment Variables:** .env file support via python-dotenv
- **Port:** Configurable (default 5000 locally, 8000 in production)
- **Build:** No build step needed
- **Database:** None (stateless application)

## Requirements

### System Requirements
- Python 3.11 or higher
- 512 MB RAM minimum
- 100 MB disk space
- Internet connection (for Anthropic API calls)

### External Dependencies
- **Anthropic API Key:** Required (get from https://console.anthropic.com)
- **Internet Access:** Needed for Claude API calls

## File Structure

```
RakanGPT/
├── app.py                    # Main Flask application (entry point)
├── requirements.txt          # Python dependencies (pip install)
├── Procfile                  # Deployment configuration for Railway/Heroku
├── runtime.txt               # Python version specification
├── .env.example              # Environment template
├── .env                      # Runtime environment (ANTHROPIC_API_KEY required)
├── .gitignore               # Git exclusions (protects .env)
│
├── templates/
│   └── index.html           # Single-page web interface
│
├── static/
│   ├── style.css            # All styling (CSS variables, responsive)
│   └── script.js            # Frontend logic and API calls
│
└── Additional files:
    ├── backend.py           # Alternative API-only server
    ├── RakanGPT.py          # Python client library
    ├── RakanGPT.cs          # C# console application (alternative)
    └── [documentation files]
```

## How It Works

### 1. User Request Flow
```
Browser → Flask Server (app.py) → Routes to endpoint
                ↓
           Process request (get parameters)
                ↓
           Call Anthropic Claude API
                ↓
           Claude generates content
                ↓
           Optional: Grammar check with language-tool
                ↓
           Return JSON response
                ↓
           JavaScript renders in browser
```

### 2. API Endpoints
- `GET /` - Serves index.html (web interface)
- `POST /api/generate/essay` - Generate academic essay
- `POST /api/generate/email` - Generate professional email
- `POST /api/improve` - Improve existing text
- `POST /api/check-grammar` - Check grammar and spelling
- `GET /api/styles` - Get available writing styles
- `GET /api/health` - Health check for deployment

## Deployment Requirements

### Environment Variables
```
ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE    # Required
FLASK_ENV=production                       # Optional, defaults to development
FLASK_DEBUG=False                          # Optional
PORT=8000                                  # Optional, Railway will set this
```

### Startup Command
```bash
gunicorn app:app --bind 0.0.0.0:8000
```

### Port
- **Development:** 5000 (can change in app.py)
- **Production:** 8000 (or $PORT environment variable)
- **Railway Default:** 8000

## Installation & Setup

### Local Development
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run application
python app.py
# Visit http://localhost:5000
```

### Railway Deployment
```bash
# 1. Connect GitHub repository
# 2. Set environment variable: ANTHROPIC_API_KEY
# 3. Railway auto-detects Python and runs:
#    gunicorn app:app --bind 0.0.0.0:$PORT
```

### Other Platforms
- **Heroku:** Uses Procfile (included)
- **Render:** Auto-detects Flask, use gunicorn start command
- **PythonAnywhere:** Upload files, add API key, configure WSGI

## Dependencies

### Core Dependencies
```
flask==3.0.0                    # Web framework
anthropic==0.13.0              # Claude API SDK
language-tool-python==2.7.1    # Grammar checking
python-dotenv==1.0.0           # Environment variables
gunicorn==21.2.0               # Production WSGI server
requests==2.31.0               # HTTP client
```

### What They Do
- **Flask:** Routes HTTP requests, serves HTML/static files
- **Anthropic:** Calls Claude AI for text generation
- **language-tool-python:** Checks grammar and spelling
- **python-dotenv:** Loads .env file variables
- **gunicorn:** Runs Flask app in production (scales to multiple workers)
- **requests:** Makes HTTP calls (used by RakanGPT.py)

## Performance Characteristics

### Response Times
- **Essay Generation:** 10-30 seconds (depends on length)
- **Email Generation:** 5-15 seconds
- **Text Improvement:** 10-20 seconds
- **Grammar Check:** 2-5 seconds (first run slower, downloads data)

### Scalability
- **Stateless:** No session storage needed
- **Horizontal Scaling:** Can run multiple instances with load balancer
- **API Rate Limits:** Depends on Anthropic plan
- **Concurrent Users:** Limited by API quota, not application

## Error Handling

### Common Errors
1. **"ModuleNotFoundError: No module named 'anthropic'"**
   - Solution: Run `pip install -r requirements.txt`

2. **"ANTHROPIC_API_KEY not found"**
   - Solution: Create .env file with your API key

3. **"Connection refused" on port 5000**
   - Solution: Flask app not running or port in use

4. **Grammar check timeout**
   - Solution: First run downloads language data, subsequent calls faster

## Security Considerations

1. **API Key Protection:**
   - Never commit .env to Git (in .gitignore)
   - Set via environment variables on deployment platform
   - Use different keys for development/production

2. **Rate Limiting:**
   - Consider adding rate limiting for production
   - Monitor API costs
   - Implement user quotas if monetized

3. **Input Validation:**
   - Flask sanitizes all inputs
   - Language Tool prevents injection attacks
   - Anthropic API enforces usage policies

4. **HTTPS:**
   - All deployment platforms provide HTTPS
   - No self-signed certificates needed

## Monitoring & Debugging

### Logs
- Flask logs to stdout by default
- Railway/Heroku capture stdout
- Check platform logs for errors

### Health Monitoring
- GET `/api/health` returns status
- Monitor API costs in Anthropic dashboard
- Track error rates in platform logs

## Costs

### Anthropic API Costs
- Usage-based pricing (per token)
- Free trial: $5 credit
- Production: ~$0.003 per 1K tokens
- Average essay: ~100-1000 tokens per generation

### Hosting Costs
- **Railway:** $0-5+ depending on usage
- **Heroku:** $7-50+ per month (free tier deprecated)
- **Render:** Free-$20 depending on tier
- **AWS:** $3-30+ per month

## Support & Documentation

### For Deployment Issues
1. Check platform documentation
2. Verify API key is set correctly
3. Check Flask logs
4. Ensure all dependencies in requirements.txt

### For Feature Issues
- See README.md for full feature documentation
- See QUICKSTART.md for quick setup
- See DEPLOY.md for detailed deployment guides

## Summary

**RakanGPT is a Python Flask web application** that:
- ✅ Requires Python 3.11+
- ✅ Uses Flask framework (web framework)
- ✅ Depends on Anthropic API (external service)
- ✅ Has zero build step (no compilation needed)
- ✅ Uses environment variables for configuration
- ✅ Runs on any platform supporting Python
- ✅ Scales horizontally (stateless design)
- ✅ Needs Gunicorn for production

**Deployment on Railway:** Connect GitHub → Set ANTHROPIC_API_KEY → Done! 🚀
