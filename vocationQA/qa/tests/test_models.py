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
        id = self.question.id
        url = '/qa/question/{}/mi-primera-pregunta-especifica/'.format(id)
        self.assertEqual(url, self.question.get_absolute_url())

    def test_user_authorized_accept_answer(self):
        self.assertTrue(self.question.user_can_accept_answer(self.question.user))

    def test_user_not_authorized_accept_answer(self):
        user = factories.UserFactory.build()
        self.assertFalse(self.question.user_can_accept_answer(user))


class AnswerTest(TestCase):

    def test_slug_with_big_body(self):
        '''
        Test slug generation when body is greather than 50 characteres,
        max length defined for slug
        '''
        answer = factories.AnswerFactory.create(
            body='fgd fhrdy thf rtpw ymkjtnk netptirm vndkft guirtadh5o' \
                'dfkj sdkjf sdkjf sdkf sdfk sdkfj ksdf  lksdf ksdf kkksdfl'
        )
        slug = 'fgd-fhrdy-thf-rtpw-ymkjtnk-netptirm-vndkft-guirtad'
        self.assertEqual(answer.slug, slug)

    def test_slug_with_small_body(self):
        '''
        Test slug generation when body is lesser than 50 characteres,
        max length defined for slug
        '''
        answer = factories.AnswerFactory.create(
            body='fgd fhrdy thf rtpw ymkjtnk netpt ñsdjdjfá'
        )
        slug = 'fgd-fhrdy-thf-rtpw-ymkjtnk-netpt-nsdjdjfa'
        self.assertEqual(answer.slug, slug)
