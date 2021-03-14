from django.http import response
from rest_framework.exceptions import ErrorDetail, ValidationError
from authentication.models import Profile
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class AuThenticationSerializerTest(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user('testusername', 'test@gmail.com', 'testpassword')
        self.test_user_profile = Profile.objects.create(user=self.test_user)
    
    def test_username_and_email_validation(self):
        user = {
            'first_name': 'Oluwaseun',
            'last_name' : 'Sekoni',
            'username': 'testusername',
            'email': 'test@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword',
            'gender': 'M',
            'address': '38, Pipeline Road, Mosan Bus Stop, Ipaja Road, Alimosho',
            "phone": "08060720222"
        }

        response = self.client.post('/auth/register/', user, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data['email'], [ErrorDetail(string='Email has already been taken', code='unique')])


    def test_login(self):

        user = User.objects.get(username=self.test_user)
        user = {
            'username': user.username,
            'password': 'testpassword',
            'email': user.email
        }

        # print(user)
        response = self.client.post('/auth/login/', user, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_validations(self):
        user = self.test_user
        credentials = {
            'username': user.username,
            'password': 'testpassword'
        }

        login_reponse = self.client.post('/auth/login/', credentials, format='json')

        self.assertEqual(login_reponse.status_code, status.HTTP_200_OK)

        token = login_reponse.data['access']

        self.client.force_login(user=self.test_user)

        data = {
            # 'old_password': 'testpassword',
            'password': 'password',
            'password2': 'password'
        }

        response = self.client.put('/auth/change_password/'+str(user.id)+'/', data)
        user = User.objects.get(username='testusername')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        # self.assertRaisesMessage('password', "This field is required.")

        self.assertEqual(response.data['old_password'], [ErrorDetail(string="This field is required.", code='required')])
        
        # assert the password did not change
        self.assertTrue(user.check_password('testpassword'))

        data2 = {
            'old_password': 'testpassword',
            'password': 'password',
            'password2': 'password234'
        }

        response2 = self.client.put('/auth/change_password/'+str(user.id)+'/', data2)

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response2.data['password'], [ErrorDetail(string="Password fields do not match", code='invalid')])

        # self.assertRaisesMessage(ErrorDetail, expected_message="")


    def test_password_reset_validations(self):
        data = {
            # 'email': self.test_user.email
        }
        response = self.client.post('/auth/password/reset/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        self.assertEqual(response.data['email'], [ErrorDetail(string="This field is required.", code="required")])

    def test_if_password_reset_does_not_send_email_to_an_email_that_does_not_exist(self):
        data = {
            'email': 'userdoesnotexist@test.com'
        }

        response = self.client.post('/auth/password/reset/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        self.assertEqual(response.data['email'], [ErrorDetail(string="Email does not exist", code="invalid")])

        
        
