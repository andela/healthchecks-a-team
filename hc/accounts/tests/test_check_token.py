from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):
    """
    This class represents the token test case
    """

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        """
        Test a form is shown
        """
        res = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(res, "You are about to log in")

    def test_it_redirects(self):
        """
        Test a user with a token is redirected
        """
        res = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(res, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_it_redirects_already_logged_in(self):
        """
        Test a logged in user is redirected
        """
        form = {"email": self.alice.email, "password": "password"}
        res = self.client.post("/accounts/login/", form)
        self.assertRedirects(res, "/checks/")

    def test_login_with_bad_token(self):
        """
        Test a user with a bad token is redirected to login
        """
        res = self.client.post("/accounts/check_token/alice/bad-token/")
        self.assertRedirects(res, "/accounts/login/")
