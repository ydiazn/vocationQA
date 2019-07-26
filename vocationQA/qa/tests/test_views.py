
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.test import Client
from qa import models
from qa import views
from . import factories


# Create your tests here.
class QuestionCreateTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_non_authenticated_user(self):
        request = self.request_factory.get('/qa/question/add/')
        request.user = AnonymousUser()

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.QuestionCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/?next=/qa/question/add/')

    def test_authenticated_user(self):
        client = Client()
        user = factories.UserFactory.create()
        client.login(username='jhon', password='secret')

        response = client.get('/qa/question/add/')
        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.context['form'].initial,
            {'user': user.id}
        )

    def test_create_question(self):
        user = factories.UserFactory.create()

        request = self.request_factory.post(
            '/qa/question/add',
            {
                'title': 'title',
                'body': 'message',
                'user': user.id
            }
        )
        request.user = user
        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.QuestionCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/qa/question/1/title/')

        question = models.Question.objects.get(title='title')
        self.assertEqual(question.body, 'message')
        self.assertEqual(question.user, user)
