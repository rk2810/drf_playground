from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserModelTest(TestCase):
    """Test case for the User model"""

    def test_create_user_with_email(self):
        """Create new user with email """
        email = "test@test.com"
        password = "testpass"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        email = "teSt@TEST.cOm"
        password = "test"
        user = User.objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())
