import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Post

# Create your tests here.


class PostMethodTests(TestCase):
    def test_was_created_lte_published(self):
        """
        Post Created Date must be less than or equal to Published Date
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        past_publish = Post(published_date=time)
        self.assertEqual(past_publish.created_date <= past_publish.published_date, True)


class PostViewTest(TestCase):
    def test_list_view_with_no_questions(self):
        """
        If no posts exist, an appropriate message should be displayed.
        :return:
        """
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_list_view_without_published_date(self):
        """
        Post with a published_date in the future should not be displayed.
        :return:
        """
        Post(title="Empty", text="Empty post")
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, "No Posts are available.", status_code=200)
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_list_view_with_a_past_published_date(self):
        """
        Post with a published date less than created date
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=-30)
        Post(title="Past", text="Past post", published_date=time)
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, "No Posts are available.", status_code=200)
        self.assertQuerysetEqual(response.context['post_list'], [])


class PostDetailTests(TestCase):
    def test_detail_view_with_a_past_published_date(self):
        time = timezone.now() + datetime.timedelta(days=-30)
        me = User.objects.get(username='admin')
        post = Post(author=me, title="Past", text="Past post", published_date=time)
        response = self.client.get(reverse('blog:post_detail', args=(post.id,)))
        self.assertEqual(response.status_code, 404)
