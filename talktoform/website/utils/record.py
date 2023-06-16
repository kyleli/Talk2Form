import pyaudio
import wave
import threading
import time
from pydub import AudioSegment
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..models import AudioFile

# Global variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

frames = []
is_recording = False
paused = False

def start_recording(form_id, filename):
    if not is_recording:
    print("starting recording")
    global is_recording
    global frames
    global paused
    is_recording = True

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Start the thread for saving audio chunks
    #save_thread = threading.Thread(target=save_audio_chunks, args=(stream,))
    #save_thread.start()
    while is_recording:
        data = stream.read(CHUNK)
        if not paused:
            frames.append(data)
            print("chunking")

    # Record audio until is_recording is True
    stream.start_stream()

    # Wait for the save thread to finish and stop recording
    #save_thread.join()
    print("thread closes")
    # Clean up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("p terminates")

    # Convert frames to AudioSegment
    audio_segment = AudioSegment(
        b''.join(frames),
        frame_rate=RATE,
        sample_width=p.get_sample_size(FORMAT),
        channels=CHANNELS
    )

    # Export audio segment as an MP3 file
    path = f"audio_files/{filename}"  # The file will be saved in media/audio_files/
    temp_file = default_storage.save(path, ContentFile(audio_segment.export(format="mp3", bitrate="64k").read()))

    # Save the audio file path to the database
    audio_file = AudioFile(form_id=form_id, audio_file=temp_file)
    audio_file.save()
    frames = []

def stop_recording():
    print("stopping recording")
    global is_recording
    is_recording = False

def toggle_pause_recording():
    print("pause/unpausing")
    global paused
    paused = not paused