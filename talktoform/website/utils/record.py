import pyaudio
import wave
import keyboard
import time
from pydub import AudioSegment
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..models import AudioFile

def record_audio(form_id, filename, chunk=1024, channels=1, rate=44100, format=pyaudio.paInt16):
    """
    Records audio from the default microphone and saves it to the database as an MP3 file.

    Args:
    - form_id (int): The ID of the form associated with the audio file.
    - filename (str): The name of the output file.
    - chunk (int): The number of audio frames per buffer.
    - channels (int): The number of audio channels (1 for mono, 2 for stereo).
    - rate (int): The sampling rate of the audio.
    - format (int): The format of the audio data.

    Returns:
    - None
    """
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
            time.sleep(0.25)
        elif not keyboard.is_pressed('r'):
            key_pressed = False

        if recording:
            data = stream.read(chunk)
            frames.append(data)

    print("Recording stopped and saving...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert frames to AudioSegment
    audio_segment = AudioSegment(
        b''.join(frames),
        frame_rate=rate,
        sample_width=p.get_sample_size(format),
        channels=channels
    )

    # Export audio segment as an MP3 file
    path = f"audio_files/{filename}"  # The file will be saved in media/audio_files/
    temp_file = default_storage.save(path, ContentFile(audio_segment.export(format="mp3", bitrate="64k").read()))

    # Save the audio file path to the database
    audio_file = AudioFile(form_id=form_id, audio_file=temp_file)
    audio_file.save()