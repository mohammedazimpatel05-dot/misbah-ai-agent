import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AGENT_NAME = "Misbah"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Misbah AI Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 10px; background: #f4f4f9; }
        .chat-box { height: 400px; overflow-y: scroll; background: #fff; padding: 15px; border-radius: 8px; border: 1px solid #ccc; }
        .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 5px; }
        .user { background: #007bff; color: white; text-align: right; }
        .bot { background: #e9ecef; color: black; }
        .input-area { display: flex; margin-top: 10px; }
        input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 15px; background: #28a745; color: white; border: none; border-radius: 4px; margin-left: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Misbah AI Agent</h2>
    <div class="chat-box" id="chat"></div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            let input = document.getElementById("userInput");
            let chat = document.getElementById("chat");
            let text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            let response = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message: text})
            });
            let data = await response.json();
            chat.innerHTML += `<div class="msg bot"><b>Misbah:</b> ${data.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    if not GEMINI_API_KEY:
        return jsonify({"reply": "API Key missing in environment variables!"})

    # Updated to gemini-3.6-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_msg}]}]}

    try:
        res = requests.post(url, headers=headers, json=payload).json()
        if "candidates" in res:
            reply = res['candidates'][0]['content']['parts'][0]['text']
        elif "error" in res:
            reply = f"API Error: {res['error'].get('message', 'Unknown Error')}"
        else:
            reply = f"Unexpected response: {str(res)}"
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

Co-authored-by: octocat <octocat@github.com>

