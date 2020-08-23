import sounddevice as sdevice
import soundfile as sfile

BREAK = "break_voice_sound.wav"


def break_suggest():
    # reading alarm file
    data, sound = sfile.read(BREAK)
    sdevice.play(data, sound)