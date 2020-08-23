import sounddevice as sdevice
import soundfile as sfile


ALARM = "loud_alarm.wav"
BREAK = "break_voice_sound.wav"


def play_alarm_sound():
    # reading alarm file
    data, sound = sfile.read(ALARM)
    sdevice.play(data, sound)


def break_suggest():
    # reading alarm file
    data, sound = sfile.read(BREAK)
    sdevice.play(data, sound)
    status = sdevice.wait()
