from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    def setUp(self):
        super(AddCheckTestCase, self).setUp()
        self.url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")

    def test_it_works(self):
        r = self.client.post(self.url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access_works(self):
        # Test that team access works
        self.client.post(self.url)
        self.check = Check.objects.filter(user=self.alice)
        check_code = self.check.first().code
        self.client.logout()
        self.client.login(username="bob@example.org", password="password")
        r = self.client.get("/checks/")
        self.assertIn(str(check_code), str(r.content))

        self.client.logout()
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.get("/checks/")
        self.assertNotIn(str(check_code), str(r.content))
