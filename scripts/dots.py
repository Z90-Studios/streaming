import time
import requests

def main():
    current_dot = "."

    while(True):
        if len(current_dot) < 3:
            current_dot = current_dot + "."
        else:
            current_dot = "."

        open("../state/dots", "w").close()

        print("Dots" + current_dot, end="     \r")

        intro_loading_text = open("../state/dots", "a")
        intro_loading_text.write(current_dot)
        time.sleep(1)

if __name__ == "__main__":
    main()
