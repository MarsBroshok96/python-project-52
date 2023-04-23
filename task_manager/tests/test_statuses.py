"""Test for statuses app"""
from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory, StatusFactory
from task_manager.statuses.models import Status
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from faker import Faker


fake = Faker()
MSG_NOT_AUTH = _('You are not authorized! Please sign in')
MSG_STATUS_UPDATED = _('Status successfully updated')
MSG_STATUS_DELETED = _('Status successfully deleted')


class StatusTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.status1 = StatusFactory()
        self.status2 = StatusFactory()

        self.params = {'name': fake.word()}

    def test_status_list_view(self):
        """Test status list view"""
        response = self.client.get('/statuses/')
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_NOT_AUTH
                         )

        self.client.force_login(self.user)
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status1.name)
        self.assertContains(response, self.status2.name)

    def test_status_list_view_has_update_and_delete_link(self):
        """Test status list view has update and delete link"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('delete_status',
                                              args=[self.status2.id]))
        self.assertContains(response, reverse('update_status',
                                              args=[self.status1.id]))

    def test_create_status(self):
        """Test create status"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_status'))
        self.assertTemplateUsed(response, 'statuses/form_status.html')
        response = self.client.post(reverse('create_status'), data=self.params)
        self.assertRedirects(response, reverse('status_list'))
        new_status = Status.objects.filter(name=self.params['name'])
        self.assertTrue(new_status.exists())

    def test_status_update(self):
        """Test update status"""
        self.client.force_login(self.user)
        status1 = Status.objects.filter(name=self.status1.name)
        self.assertTrue(status1.exists())
        response = self.client.post(reverse('update_status',
                                            args=[self.status1.id]),
                                    data=self.params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), MSG_STATUS_UPDATED)
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, self.params['name'])

    def test_status_delete(self):
        """Test delete status"""
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
        self.assertEqual(str(messages[0]), MSG_STATUS_DELETED)
        self.assertFalse(status2.exists())
