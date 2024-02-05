import pytchat
import json
import os
from emoji import demojize
import requests

video_id = "qKqqangBWp4"

def main():
    chat = pytchat.create(video_id)
    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                livechat_obj = c.json()
                live_chat = json.loads(livechat_obj)

                chat_log = open("chat-log", "a")

                print(live_chat['datetime'] + " : " + live_chat['author']['name'] + " : " + live_chat['message'])
                chat_log.write(live_chat['author']['name'] + "\n    " + live_chat['message'] + "\n\n")

                chat_log.close()

                #convert emojis from into string
                #print(demojize(live_chat['datetime'] + " : " + live_chat['author']['name'] + " : " + live_chat['message']))

                if (live_chat['message'] == "!links"):
                    print("Links Triggered!")

                if ("!z" in live_chat['message']):
                    gen_prompt = live_chat['message'].replace("!z", "")
                    if (len(gen_prompt) == 0):
                        print("Z Help Requested")
                    else:
                        gen_prompt = gen_prompt.strip()
                        print(gen_prompt)
                        try:
                            requests.post(
                                'http://192.168.1.224:5000/generate',
                                json={"prompt": gen_prompt},
                                timeout=0.0000000001
                            )
                        except requests.exceptions.ReadTimeout: 
                            pass

                #get a super chat and do something!
                if(live_chat['type'] == "superChat"):
                    print("Thanks for the Super chat")
                os.system("mpv --volume=75 '../assets/bweeweep boom.mp3' > /dev/null 2>&1 /dev/null")
        os.system("mpv --loop --volume=50 '../assets/the script has failed.mp3'")
    except Exception as e:
        # TODO: Parse error logs
        print(e)
        print(f"Exception occured with the payload: {c.message}")
        os.system("mpv --loop --volume=50 '../assets/the script has failed.mp3'")
        exit()

if __name__ == "__main__":
    print("********Started YouTube Server********")
    print("======================================")
    main()
