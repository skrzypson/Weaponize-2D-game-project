from pydub import AudioSegment
from pydub.playback import play


def speed_change(sound, speed=1.0):
    """ Manually override the frame_rate - instructs on how many
    samples to play per second.

    Args:
        sound: AudioSegment
        speed: float

    Returns:
        AudioSegment
    """
    sound_with_altered_frame_rate = sound._spawn(
        sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        }
    )

    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


if __name__ == "__main__":

    s = AudioSegment.from_wav('./sounds/lasershot.wav')
    s = s[len(s)*0.018:len(s)*0.05588]

    s = speed_change(s, 0.4)
    s = s + 15

    # sssss = sum(5*[s])
    play(s)
    s.export('./sounds/fasterlasershot.wav', format='wav')

    # print(len(s))
    # while True:
    #     play(s)
        # play(speed_change(s, 100))
