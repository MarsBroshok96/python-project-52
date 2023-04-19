from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory, TaskFactory, StatusFactory
from task_manager.tasks.models import Task
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from faker import Faker


fake = Faker()
MSG_NOT_AUTH = _('You are not authorized! Please sign in')
MSG_DELETE_PERMISSION_ERROR = _('You have no permission to delete this task')
MSG_USER_PROTECTED_ERROR = _('Can\'t delete user because it used')


class TaskTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.status1 = StatusFactory()
        self.task1 = TaskFactory(created_by=self.user1,
                                 executor=self.user1,
                                 status=self.status1)
        self.task2 = TaskFactory()
        self.good_params = {'name': fake.word(),
                            'description': fake.text(max_nb_chars=50),
                            'status': self.status1.id,
                            'executor': self.user1.id,
                            }

        self.bad_params = {'name': fake.word(),
                           'description': fake.text(max_nb_chars=50),
                           'status': fake.word(),
                           'executor': fake.name(),
                           }

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_NOT_AUTH
                         )
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_task_list_view_has_update_and_delete_link(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('task_delete',
                                              args=[self.task2.id]))
        self.assertContains(response, reverse('task_update',
                                              args=[self.task1.id]))

    def test_filter_tasks_by_status(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_list'),
                                   data={'status': self.status1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_tasks_by_executor(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_list'),
                                   data={'executor': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_tasks_by_current_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_list'),
                                   data={'self_tasks': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_create_task(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_create'))
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        response = self.client.post(reverse('task_create'),
                                    data=self.bad_params)
        errors = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertIn('executor', errors)

        response = self.client.post(reverse('task_create'),
                                    data=self.good_params)
        self.assertRedirects(response, reverse('task_list'))
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, self.good_params['name'])

    def test_task_update(self):

        self.client.force_login(self.user1)
        task1 = Task.objects.filter(name=self.task1.name)
        self.assertTrue(task1.exists())
        response = self.client.post(reverse('task_update',
                                            args=[self.task1.id]),
                                    data=self.bad_params)
        errors = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertIn('executor', errors)

        response = self.client.post(reverse('task_update',
                                            args=[self.task1.id]),
                                    data=self.good_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))

        self.assertEqual(Task.objects.get(id=self.task1.id).name,
                         self.good_params['name']
                         )
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, self.good_params['name'])

    def test_task_delete(self):
        "test that task can be deleted only by its creator"
        self.client.force_login(self.user2)
        response = self.client.get(reverse('task_delete', args=[self.task1.id]))
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

        response = self.client.post(reverse('task_delete',
                                            args=[self.task1.id]
                                            ))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_DELETE_PERMISSION_ERROR
                         )
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, self.task1.name)
        self.client.logout()

        self.client.force_login(self.user1)
        response = self.client.post(reverse('task_delete', args=[self.task1.id])
                                    )
        self.assertRedirects(response, reverse('task_list'))
        response = self.client.get(reverse('task_list'))
        self.assertNotContains(response, self.task1.name)

    def test_task_detail(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_detail', args=[self.task1.id]))
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task1.description)
        self.assertContains(response, self.task1.status.name)
        self.assertContains(response, self.task1.created_by)
        self.assertContains(response, self.task1.executor)

    def test_user_with_task_protected(self):
        "user related to task can't be deleted"
        self.client.force_login(self.user1)
        response = self.client.post(reverse('user_del', args=[self.user1.id]))
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         MSG_USER_PROTECTED_ERROR
                         )
        response = self.client.get(reverse('user_list'))
        self.assertContains(response, self.user1.username)
