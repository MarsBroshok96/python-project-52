from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory, LabelFactory, TaskFactory
from task_manager.labels.models import Label
from django.contrib.messages import get_messages
from django.urls import reverse
from faker import Faker
from django.utils.translation import gettext_lazy as _


fake = Faker()
MSG_NOT_AUTH = _('You are not authorized! Please sign in')
MSG_LABEL_PROTECTED_ERROR = _('Can\'t delete label because it used')


class LabelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.label1 = LabelFactory()
        self.label2 = LabelFactory()
        self.label3 = LabelFactory()
        self.user = UserFactory()
        self.task = TaskFactory(labels=[self.label1, self.label2])

        self.params = {'name': fake.word()}

    def test_label_list_view(self):
        response = self.client.get(reverse('label_list'))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_NOT_AUTH
                         )

        self.client.force_login(self.user)
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label1.name)
        self.assertContains(response, self.label2.name)

    def test_label_list_view_has_update_and_delete_link(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('label_delete',
                                              args=[self.label2.id]))
        self.assertContains(response, reverse('label_update',
                                              args=[self.label1.id]))

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('label_create'))
        self.assertTemplateUsed(response, 'labels/form_label.html')
        response = self.client.post(reverse('label_create'), data=self.params)
        self.assertRedirects(response, reverse('label_list'))
        new_label = Label.objects.filter(name=self.params['name'])
        self.assertTrue(new_label.exists())

    def test_label_update(self):
        self.client.force_login(self.user)
        label1 = Label.objects.filter(name=self.label1.name)
        self.assertTrue(label1.exists())
        response = self.client.post(reverse('label_update',
                                            args=[self.label1.id]),
                                    data=self.params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, self.params['name'])

    def test_label_delete(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('label_list'))
        self.assertContains(response, self.label3.name)
        response = self.client.post(reverse('label_delete',
                                            args=[self.label3.id]))
        self.assertRedirects(response, reverse('label_list'))
        response = self.client.get(reverse('label_list'))
        self.assertNotContains(response, self.label3.name)

    def test_label_on_task_protected(self):
        "label related to task can't be deleted"
        self.client.force_login(self.user)
        response = self.client.post(reverse('label_delete',
                                            args=[self.label1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_LABEL_PROTECTED_ERROR
                         )
