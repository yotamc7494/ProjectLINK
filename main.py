from flask import Flask, request, jsonify
import httpx

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

with open("base_prompt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get("text", "")
    prompt = prompt_template.replace("[user request]", user_input)

    try:
        response = httpx.post(OLLAMA_URL, timeout=100, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        content = response.json().get("response", "[say]:Sorry, I had an issue.")
    except Exception as e:
        content = f"[say]:I'm sorry, something went wrong: {e}"

    return jsonify({"reply": content})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
