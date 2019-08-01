
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.test import Client
from qa import models
from qa import views
from . import factories


# Create your tests here.
class QuestionCreateViewTest(TestCase):
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
        client.login(username=user.username, password='secret')

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
        question = models.Question.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, '/qa/question/{}/title/'.format(question.id))

        question = models.Question.objects.get(title='title')
        self.assertEqual(question.body, 'message')
        self.assertEqual(question.user, user)


class QuestionDetailViewTest(TestCase):
    def test_question_not_found(self):
        from django.http.response import Http404
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')
        view = views.QuestionDetailView.as_view()
        with self.assertRaises(Http404):
            view(request, pk='1', slug='dfsdf-sdf-sdf-sdf')

    def test_non_authenticated_user(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')

        question = factories.QuestionFactory.create()
        answers = [
            factories.AnswerFactory.create(question=question),
            factories.AnswerFactory.create(question=question),
        ]
        answers.reverse()
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.QuestionDetailView()
        view.setup(request, pk=question.pk, slug=question.slug)
        response = view.dispatch(request, pk=question.pk, slug=question.slug)
        context = view.get_context_data()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context['object'], question)
        self.assertEqual(context['question'], question)
        self.assertListEqual(list(context['answers']), answers)
        self.assertNotIn('create_answer_form', context)
        self.assertNotIn('accept_answer_form', context)
        self.assertNotIn('reject_answer_form', context)

    def test_authenticated_user_can_accept_answer(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')

        question = factories.QuestionFactory.create()
        answers = [
            factories.AnswerFactory.create(question=question),
            factories.AnswerFactory.create(question=question),
        ]
        answers.reverse()
        request.user = question.user
        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.QuestionDetailView()
        view.setup(request, pk=question.pk, slug=question.slug)
        response = view.dispatch(request, pk=question.pk, slug=question.slug)
        context = view.get_context_data()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context['object'], question)
        self.assertEqual(context['question'], question)
        self.assertListEqual(list(context['answers']), answers)
        self.assertTrue(context['can_accept_answer'])
        self.assertIn('create_answer_form', context)
        self.assertIn('accept_answer_form', context)
        self.assertIn('reject_answer_form', context)

    def test_authenticated_user_can_not_accept_answer(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')

        question = factories.QuestionFactory.create()
        answers = [
            factories.AnswerFactory.create(question=question),
            factories.AnswerFactory.create(question=question),
        ]
        answers.reverse()
        request.user = factories.UserFactory.create()
        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.QuestionDetailView()
        view.setup(request, pk=question.pk, slug=question.slug)
        response = view.dispatch(request, pk=question.pk, slug=question.slug)
        context = view.get_context_data()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context['object'], question)
        self.assertEqual(context['question'], question)
        self.assertListEqual(list(context['answers']), answers)
        self.assertFalse(context['can_accept_answer'])
        self.assertIn('create_answer_form', context)
        self.assertNotIn('accept_answer_form', context)
        self.assertNotIn('reject_answer_form', context)


class AcceptanceAnswerTest(TestCase):
    def test_non_authenticated_user(self):
        request_factory = RequestFactory()
        answer = factories.AnswerFactory.build()
        request = request_factory.post('/qa/question/acceptance/')
        request.user = AnonymousUser()

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.acceptance_answer(request, pk=answer.pk, slug=answer.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/?next=/qa/question/acceptance/')

    def test_answer_not_found(self):
        from django.http.response import Http404

        request_factory = RequestFactory()
        request = request_factory.post('/qa/answer/acceptance')
        request.user = AnonymousUser
        SessionMiddleware().process_request(request)
        request.session.save()

        with self.assertRaises(Http404):
            views.acceptance_answer(request, pk='1', slug='dfsdf-sdf-sdf-sdf')

    def test_http_method_not_allowed(self):
        request_factory = RequestFactory()
        answer = factories.AnswerFactory.create()
        request = request_factory.get('/qa/question/acceptance/')
        question = answer.question
        # This is user that can processes answers
        request.user = answer.question.user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.acceptance_answer(request, pk=answer.pk, slug=answer.slug)
        self.assertEqual(response.status_code, 405)

    def test_accept_answer(self):
        request_factory = RequestFactory()
        answer = factories.AnswerFactory.create(accepted=False)
        request = request_factory.post(
            '/qa/question/acceptance/', {'accepted': True})
        question = answer.question
        # This is user that can processes answers
        request.user = answer.question.user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.acceptance_answer(request, pk=answer.pk, slug=answer.slug)
        answer = models.Answer.objects.get(pk=answer.pk)

        self.assertTrue(answer.accepted)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/qa/question/{}/{}/'.format(question.pk, question.slug)
        )

    def test_reject_answer(self):
        request_factory = RequestFactory()
        answer = factories.AnswerFactory.create(accepted=True)
        request = request_factory.post(
            '/qa/question/acceptance/', {'accepted': False})
        question = answer.question
        # This is user that can processes answers
        request.user = answer.question.user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.acceptance_answer(request, pk=answer.pk, slug=answer.slug)
        answer = models.Answer.objects.get(pk=answer.pk)

        self.assertFalse(answer.accepted)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/qa/question/{}/{}/'.format(question.pk, question.slug)
        )


