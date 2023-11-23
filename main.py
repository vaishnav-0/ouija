import glob
import random
from time import sleep

import pygame
import serial

from audio import Audio
from constants import LETTER_MAP
from mistral import Mistral

ser: serial.Serial | None = None


def send_to_serial(text):
    if ser is None:
        return

    print("To arduino:", text)

    ser.write(text.encode())
    ser.flush()


def text_to_coords(answer):
    # Remove any characters other than alphabets abd numbers
    answer = "".join([c for c in answer if c.isalnum()])
    answer = answer.upper()

    if answer in LETTER_MAP:
        return [LETTER_MAP[answer]]

    return [LETTER_MAP[c] for c in answer]


def pre_recording():
    pygame.mixer.music.pause()
    send_to_serial("SPIN")
    # Stop background music


def post_recording():
    pygame.mixer.music.unpause()
    send_to_serial("STOP")
    # play background music


def main():
    global ser

    pygame.mixer.init()
    pygame.mixer.music.load("bg.mp3")
    pygame.mixer.music.play(-1)

    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
    except serial.SerialException:
        print("Serial port not found. Skipping serial communication.")
        print("Please connect the Arduino and restart the program.")

    audio = Audio(silent_frames=2)

    audio.set_pre_recording(pre_recording)
    audio.set_post_recording(post_recording)
    audio.set_while_silent(None)

    while True:
        ghosts = glob.glob("ghosts/*.txt")
        ghost = random.choice(ghosts)

        mistral = Mistral(ghost)

        while True:
            try:
                question = audio.get_transcript()
                print("Question:", question)
                answer = mistral(question)
                print("Answer:", answer)
                coords = text_to_coords(answer)

                for coord in coords:
                    send_to_serial(",".join(map(str, coord)))
                    sleep(10)

            except KeyboardInterrupt:
                break

        send_to_serial("CENTER")

        print("Press Ctrl+C again to exit. Press any other key to continue.")
        try:
            input()
        except KeyboardInterrupt or UnicodeError:
            break


if __name__ == '__main__':
    main()