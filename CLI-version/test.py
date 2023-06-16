import pyaudio
import wave
import keyboard
import time
from pydub import AudioSegment
from django.core.files.base import ContentFile
from ..models import AudioFile, Form

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

    while True:
        if recording:
            data = stream.read(chunk)
            frames.append(data)

        if not recording:
            break

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

    # Export audio segment as MP3 byte string
    audio_byte_string = audio_segment.export(format="mp3", bitrate="64k").getvalue()

    # Get the associated form
    form = Form.objects.get(pk=form_id)

    # Create a new AudioFile instance
    audio_file = AudioFile(form=form, audio_file=ContentFile(audio_byte_string, filename))
    audio_file.save()




