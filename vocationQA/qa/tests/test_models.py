from faker import Faker

from django.test import TestCase

from qa import models
from . import factories


class QuestionTest(TestCase):
    def setUp(self):
        self.question = factories.PreguntaFactory.create(
            titulo='mi primera pregunta específica'
        )
    
    def test_votos_initialization(self):
        self.assertEqual(self.question.votos_positivos, 0)
        self.assertEqual(self.question.votos_negativos, 0)

    def test_str(self):
        self.assertEqual(str(self.question), 'mi primera pregunta específica')

    def test_slug(self):
        self.assertEqual(self.question.slug, 'mi-primera-pregunta-especifica')

    def test_user_authorized_accept_answer(self):
        self.assertTrue(self.question.user_can_accept_answer(self.question.autor))

    def test_user_not_authorized_accept_answer(self):
        user = factories.UserFactory.build()
        self.assertFalse(self.question.user_can_accept_answer(user))


class ThreadTest(TestCase):
    def test_str(self):
        pregunta = factories.PreguntaFactory.create(titulo='titulo')
        self.assertEqual(str(pregunta.discusion), 'titulo')


class AswersTest(TestCase):
    def test_derivated_fields(self):
        text = 'Certain even year image. I how explain lot. Someone has ..'
        slug = 'certain-even-year-image-i-how-explain-lot-someon'
        answer = factories.RespuestaFactory(cuerpo=text)

        self.assertEqual(answer.votos_positivos, 0)
        self.assertEqual(answer.votos_negativos, 0)
        self.assertEqual(answer.slug, slug)
