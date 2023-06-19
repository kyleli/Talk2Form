from pydub import AudioSegment
import io

class BytesIOWithFilename(io.BytesIO):
    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

def convert_audio_format(audio_bytes, source_format, target_format):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=source_format, codec='aac')
    converted_audio = io.BytesIO()
    audio.export(converted_audio, format=target_format)
    converted_audio.seek(0)
    return converted_audio.read()

def mp4_to_webm(audio_bytes):
    source_format = 'mp4'
    target_format = 'webm'
    return convert_audio_format(audio_bytes, source_format, target_format)
