from django.test import TestCase

from users.models import User


class CategoryTestCase(TestCase):
    def test_user_create(self):
        user = User.objects.create(email="b@example.com", password="example24")
        self.assertEqual(user.email, "b@example.com")
        self.assertTrue(user.password, user.check_password("example24"))

    def test_superuser_create(self):
        user = User.objects.create(
            email="c@example.com",
            password="example24",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.assertEqual(user.email, "c@example.com")
        self.assertTrue(user.password, user.check_password("example24"))
        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_superuser, True)
        self.assertTrue(user.is_active, True)
