"""
RakanGPT - Main Python Script
Alternative to backend.py - can be run directly for testing
"""

import requests
import json
from typing import Dict, List

class RakanGPT:
    """Python API client for RakanGPT"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def generate_essay(self, topic: str, style: str = "formal", 
                      length: str = "medium", check_grammar: bool = True) -> Dict:
        """Generate an academic essay"""
        payload = {
            "topic": topic,
            "style": style,
            "length": length,
            "check_grammar": check_grammar
        }
        response = requests.post(f"{self.base_url}/generate/essay", json=payload)
        return response.json()
    
    def generate_email(self, purpose: str, recipient: str = "Team", 
                      tone: str = "business", key_points: List[str] = None,
                      check_grammar: bool = True) -> Dict:
        """Generate a professional email"""
        payload = {
            "recipient": recipient,
            "purpose": purpose,
            "tone": tone,
            "key_points": key_points or [],
            "check_grammar": check_grammar
        }
        response = requests.post(f"{self.base_url}/generate/email", json=payload)
        return response.json()
    
    def improve_text(self, text: str, improvement_type: str = "clarity") -> Dict:
        """Improve existing text"""
        payload = {
            "text": text,
            "improvement_type": improvement_type
        }
        response = requests.post(f"{self.base_url}/improve", json=payload)
        return response.json()
    
    def check_grammar(self, text: str) -> Dict:
        """Check grammar and spelling"""
        payload = {"text": text}
        response = requests.post(f"{self.base_url}/check-grammar", json=payload)
        return response.json()
    
    def get_styles(self) -> Dict:
        """Get available writing styles"""
        response = requests.get(f"{self.base_url}/styles")
        return response.json()

if __name__ == "__main__":
    # Example usage
    api = RakanGPT()
    
    print("RakanGPT - Python Client")
    print("=" * 40)
    
    # Example: Generate an essay
    print("\n📚 Generating essay...")
    essay = api.generate_essay(
        topic="The Impact of Artificial Intelligence on Modern Education",
        style="formal",
        length="medium"
    )
    
    if essay.get("success"):
        print(f"✅ Essay generated ({essay['word_count']} words)")
        print(f"\n{essay['essay'][:500]}...")
    else:
        print(f"❌ Error: {essay.get('error')}")
    
    # Example: Generate an email
    print("\n\n✉️  Generating email...")
    email = api.generate_email(
        purpose="Meeting request",
        recipient="Project Manager",
        tone="professional",
        key_points=["Discuss Q4 roadmap", "Review budget allocation"]
    )
    
    if email.get("success"):
        print(f"✅ Email generated")
        print(f"\n{email['email']}")
    else:
        print(f"❌ Error: {email.get('error')}")
