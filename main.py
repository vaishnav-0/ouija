import glob
import random

import pygame

from audio import Audio
from mistral import Mistral
from transporter import Transporter

transporter = Transporter("COM3")


def pre_recording():
    pygame.mixer.music.pause()
    transporter.write(transporter.COMMANDS["spin"])
    # Stop background music


def post_recording():
    pygame.mixer.music.unpause()
    transporter.write_as_coords("CENTER")


def manual_mode():
    pygame.mixer.music.unpause()
    print("Manual mode, use Ctrl+C to exit.")
    print("Listen to user's question and type the answer.")
    while True:
        try:
            text = input("Enter text to send to board:")

            transporter.write_as_coords(text)
            transporter.write(transporter.COMMANDS["spin"])
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                break

            print(e)


def main():
    pygame.mixer.init()
    pygame.mixer.music.load("bg.mp3")
    pygame.mixer.music.play(-1)

    audio = Audio(silent_frames=2)

    audio.set_pre_recording(pre_recording)
    audio.set_post_recording(post_recording)
    audio.set_while_silent(None)

    while True:
        ghosts = glob.glob("ghosts/*.txt")
        ghost = random.choice(ghosts)

        mistral = Mistral(ghost)

        try:
            while True:
                question = audio.get_transcript()
                print("Question:", question)
                answer = mistral(question)
                print("Answer:", answer)

                transporter.write_as_coords(answer)

        except KeyboardInterrupt or Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                print(e)

        transporter.write(transporter.COMMANDS["spin"])

        print("q to quit. m for manual mode any other key to continue.")
        choice = input()

        if choice == "q":
            break
        elif choice == "m":
            return manual_mode()


if __name__ == '__main__':
    main()
