import sounddevice as sdevice
import soundfile as sfile

ALARM = "loud_alarm.wav"


def play_alarm_sound():
    # reading alarm file
    data, sound = sfile.read(ALARM)
    sdevice.play(data, sound)
