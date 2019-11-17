from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        """Setup a few stuff like a super user thats logged in 
        and a regular user to show up in list."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com", password="somepass"
        )
        # force login this admin user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create(
            email="user@test.com", password="pass", name="Some Name"
        )

    def test_user_listed(self):
        """Test to check if admin page loads list of users correctly"""
        url = reverse("admin:core_user_changelist")
        print(url)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """the user edit page"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test if create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
