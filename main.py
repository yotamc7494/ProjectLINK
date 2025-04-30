from flask import Flask, request, jsonify
import httpx
import json

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
current_conversation = ""

with open("base_prompt", "r", encoding="utf-8") as f:
    prompt_template = f.read()


#@app.route('/query', methods=['POST'])
def query(user_input):
    global current_conversation
    #data = request.get_json()
    #user_input = data.get("text", "")
    current_conversation += f"[USER]: {user_input}\n"
    prompt = prompt_template.replace("[conversation log]", current_conversation)

    try:
        response = httpx.post(OLLAMA_URL, timeout=100, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        content = response.json().get("response", "[say]: Sorry, I had an issue.")
    except Exception as e:
        content = f"[say]: I'm sorry, something went wrong: {e}"
    action_manager(content)
    current_conversation += f"[LINK]: {content}\n"
    #return jsonify({"reply": content})


def action_manager(ai_response):
    action_map = {
        "say": print,
        "open app": print,
        "search": print,
        "light": print,
        "play song": print,
        "play playlist": print,
        "next song": print,
        "prev song": print,
        "play": print,
        "pause": print,
        "request": print
    }
    try:
        actions = json.loads(ai_response)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse AI response: {e}")
        return
    for action, data in actions.items():

        if action in action_map:
            print(f"[{action}] -> {data}")

            # Uncomment this line if you have real functions later:
            # action_map[action](data)
        else:
            print(f"[UNKNOWN ACTION] {action} (data: {data})")


if __name__ == '__main__':
    query("its quite here, put us in a romantic vibe")
    #app.run(host="0.0.0.0", port=5000)
