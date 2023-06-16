from django.test import TestCase
from .utils.record import record_audio
from .models import Form, AudioFile, User, FormTemplate

class AudioRecordingTestCase(TestCase):
    def test_audio_recording(self):
        user = User.objects.create(username='example_user', email='kyle@gmail.com', password='01Olaman')
        formtemplate = FormTemplate.objects.create(title='Okay', body='Body', user=user)
        form = Form.objects.create(template=formtemplate, user=user)

        # Call the record_audio function with test parameters
        record_audio(form_id=form.id, filename='9.mp3')

        # Add assertions to check if the audio file was saved correctly
        # For example, you can check if an AudioFile object was created for the form:
        self.assertEqual(AudioFile.objects.filter(form=form).count(), 1)