from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):
    """
    This class represents the profile test case
    """

    def test_it_sends_set_password_link(self):
        """
        Test a set password link is sent via email
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        ### Assert that the token is set
        self.assertNotEqual(len(token), 0)

        ### Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual("Set password on healthchecks.io",
                         mail.outbox[0].subject)
        self.assertIn("Here's a link to set a password",
                      mail.outbox[0].body)

    def test_it_sends_report(self):
        """
        Test a report is sent
        """
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        ###Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual("Monthly Report", mail.outbox[0].subject)
        self.assertIn("This is a monthly report sent by healthchecks.io",
                      mail.outbox[0].body)

    def test_it_adds_team_member(self):
        """
        Test a member can be added to a team
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        ### Assert the existence of the member emails
        self.assertEqual(len(member_emails), 2)

        self.assertTrue(form["email"] in member_emails)

        ###Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("You have been invited to join alice@example.org",
                      mail.outbox[0].subject)
        self.assertIn("invites you to their healthchecks.io account",
                      mail.outbox[0].body)

    def test_add_team_member_checks_team_access_allowed_flag(self):
        """
        Test a member needs to have access
        """
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 403

    def test_it_removes_team_member(self):
        """
        Test a team member can be removed
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        """
        Test a team name can be set
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        """
        Test one needs access to set team name
        """
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        res = self.client.post("/accounts/profile/", form)
        assert res.status_code == 403

    def test_it_switches_to_own_team(self):
        """
        Test one can switch to own team
        """
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        """
        Test badges are shown
        """
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        res = self.client.get("/accounts/profile/")
        self.assertContains(res, "foo.svg")
        self.assertContains(res, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(res, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(res, "bobs-tag.svg")

    def test_it_creates_api_key(self):
        """
        Test creation of API key
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"create_api_key": "abcd"}
        res = self.client.post("/accounts/profile/", form)
        self.assertEqual(res.status_code, 200)

        # Set the API key
        self.alice.profile.refresh_from_db()
        api_key = self.alice.profile.api_key

        self.assertNotEqual(api_key, None)
        self.assertContains(res, "The API key has been created!")

    def test_it_revokes_api_key(self):
        """
        Test an API key can be revoked
        """
        self.client.login(username="alice@example.org", password="password")

        form = {"revoke_api_key": "efgh"}
        res = self.client.post("/accounts/profile/", form)
        self.assertEqual(res.status_code, 200)

        # API key should be set to None
        self.alice.profile.refresh_from_db()
        api_key = self.alice.profile.api_key

        # Assert that the API key is None
        self.assertEqual(api_key, "")
        self.assertContains(res, "The API key has been revoked!")
