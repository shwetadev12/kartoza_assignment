from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point


class UserSignupViewTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'longitude': '123.456',
            'latitude': '78.910'
        }

    def test_signup_view_success(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signin_url)

        # Check if the user was created with the correct location
        User = get_user_model()
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.location.x, float(self.user_data['longitude']))
        self.assertEqual(user.location.y, float(self.user_data['latitude']))

    def test_signup_view_invalid_form(self):
        # Submit an invalid form (missing required fields)
        invalid_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'longitude', 'This field is required.')
        self.assertFormError(response, 'form', 'latitude', 'This field is required.')

        # Check if the user was not created
        User = get_user_model()
        self.assertFalse(User.objects.filter(username=self.user_data['username']).exists())


class UserSigninViewTest(TestCase):
    def setUp(self):
        self.signin_url = reverse('signin')
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',
                                                         location=Point(27.2356, 75.2356))

    def test_successful_signin(self):
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('profile', kwargs={'pk': self.user.pk}))

    def test_invalid_credentials(self):
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',
                                                         location=Point(27.2356, 75.2356))
        self.profile_url = reverse('profile', kwargs={'pk': self.user.pk})

    def test_view_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_profile.html')
        self.assertEqual(response.context['user'], self.user)


class UsersLocationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('map')
        User = get_user_model()
        User.objects.create_user(username='user1', password='password1', location=Point(27.2356, 75.2356))
        User.objects.create_user(username='user2', password='password2', location=Point(28.2356, 76.2356))

    def test_users_location_view(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_location.html')


class UserSignOutViewTest(TestCase):
    def test_sign_out_redirects_to_sign_in_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('signin'))
