from django.test import TestCase
from qa import models
from . import factories


class QuestionTest(TestCase):
    def setUp(self):
        self.question = factories.QuestionFactory.create(
            title='mi primera pregunta específica'
        )
    
    def test_str(self):
        self.assertEqual(str(self.question), 'mi primera pregunta específica')

    def test_slug(self):
        self.assertEqual(self.question.slug, 'mi-primera-pregunta-especifica')

    def test_absolute_url(self):
        url = '/qa/question/1/mi-primera-pregunta-especifica/'
        self.assertEqual(url, self.question.get_absolute_url())
