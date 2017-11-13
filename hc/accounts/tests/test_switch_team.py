from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):
    """
    This class represents the switch team test case
    """

    def test_it_switches(self):
        """
        Test that a superuser can switch teams
        """
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        res = self.client.get(url, follow=True)

        ### Assert the contents of r
        self.assertRedirects(res, "/checks/")

    def test_it_checks_team_membership(self):
        """
        Test users can switch to teams they are members of
        """
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        res = self.client.get(url)
        ### Assert the expected error code
        self.assertEqual(res.status_code, 403)

    def test_it_switches_to_own_team(self):
        """
        Test that a user can switch to their own team
        """
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        res = self.client.get(url, follow=True)
        ### Assert the expected error code
        self.assertEqual(res.status_code, 200)
