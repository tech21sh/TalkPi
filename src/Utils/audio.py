import pyaudio
import wave

if __name__ == '__audio__':
    pass

def playWav(wav_file):
    wf = wave.open(wav_file, "r")
    # ストリーム開始
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    remain = wf.getnframes()
    while remain > 0:
        buf = wf.readframes(min(4096, remain))
        stream.write(buf)
        remain -= 4096
    # ストリーム終了
    stream.close()
    p.terminate()
