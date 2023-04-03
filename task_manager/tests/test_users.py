from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from faker import Faker


fake = Faker()

UNDER_MIN_PASS_MSG = "This password is too short. " \
                     "It must contain at least 3 characters."

good_params = {'first_name': fake.first_name(),
               'last_name': fake.last_name(),
               'password1': fake.password(),
               'password2': '',
               'username': fake.user_name(),
               'email': fake.email()
               }
good_params['password2'] = good_params['password1']

bad_params = {'first_name': fake.first_name(),
              'last_name': fake.last_name(),
              'password1': '',
              'password2': '',
              'username': fake.user_name(),
              'email': fake.email()
              }
bad_params['password1'] = 'qw'
bad_params['password2'] = bad_params['password1']


class UsersTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_user_list_view(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_user_list_view_has_update_and_delete_link(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('user_del',
                                              args=[self.user2.id]))
        self.assertContains(response, reverse('user_update',
                                              args=[self.user1.id]))

    def test_create_user(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'users/register.html')
        response = self.client.post(reverse('register'), data=bad_params)
        errors = response.context['form'].errors
        self.assertIn('password2', errors)
        self.assertEqual([UNDER_MIN_PASS_MSG], errors['password2'])

        response = self.client.post(reverse('register'), data=good_params)
        self.assertRedirects(response, reverse('user_list'))
#        new_user = User.objects.filter(username=good_params['username'])
#        self.assertTrue(new_user.exists())
        new_user = User.objects.filter(pk=3).first()
        self.assertEqual(new_user.username, good_params['username'])

    def test_user_update(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user_update', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can`t edit other users')

        user1 = User.objects.filter(username=self.user1.username)
        self.assertTrue(user1.exists())
        response = self.client.post(reverse('user_update',
                                            args=[self.user1.id]),
                                    data=good_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User`s info successfully updated')
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, good_params['username'])

    def test_user_delete(self):
        self.client.force_login(self.user1)
        user1 = User.objects.filter(username=self.user1.username)
        self.assertTrue(user1.exists())

        response = self.client.get(reverse('user_del', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You can`t edit other users')

        response = self.client.post(reverse('user_del', args=[self.user1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User successfully Deleted')
        self.assertFalse(user1.exists())
