from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):
    """
    This class represents the login test case
    """

    def test_it_sends_link(self):
        """
        Test a link is sent via email
        """
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}
        count0 = User.objects.count()

        res = self.client.post("/accounts/login/", form)
        assert res.status_code == 302
        count1 = User.objects.count()

        ### Assert that a user was created
        self.assertEqual(count1, count0+1)
        user = User.objects.get(email="alice@example.org")
        self.assertEqual(user.email, "alice@example.org")

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Log in to healthchecks.io')
        ### Assert contents of the email body
        self.assertIn('To log into healthchecks.io',
                      mail.outbox[0].body)

        ### Assert that check is associated with the new user
        check = Check.objects.get(user=user)
        self.assertEqual(check.user, user)

    def test_it_pops_bad_link_from_session(self):
        """
        Test a bad link is popped from session
        """
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session
