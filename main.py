import glob
import random

from audio import Audio
from mistral import Mistral


def send_to_serial(text):
    print(text)
    pass  # TODO: Send text to arduino via serial


def pre_recording():
    send_to_serial("SPIN")


def post_recording():
    send_to_serial("STOP")


def while_silent(speech_detected):
    pass  # TODO: Figure out what to do while silent ( design decision )


def text_to_coords(answer):
    print(answer)
    return 0, 0  # TODO: Figure out how to convert text to coordinates


def main():
    audio = Audio(silent_frames=2)

    audio.set_pre_recording(pre_recording)
    audio.set_post_recording(post_recording)
    audio.set_while_silent(while_silent)

    ghosts = glob.glob("ghosts/*.txt")
    ghost = random.choice(ghosts)

    mistral = Mistral(ghost)

    while True:
        try:
            question = audio.get_transcript()
            answer = mistral(question)
            coords = text_to_coords(answer)

            send_to_serial(",".join(map(str, coords)))
        except KeyboardInterrupt:
            break

    send_to_serial("CENTER")


if __name__ == '__main__':
    main()
