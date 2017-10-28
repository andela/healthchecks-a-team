from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):
    """
    This class represents team access middleware test case
    """
    def test_it_handles_missing_profile(self):
        """
        Test that a missing profile is taken care of
        """
        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        self.client.login(username="ned@example.org", password="password")
        res = self.client.get("/about/")
        self.assertEqual(res.status_code, 200)

        ### Assert the new Profile objects count
        self.assertEqual(Profile.objects.count(), 1)
