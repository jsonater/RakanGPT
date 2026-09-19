"""
RakanGPT Web Application
Flask app with HTML/CSS/JS frontend for browser-based access
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from anthropic import Anthropic
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

AI_IDENTITY = (
    "You are RakanGPT, a friendly AI English writing assistant. "
    "Your name is RakanGPT. You help users with essays, emails, grammar, and general writing. "
    "Always introduce yourself as RakanGPT and answer in a helpful, natural, English-focused way."
)

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:3b')

# Initialize clients
# Prefer free local Ollama model when available; fallback to Anthropic if API key is configured.
default_headers = {}
if os.getenv('ANTHROPIC_WORKSPACE_ID'):
    default_headers['anthropic-workspace-id'] = os.getenv('ANTHROPIC_WORKSPACE_ID')

anthropic_client = None
if os.getenv('ANTHROPIC_API_KEY'):
    anthropic_client = Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        default_headers=default_headers
    )


def generate_with_model(prompt: str, max_tokens: int = 1000):
    """Generate text using the free local Ollama endpoint when available, else Anthropic."""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "system": AI_IDENTITY,
                "stream": False,
                "options": {"num_predict": max_tokens}
            },
            timeout=180
        )
        if response.status_code == 200:
            payload = response.json()
            return payload.get('response', '').strip()
        raise RuntimeError(f"Ollama request failed: {response.status_code} {response.text[:200]}")
    except Exception:
        if anthropic_client is None:
            raise RuntimeError(
                'No AI backend is available. Please either install Ollama and pull a model, or add an Anthropic API key.'
            )

        message = anthropic_client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=max_tokens,
            system=AI_IDENTITY,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return message.content[0].text


# Grammar tool removed - causing compatibility issues
# Can be added back later if needed

# Writing style templates
STYLES = {
    "formal": "Write in a professional, academic tone with sophisticated vocabulary and structured arguments.",
    "casual": "Write in a friendly, conversational tone that's easy to read and understand.",
    "creative": "Write with vivid imagery, engaging language, and creative expression.",
    "business": "Write in a professional business tone, clear and concise with action-oriented language.",
    "persuasive": "Write using persuasive techniques, compelling arguments, and emotional appeal where appropriate."
}

# ================== API ENDPOINTS ==================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "RakanGPT"})

# ================== CHAT ENDPOINT ==================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with Claude AI"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        reply = generate_with_model(message, max_tokens=1000)
        
        return jsonify({
            "success": True,
            "reply": reply
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/styles', methods=['GET'])
def get_styles():
    """Get available writing styles"""
    return jsonify({
        "styles": list(STYLES.keys()),
        "descriptions": STYLES
    })

# ================== ESSAY ENDPOINTS ==================

@app.route('/api/generate/essay', methods=['POST'])
def generate_essay():
    """Generate an academic essay"""
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        style = data.get('style', 'formal')
        length = data.get('length', 'medium')
        check_grammar = data.get('check_grammar', True)
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        style_instruction = STYLES.get(style, STYLES['formal'])
        
        length_map = {
            'short': '300-500 words',
            'medium': '600-900 words',
            'long': '1200-1500 words'
        }
        word_count = length_map.get(length, length_map['medium'])
        
        prompt = f"""Write an academic essay on the following topic:

Topic: {topic}

Requirements:
- Length: {word_count}
- {style_instruction}
- Include an introduction, body paragraphs, and conclusion
- Use evidence and examples to support points
- Maintain coherence and logical flow

Essay:"""
        
        essay = generate_with_model(prompt, max_tokens=2000)
        
        return jsonify({
            "success": True,
            "essay": essay,
            "grammar_issues": [],
            "word_count": len(essay.split()),
            "style_used": style
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== EMAIL ENDPOINTS ==================

@app.route('/api/generate/email', methods=['POST'])
def generate_email():
    """Generate a professional email"""
    try:
        data = request.json
        recipient = data.get('recipient', 'Team').strip()
        purpose = data.get('purpose', '').strip()
        tone = data.get('tone', 'professional')
        key_points = data.get('key_points', [])
        check_grammar = data.get('check_grammar', True)
        
        if not purpose:
            return jsonify({"error": "Purpose is required"}), 400
        
        tone_instruction = STYLES.get(tone, STYLES['business'])
        
        points_text = "\n".join([f"- {point}" for point in key_points if point.strip()]) if key_points else ""
        
        prompt = f"""Write a professional email with the following details:

Recipient: {recipient}
Purpose: {purpose}
Tone: {tone_instruction}

{f'Key points to include:' + chr(10) + points_text if points_text else ''}

Requirements:
- Include appropriate greeting and closing
- Keep it concise but professional
- Structure with clear subject line, body, and sign-off
- Match the specified tone

Email:"""
        
        email = generate_with_model(prompt, max_tokens=1000)
        
        return jsonify({
            "success": True,
            "email": email,
            "grammar_issues": [],
            "tone_used": tone
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== TEXT IMPROVEMENT ENDPOINTS ==================

@app.route('/api/improve', methods=['POST'])
def improve_text():
    """Improve existing text"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        improvement_type = data.get('improvement_type', 'general')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        improvement_prompts = {
            'clarity': 'Make this text clearer and easier to understand without losing information:',
            'grammar': 'Fix all grammar and spelling errors in this text:',
            'style': 'Improve the writing style to be more engaging and professional:',
            'conciseness': 'Make this text more concise while keeping all important information:',
            'formal': 'Make this text more formal and professional:'
        }
        
        prompt = improvement_prompts.get(improvement_type, 'Improve this text:')
        
        improved_text = generate_with_model(f"{prompt}\n\n{text}", max_tokens=2000)
        
        return jsonify({
            "success": True,
            "original": text,
            "improved": improved_text,
            "improvement_type": improvement_type
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== GRAMMAR CHECK ENDPOINTS ==================

@app.route('/api/check-grammar', methods=['POST'])
def check_grammar():
    """Check grammar and spelling of text"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        matches = grammar_tool.check(text)
        issues = [
            {
                'message': match.message,
                'offset': match.offset,
                'length': match.length,
                'suggestions': match.replacements[:5],
                'category': match.category
            }
            for match in matches
        ]
        
        return jsonify({
            "success": True,
            "text": text,
            "issues_found": len(issues),
            "issues": issues
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== STATIC FILES ==================

@app.route('/favicon.ico')
def favicon():
    """Favicon route"""
    return jsonify({}), 204

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("✅ Using free local Ollama model (no paid API required)")
        print("If Ollama is not running, start it with: ollama serve")
    
    # Railway and other platforms set PORT env variable
    port = int(os.getenv('PORT', 5000))
    is_production = os.getenv('FLASK_ENV') == 'production' or os.getenv('RAILWAY_ENVIRONMENT_NAME') is not None
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=not is_production and os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
