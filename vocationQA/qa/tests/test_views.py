from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from qa import models
from qa import views
from . import factories


# Create your tests here.

class QuestionListTest(TestCase):
    def test_no_questions(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/')
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


class QuestionDetailTest(TestCase):

    def test_question_detail(self):
        question = factories.PreguntaFactory.create()

        response = self.client.get(
            '/qa/question/{}/{}/'.format(question.pk, question.slug)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], question.discusion)


class QuestionCreateFormTest(TestCase):
    def test_anonymous_user_test(self):
        response = self.client.get('/qa/question/add')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '{}?next=/qa/question/add'.format(settings.LOGIN_URL)
        )

    def test_authenticated_user_test(self):
        user = factories.UserFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.get('/qa/question/add')
        self.assertEqual(response.status_code, 200)


class QuestionCreateTest(TestCase):
    def test_anonymous_user(self):
        response = self.client.post('/qa/question/add', {
            'titulo': 'sdasdad asdjk aksjd',
            'cuerpo': 'asldj askdj as lkasjd '
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '{}?next=/qa/question/add'.format(settings.LOGIN_URL)
        )
        self.assertEqual(models.Pregunta.objects.count(), 0)

    def test_no_title(self):
        user = factories.UserFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post('/qa/question/add', {
            'body': 'asldj askdj as lkasjd '
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Pregunta.objects.count(), 0)

    def test_no_body(self):
        user = factories.UserFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post('/qa/question/add', {
            'titulo': 'asldj askdj as lkasjd '
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Pregunta.objects.count(), 0)

    def test_success_creation(self):
        user = factories.UserFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post('/qa/question/add', {
            'titulo': 'sdasdad asdjk aksjd',
            'cuerpo': 'asldj askdj as lkasjd'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,'/')
        self.assertEqual(models.Pregunta.objects.count(), 1)
        pregunta = models.Pregunta.objects.first()
        self.assertEqual(pregunta.titulo, 'sdasdad asdjk aksjd')
        self.assertEqual(pregunta.cuerpo, 'asldj askdj as lkasjd')
        self.assertEqual(pregunta.autor, user)


class AnswerCreateTest(TestCase):
    def test_anonymous_user(self):
        response = self.client.post('/qa/question/1/ejemplo/', {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '{}?next=/qa/question/1/ejemplo/'.format(settings.LOGIN_URL)
        )
        self.assertEqual(models.Respuesta.objects.count(), 0)

    def test_no_body(self):
        user = factories.UserFactory.create()
        question = factories.PreguntaFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post(
            '/qa/question/{}/{}/'.format(question.discusion.id, question.slug), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Respuesta.objects.count(), 0)

    def test_no_discusion(self):
        user = factories.UserFactory.create()
        question = factories.PreguntaFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post(
            '/qa/question/{}/{}/'.format(question.discusion.id, question.slug),
            {
                'cuerpo': 'cuerpo'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Respuesta.objects.count(), 0)

    def test_no_author(self):
        user = factories.UserFactory.create()
        question = factories.PreguntaFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post(
            '/qa/question/{}/{}/'.format(question.discusion.id, question.slug),
            {
                'cuerpo': 'cuerpo',
                'discusion': question.discusion.id
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Respuesta.objects.count(), 0)

    def test_success_creation(self):
        user = factories.UserFactory.create()
        question = factories.PreguntaFactory.create()
        self.client.login(username=user.username, password='secret')
        response = self.client.post(
            '/qa/question/{}/{}/'.format(question.discusion.id, question.slug),
            {
                'cuerpo': 'cuerpo',
                'discusion': question.discusion.id,
                'autor': user.id
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Respuesta.objects.count(), 1)
