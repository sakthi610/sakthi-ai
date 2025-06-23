from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Safely load the Gemini API key
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCA1fPpo59Z7X3k6hWymhIJP75r0QnNkJM")
genai.configure(api_key=API_KEY)

# Start model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()
history = []

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "No message received"}), 400

    history.append(f"User: {user_message}")
    response = chat.send_message('\n'.join(history))
    bot_message = response.text
    history.append(f"Chatbot: {bot_message}")

    return jsonify({'response': bot_message})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
