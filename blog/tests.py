from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Blog, ContactQuery, Website


class ContentTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.website = Website.objects.create(name='Example', slug='example')
        self.user = get_user_model().objects.create_user(
            username='tester',
            password='secret123',
        )
        self.client.force_authenticate(user=self.user)

    def test_existing_default_for_blog_model_is_blog(self):
        blog = Blog.objects.create(
            website=self.website,
            title='First Post',
            content='Hello world',
            is_published=True,
        )

        self.assertEqual(blog.content_type, Blog.BLOG)

    def test_case_study_endpoint_creates_case_study(self):
        response = self.client.post(
            f'/api/{self.website.slug}/case-studies/',
            {
                'title': 'Case Study One',
                'content': 'Detailed result',
                'is_published': True,
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content_type'], Blog.CASE_STUDY)
        self.assertTrue(Blog.objects.filter(content_type=Blog.CASE_STUDY, title='Case Study One').exists())

    def test_blog_endpoint_ignores_case_study_content_type_from_dashboard_payload(self):
        response = self.client.post(
            f'/api/{self.website.slug}/blogs/',
            {
                'title': 'Blog One',
                'content': 'Body copy',
                'is_published': True,
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotIn('content_type', response.data)
        self.assertTrue(Blog.objects.filter(content_type=Blog.BLOG, title='Blog One').exists())


class ContactQueryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.website = Website.objects.create(name='4xcode.com', slug='4xcode-com')
        self.user = get_user_model().objects.create_user(
            username='query-admin',
            password='secret123',
        )

    def test_contact_query_submit_requires_authentication(self):
        response = self.client.post(
            f'/api/{self.website.slug}/contact-queries/submit/',
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'number': '+923001234567',
                'project_detail': 'Need a new landing page and admin dashboard.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 401)

    def test_authenticated_contact_query_submit_saves_record(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'/api/{self.website.slug}/contact-queries/submit/',
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'number': '+923001234567',
                'project_detail': 'Need a new landing page and admin dashboard.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactQuery.objects.count(), 1)
        self.assertEqual(ContactQuery.objects.get().website, self.website)

    def test_contact_query_list_requires_authentication(self):
        response = self.client.get(f'/api/{self.website.slug}/contact-queries/')
        self.assertEqual(response.status_code, 401)

    def test_authenticated_contact_query_list_and_detail(self):
        contact_query = ContactQuery.objects.create(
            website=self.website,
            name='John Doe',
            email='john@example.com',
            number='+923001234567',
            project_detail='Build a case studies page.',
        )
        self.client.force_authenticate(user=self.user)

        list_response = self.client.get(f'/api/{self.website.slug}/contact-queries/')
        detail_response = self.client.get(f'/api/{self.website.slug}/contact-queries/{contact_query.id}/')

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(list_response.data[0]['id'], contact_query.id)
        self.assertEqual(detail_response.data['project_detail'], contact_query.project_detail)
