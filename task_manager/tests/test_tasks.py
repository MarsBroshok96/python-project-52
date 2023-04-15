from django.test import TestCase, Client
from task_manager.tests.factories import UserFactory, TaskFactory, StatusFactory
from task_manager.tasks.models import Task
from django.contrib.messages import get_messages
from django.urls import reverse


class TaskTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.status1 = StatusFactory()
        self.task1 = TaskFactory(created_by=self.user1, status=self.status1)
        self.task2 = TaskFactory()

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You are not authorized! Please sign in'
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

    def test_create_task(self):
        good_params = {'name': 'Random task name',
                       'description': 'Random task description',
                       'status': self.status1.id,
                       'assigned_to': self.user1.id,
                       }

        bad_params = {'name': 'Random task name',
                      'description': 'Random task description',
                      'status': 'not existing status',
                      'assigned_to': 'not existing user',
                      }

        self.client.force_login(self.user1)
        response = self.client.get(reverse('task_create'))
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        response = self.client.post(reverse('task_create'), data=bad_params)
        errors = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertIn('assigned_to', errors)

        response = self.client.post(reverse('task_create'), data=good_params)
        self.assertRedirects(response, reverse('task_list'))
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, good_params['name'])

    def test_task_update(self):
        good_params = {'name': 'New task name',
                       'description': 'New task description',
                       'status': self.status1.id,
                       'assigned_to': self.user1.id,
                       }

        bad_params = {'name': 'New task name',
                      'description': 'New task description',
                      'status': 'not existing status',
                      'assigned_to': 'not existing user',
                      }

        self.client.force_login(self.user1)
        task1 = Task.objects.filter(name=self.task1.name)
        self.assertTrue(task1.exists())
        response = self.client.post(reverse('task_update',
                                            args=[self.task1.id]),
                                    data=bad_params)
        errors = response.context['form'].errors
        self.assertIn('status', errors)
        self.assertIn('assigned_to', errors)

        response = self.client.post(reverse('task_update',
                                            args=[self.task1.id]),
                                    data=good_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))

        self.assertEqual(Task.objects.get(id=self.task1.id).name,
                         good_params['name']
                         )
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, good_params['name'])

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
                         'You have no permission to delete this task'
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
        self.assertContains(response, self.task1.created_by.username)
        self.assertContains(response, self.task1.assigned_to.username)

    def test_user_with_task_protected(self):
        "user related to task can't be deleted"
        self.client.force_login(self.user1)
        response = self.client.post(reverse('user_del', args=[self.user1.id]))
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Can\'t delete user because it used'
                         )
        response = self.client.get(reverse('user_list'))
        self.assertContains(response, self.user1.username)
