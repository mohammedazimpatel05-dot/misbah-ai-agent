import requests
import json
import os

# Environment variable se key read karein (Hardcode mat karein)
API_KEY = os.getenv("GEMINI_API_KEY", "")
AGENT_NAME = "Misbah"

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Your name is {AGENT_NAME}. User: {prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'error' in data:
            return f"API Error ({data['error'].get('code')}): {data['error'].get('message')}"
            
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(f"=== {AGENT_NAME} AI Agent Active ===")
    print("Type 'exit' or 'quit' to end the chat.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(f"\n{AGENT_NAME}: Goodbye!")
            break
            
        if user_input.strip() == "":
            continue
            
        reply = ask_gemini(user_input)
        print(f"\n{AGENT_NAME}: {reply}\n" + "-"*40)

