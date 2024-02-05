import time
import json
import requests

def get_dots(current_dot):
    if len(current_dot) < 3:
        current_dot = current_dot + "."
    else:
        current_dot = "."

    open("../state/dots", "w").close()

    print("Dots" + current_dot, end="     \r")

def get_response(prompt):
    response = ""

    s = requests.Session()

    data = {
        'model': 'mistral',
        'prompt': prompt,
        'stream': True,
    }

    with s.post('http://192.168.1.224:11434/api/generate', json=data, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                response_part = json.loads(line.decode('UTF-8'))
                print(response_part['response'])

                token = response_part['response']
                response = response + token

    return response

def main():
    max_len = 119

    current_str = "Figuring things out"
    current_dot = ".."

    prompt = "Generate a random loading screen message that is short. Use quirky references that are jovial in nature, avoid copyright infringement but make pop culture references, especially meme references."

    response = get_response(prompt)
    print(response)

    while(True):
        open("../state/intro-loading-text", "w").close()
        intro_loading_text = open("../state/intro-loading-text", "a")
        intro_loading_text.write(current_str + current_dot)
        time.sleep(1)

if __name__ == "__main__":
    print("Intro Loader...")
    main()
