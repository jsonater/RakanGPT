"""
RakanGPT Python Backend - Essay and Email Writer
Uses Claude API to generate professional essays and emails with grammar checking
"""

from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import language_tool_python

app = Flask(__name__)

# Initialize Claude client
client = Anthropic()

# Initialize grammar tool
grammar_tool = language_tool_python.LanguageTool('en-US')

# Conversation history for multi-turn interactions
conversation_history = {}

# Writing style templates
STYLES = {
    "formal": "Write in a professional, academic tone with sophisticated vocabulary and structured arguments.",
    "casual": "Write in a friendly, conversational tone that's easy to read and understand.",
    "creative": "Write with vivid imagery, engaging language, and creative expression.",
    "business": "Write in a professional business tone, clear and concise with action-oriented language.",
    "persuasive": "Write using persuasive techniques, compelling arguments, and emotional appeal where appropriate."
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "RakanGPT Backend"})

@app.route('/generate/essay', methods=['POST'])
def generate_essay():
    """Generate an academic essay"""
    try:
        data = request.json
        topic = data.get('topic', '')
        style = data.get('style', 'formal')
        length = data.get('length', 'medium')  # short, medium, long
        check_grammar = data.get('check_grammar', True)
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Create style instruction
        style_instruction = STYLES.get(style, STYLES['formal'])
        
        # Determine length
        length_map = {
            'short': '300-500 words',
            'medium': '600-900 words',
            'long': '1200-1500 words'
        }
        word_count = length_map.get(length, length_map['medium'])
        
        # Create the prompt
        prompt = f"""Write an academic essay on the following topic:

Topic: {topic}

Requirements:
- Length: {word_count}
- {style_instruction}
- Include an introduction, body paragraphs, and conclusion
- Use evidence and examples to support points
- Maintain coherence and logical flow

Essay:"""
        
        # Call Claude API
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        essay = message.content[0].text
        
        # Check grammar if requested
        grammar_issues = []
        if check_grammar:
            matches = grammar_tool.check(essay)
            grammar_issues = [
                {
                    'message': match.message,
                    'offset': match.offset,
                    'length': match.length,
                    'suggestions': match.replacements[:3]
                }
                for match in matches[:10]  # Limit to 10 issues
            ]
        
        return jsonify({
            "success": True,
            "essay": essay,
            "grammar_issues": grammar_issues,
            "word_count": len(essay.split()),
            "style_used": style
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/email', methods=['POST'])
def generate_email():
    """Generate a professional email"""
    try:
        data = request.json
        recipient = data.get('recipient', 'Team')
        purpose = data.get('purpose', '')  # request, inquiry, apology, thank you, etc.
        tone = data.get('tone', 'professional')
        key_points = data.get('key_points', [])
        check_grammar = data.get('check_grammar', True)
        
        if not purpose:
            return jsonify({"error": "Purpose is required"}), 400
        
        # Create tone instruction
        tone_instruction = STYLES.get(tone, STYLES['business'])
        
        # Create key points string
        points_text = "\n".join([f"- {point}" for point in key_points]) if key_points else ""
        
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
        
        # Call Claude API
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        email = message.content[0].text
        
        # Check grammar if requested
        grammar_issues = []
        if check_grammar:
            matches = grammar_tool.check(email)
            grammar_issues = [
                {
                    'message': match.message,
                    'offset': match.offset,
                    'length': match.length,
                    'suggestions': match.replacements[:3]
                }
                for match in matches[:10]
            ]
        
        return jsonify({
            "success": True,
            "email": email,
            "grammar_issues": grammar_issues,
            "tone_used": tone
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/improve', methods=['POST'])
def improve_text():
    """Improve existing text"""
    try:
        data = request.json
        text = data.get('text', '')
        improvement_type = data.get('improvement_type', 'general')  # clarity, grammar, style, etc.
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        improvement_prompts = {
            'clarity': 'Make this text clearer and easier to understand without losing information:',
            'grammar': 'Fix all grammar and spelling errors in this text:',
            'style': 'Improve the writing style to be more engaging and professional:',
            'conciseness': 'Make this text more concise while keeping all important information:',
            'formal': 'Make this text more formal and professional:'
        }
        
        prompt = improvement_prompts.get(improvement_type, improvement_prompts['general'])
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ]
        )
        
        improved_text = message.content[0].text
        
        return jsonify({
            "success": True,
            "original": text,
            "improved": improved_text,
            "improvement_type": improvement_type
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    """Check grammar and spelling of text"""
    try:
        data = request.json
        text = data.get('text', '')
        
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

@app.route('/styles', methods=['GET'])
def get_styles():
    """Get available writing styles"""
    return jsonify({
        "styles": list(STYLES.keys()),
        "descriptions": STYLES
    })

if __name__ == '__main__':
    # Make sure ANTHROPIC_API_KEY environment variable is set
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Warning: ANTHROPIC_API_KEY environment variable not set")
    
    app.run(debug=True, host='localhost', port=5000)
