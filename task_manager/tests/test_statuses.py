from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory, StatusFactory
from task_manager.statuses.models import Status
from django.contrib.messages import get_messages
from django.urls import reverse


params = {'name': 'Random status name'}


class StatusTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.status1 = StatusFactory()
        self.status2 = StatusFactory()

    def test_status_list_view(self):
        response = self.client.get('/statuses/')
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You are not authorized! Please sign in'
                         )

        self.client.force_login(self.user)
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status1.name)
        self.assertContains(response, self.status2.name)

    def test_status_list_view_has_update_and_delete_link(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('delete_status',
                                              args=[self.status2.id]))
        self.assertContains(response, reverse('update_status',
                                              args=[self.status1.id]))

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_status'))
        self.assertTemplateUsed(response, 'statuses/form_status.html')
        response = self.client.post(reverse('create_status'), data=params)
        self.assertRedirects(response, reverse('status_list'))
        new_status = Status.objects.filter(name=params['name'])
        self.assertTrue(new_status.exists())

    def test_status_update(self):
        self.client.force_login(self.user)
        status1 = Status.objects.filter(name=self.status1.name)
        self.assertTrue(status1.exists())
        response = self.client.post(reverse('update_status',
                                            args=[self.status1.id]),
                                    data=params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Status successfully updated')
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, params['name'])

    def test_status_delete(self):
        self.client.force_login(self.user)
        status2 = Status.objects.filter(name=self.status2.name)
        self.assertTrue(status2.exists())

        response = self.client.post(reverse('delete_status',
                                            args=[self.status2.id]
                                            ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Status successfully deleted')
        self.assertFalse(status2.exists())
