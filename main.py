import unittest
import app

class FlaskTest(unittest.TestCase):

    
    def test_index(self):
        tester = app.app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    
    def test_login_page_loads(self):
        tester = app.app.test_client(self)
        response = tester.get('/login', follow_redirects=True)
        self.assertIn(b'Login', response.data)

   
    def test_correct_login(self):
        tester = app.app.test_client(self)
        response = tester.post('/login', data=dict(username='testuser', password='testpass'), follow_redirects=True)
        self.assertIn(b'Welcome to the home page!', response.data)

    
    def test_incorrect_login(self):
        tester = app.app.test_client(self)
        response = tester.post('/login', data=dict(username='wronguser', password='wrongpass'), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    
    def test_home_requires_login(self):
        tester = app.app.test_client(self)
        response = tester.get('/home', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    
    def test_users_loaded_from_file(self):
        self.assertEqual(app.users['testuser'], 'testpass')

    
    def test_users_saved_to_file(self):
        app.users['newuser'] = 'newpass'
        app.save_users()
        with open('users.txt', 'r') as f:
            lines = [x.strip() for x in f]
            self.assertIn('newuser:newpass', lines)
        app.users.pop('newuser')
        app.save_users()


if __name__ == '__main__':
    unittest.main()
