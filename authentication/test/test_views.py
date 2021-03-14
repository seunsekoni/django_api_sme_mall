from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from ..models import Profile
from rest_framework import status
from django.core import mail

class AuthenticationViewTest(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user('testusername', 'test@gmail.com', 'testpassword')
        self.test_user_profile = Profile.objects.create(user=self.test_user)

        self.factory = APIRequestFactory()

    def test_user_registration(self):

        user = {
            'first_name': 'Oluwaseun',
            'last_name' : 'Sekoni',
            'username': 'testusername1',
            'email': 'test1@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword',
            'gender': 'M',
            'address': '38, Pipeline Road, Mosan Bus Stop, Ipaja Road, Alimosho',
            "phone": "08060720222"
        }

        response = self.client.post('/auth/register/', user, format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], user['first_name'])

        # get user profile
        find_user = User.objects.first()
        user_profile = Profile.objects.get(user=find_user.id)

        # testing if email was sent
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome To The SME MALL')

        self.assertEqual(find_user.id, user_profile.user.id)
        self.assertFalse('password' in response.data['user'])

    def test_change_password(self):
        user = self.test_user
        credentials = {
            'username': user.username,
            'password': 'testpassword'
        }

        login_reponse = self.client.post('/auth/login/', credentials, format='json')

        self.assertEqual(login_reponse.status_code, status.HTTP_200_OK)

        token = login_reponse.data['access']

        # client = APIClient()
        # client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.client.force_login(user=self.test_user)

        data = {
            'old_password': 'testpassword',
            'password': 'password',
            'password2': 'password'
        }

        # response = self.client.put('/auth/change_password/'+str(user.id)+'/', data, HTTP_AUTHORIZATION='Bearer {}'.format(token))
        response = self.client.put('/auth/change_password/'+str(user.id)+'/', data)
        user = User.objects.get(username='testusername')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # assert the password changed
        self.assertTrue(user.check_password('password'))

    def test_password_reset(self):
        data = {
            'email': self.test_user.email
        }
        response = self.client.post('/auth/password/reset/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # testing if email was sent
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset')
        self.assertTemplateUsed('authentication/email/password_reset_form.html')
        

    def test_logout(self):
        
        auth_user = self.client.force_login(user=self.test_user)

        response = self.client.post('/auth/logout/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)