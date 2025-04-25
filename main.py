from flask import Flask, request, jsonify
import httpx

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
current_conversation = ""

with open("base_prompt", "r", encoding="utf-8") as f:
    prompt_template = f.read()


@app.route('/query', methods=['POST'])
def query():
    global current_conversation
    data = request.get_json()
    user_input = data.get("text", "")
    current_conversation += f"[USER]: {user_input}\n"
    prompt = prompt_template.replace("[conversation log]", current_conversation)

    try:
        response = httpx.post(OLLAMA_URL, timeout=100, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        content = response.json().get("response", "[say]: Sorry, I had an issue.")
    except Exception as e:
        content = f"[say]: I'm sorry, something went wrong: {e}"
    action_manager(content)
    print(content)
    current_conversation += f"[LINK]: {content}\n"
    return jsonify({"reply": content})


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
    }
    actions = ai_response.split("$$$")
    for raw_action in actions:
        try:
            action, data = raw_action.split(":", 1)
            action = action.strip().strip("[]")
            data = data.strip()
        except ValueError:
            action = raw_action.strip().strip("[]")
            data = None

        if action in action_map:
            #action_map[action](data)
            print(f"[{action}]: {data}")
        else:
            print(f"[UNKNOWN ACTION] {action} (data: {data})")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
