from audio import Audio


def send_to_serial(text):
    pass  # TODO: Send text to arduino via serial


def pre_recording():
    send_to_serial("SPIN")


def post_recording():
    send_to_serial("STOP")


def while_silent(speech_detected):
    pass  # TODO: Figure out what to do while silent ( design decision )


def main():
    audio = Audio(silent_frames=2)

    audio.set_pre_recording(pre_recording)
    audio.set_post_recording(post_recording)
    audio.set_while_silent(while_silent)

    while True:
        try:
            question = audio.get_transcript()
            # TODO: Send question to Mistral and get answer
            # TODO: Convert answer to letter coordinates
            coords = (10, 20)
            send_to_serial(",".join(map(str, coords)))
        except KeyboardInterrupt:
            break

    send_to_serial("CENTER")


if __name__ == '__main__':
    main()
