from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@.com')
        self.course = Course.objects.create(name='test_course', description='...', owner=self.user)
        self.lesson = Lesson.objects.create(name='test_lesson', description='...', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        # print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('materials:lessons-create')
        data = {'name': 'test_lesson2', 'video': 'https://www.youtube.com/'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lessons-update', args=(self.lesson.pk,))
        data = {'name': 'test_lesson3'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'test_lesson3')

    def test_lesson_delete(self):
        url = reverse('materials:lessons-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lessons-list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results':
                      [{'id': self.lesson.pk,
                        'video': None,
                        'name': self.lesson.name,
                        'description': self.lesson.description,
                        'preview': None,
                        'course': self.lesson.course.pk,
                        'owner': self.lesson.owner.pk}]}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@.com')
        self.course = Course.objects.create(name='test_course', description='', owner=self.user)
        self.lesson = Lesson.objects.create(name='test_lesson', description='', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_subscription(self):
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Подписка добавлена')
