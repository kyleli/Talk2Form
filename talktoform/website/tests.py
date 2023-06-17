from django.test import TestCase
from django.urls import reverse
from .models import Form, AudioFile, User, FormTemplate, Question, FormResponse

class CreateFormViewTest(TestCase):
    def test_create_form(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a form template
        template = FormTemplate.objects.create(title='Template 1', body='Form template body', user=user)

        # Create questions associated with the template
        question1 = Question.objects.create(template=template, question='Question 1')
        question2 = Question.objects.create(template=template, question='Question 2')

        # Log in the user (authenticate the request)
        self.client.login(username='testuser', password='testpassword')

        # Call the create_form view
        response = self.client.get(reverse('create_form', args=(template.id,)))

        # Assert that the response is successful (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Retrieve the created form
        form = Form.objects.first()

        # Check if the FormResponse objects are created for each question
        self.assertEqual(FormResponse.objects.filter(form=form).count(), 2)