class ReplyAnswerTest(TestCase):
    def test_non_authenticated_user(self):
        request_factory = RequestFactory()
        question = factories.QuestionFactory.build()
        request = request_factory.post('/qa/question/reply/')
        request.user = AnonymousUser()

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.reply(request, pk=question.pk, slug=question.slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/?next=/qa/question/reply/'
        )

    def test_question_not_found(self):
        from django.http.response import Http404

        request_factory = RequestFactory()
        request = request_factory.post('/qa/answer/reply/')
        request.user = factories.UserFactory.create()
        SessionMiddleware().process_request(request)
        request.session.save()

        with self.assertRaises(Http404):
            views.reply(request, pk='1', slug='dfsdf-sdf-sdf-sdf')

    def test_http_method_not_allowed(self):
        request_factory = RequestFactory()
        question = factories.QuestionFactory.create()
        request = request_factory.get('/qa/question/reply/')
        # This is user that can processes answers
        request.user = question.user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.reply(request, pk=question.pk, slug=question.slug)
        self.assertEqual(response.status_code, 405)

    def test_reply_fail(self):
        '''
        Answer form submitted without required body field
        '''
        request_factory = RequestFactory()
        question = factories.QuestionFactory.create()
        user = question.user
        request = request_factory.post('/qa/question/reply/')
        # This is user that can processes answers
        request.user = user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.reply(request, pk=question.pk, slug=question.slug)

        self.assertEqual(response.status_code, 403)

    def test_reply_success(self):
        request_factory = RequestFactory()
        question = factories.QuestionFactory.create()
        user = question.user
        request = request_factory.post(
            '/qa/question/reply/',
            {
                'body': 'asdh ashd asdhasjdh asjdh',
                'user': user.pk,
                'question': question.pk
            }
        )
        # This is user that can processes answers
        request.user = user

        SessionMiddleware().process_request(request)
        request.session.save()

        response = views.reply(request, pk=question.pk, slug=question.slug)
        answer_count = models.Answer.objects.count()
        answer = models.Answer.objects.last()

        self.assertEqual(answer_count, 1)
        self.assertEqual(answer.body, 'asdh ashd asdhasjdh asjdh')
        self.assertEqual(answer.user, user)
        self.assertEqual(answer.question, question)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/qa/question/{}/{}/'.format(question.pk, question.slug)
        )


class QuestionListTest(TestCase):
    def test_no_questions(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')
        request.user = AnonymousUser()

        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.QuestionListView()
        view.setup(request)
        response = view.dispatch(request)
        context = view.get_context_data()
        self.assertEqual(len(context['object_list']), 0)
        self.assertEqual(response.status_code, 200)

    def test_with_questions(self):
        request_factory = RequestFactory()
        request = request_factory.get('/qa/question/')
        request.user = AnonymousUser()

        questions = [
            factories.QuestionFactory.create(title='first'),
            factories.QuestionFactory.create(title='last'),
        ]
        questions.reverse()

        SessionMiddleware().process_request(request)
        request.session.save()

        view = views.QuestionListView()
        view.setup(request)
        response = view.dispatch(request)
        context = view.get_context_data()
        self.assertEqual(len(context['object_list']), 2)
        # Veryfing list ordering
        self.assertEqual(list(context['object_list']), questions)
        self.assertEqual(response.status_code, 200)