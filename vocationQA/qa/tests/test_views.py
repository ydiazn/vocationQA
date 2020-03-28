
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.test import Client
from qa import models
from qa import views
from . import factories


# Create your tests here.

class QuestionListTest(TestCase):
    def test_no_questions(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')
        request.user = AnonymousUser()

        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.IndexView()
        view.setup(request)
        response = view.dispatch(request)
        context = view.get_context_data()
        self.assertEqual(len(context['object_list']), 0)
        self.assertEqual(response.status_code, 200)

    def test_with_questions(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/')
        request.user = AnonymousUser()

        questions = [
            factories.PreguntaFactory.create(titulo='first'),
            factories.PreguntaFactory.create(titulo='second'),
            factories.PreguntaFactory.create(titulo='last'),
        ]
        discusions = [question.discusion for question in questions]
        discusions.reverse()

        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.IndexView()
        view.setup(request)
        response = view.dispatch(request)
        context = view.get_context_data()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context['object_list']), 3)
        # Veryfing list ordering
        self.assertEqual(list(context['object_list']), discusions)
