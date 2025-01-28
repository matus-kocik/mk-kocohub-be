from django.test import TestCase

from apps.users.models import CustomUser


class CustomUserManagerTestCase(TestCase):
    """
    Test case for the CustomUserManager.
    """

    def test_create_user(self):
        """
        Test creating a regular user with the custom manager.
        """
        user = CustomUser.objects.create_user(
            email="newuser@example.com",
            password="password123",
            first_name="New",
            last_name="User",
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Test creating a superuser with the custom manager.
        """
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
        )
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class CustomUserTestCase(TestCase):
    """
    Test case for the CustomUser model.
    """

    def setUp(self):
        """
        Setup a test user for use in the test cases.
        """
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

    def test_user_creation(self):
        """
        Test that the user is created with the correct attributes.
        """
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.check_password("testpassword"), True)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_full_name(self):
        """
        Test that the user's full name is generated correctly.
        """
        self.assertEqual(self.user.full_name, "Test User")

    def test_str_representation(self):
        """
        Test that the user's string representation is correct.
        """
        self.assertEqual(str(self.user), "testuser@example.com")
