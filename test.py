from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """What should be done before every test is run"""
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_home(self):
        """Ensure that the right template is displayed and the session contains relevant info (board, highscore, etc)"""
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('number_plays'))
            self.assertIn(b'High Score:', res.data)
            self.assertIn(b'<form class="word-form" id="word-form" method="POST">', res.data)
            self.assertIn(b'Score:', res.data)


    def test_word_valid(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [['R', 'H', 'I', 'N', 'O'],['R', 'H', 'I', 'N', 'O'],['R', 'H', 'I', 'N', 'O'],['R', 'H', 'I', 'N', 'O'],['R', 'H', 'I', 'N', 'O']]
        res = self.client.get('/check-word?word=rhino')
        self.assertEqual(res.json['result'], "ok")


    def test_word_invalid(self):
        """test word hihgly unlikely to be on the board"""
        self.client.get('/')
        res = self.client.get('/check-word?word=improbable')
        self.assertEqual(res.json['result'], 'not-on-board')

    
    def test_not_word(self):
        """Test word that doesn't exist"""
        self.client.get('/')
        res = self.client.get('/check-word?word=rfbueryfbeuyrf')
        self.assertEqual(res.json['result'], "not-word")


            