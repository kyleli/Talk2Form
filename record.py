import pyaudio
import wave
import keyboard
import time

def record_audio(filename, chunk=1024, channels=1, rate=44100, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    recording = False
    key_pressed = False

    print("Press 'r' to start/pause recording, and press 'esc' to stop recording and save the file.")

    while True:
        if keyboard.is_pressed('esc'):
            break

        if keyboard.is_pressed('r') and not key_pressed:
            recording = not recording
            key_pressed = True
            print("Recording..." if recording else "Recording paused.")
            time.sleep(0.5)
        elif not keyboard.is_pressed('r'):
            key_pressed = False

        if recording:
            data = stream.read(chunk)
            frames.append(data)

    print("Recording stopped and saving...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"File saved as {filename}")

if __name__ == '__main__':
    record_audio('output.wav')