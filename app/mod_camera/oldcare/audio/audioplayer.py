# -*- coding: utf-8 -*-
'''
audio player
'''

# import library


# play audio
from pygame import mixer


def play_audio(audio_name):
    try:
        mixer.init()
        mixer.music.load(audio_name)
        mixer.music.play()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        pass


if __name__ == '__main__':
    pass
