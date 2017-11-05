from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            self.check.last_ping = timezone.now() - td(days=3)
            self.check.status = "up"
            self.check.save()
            r = self.client.get("/checks_failed/")
            self.assertContains(r, "Alice Was Here", status_code=200)

    def test_it_does_not_show_checks_that_have_not_failed(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/checks_failed/")
            self.assertContains(r, "No Failed checks", status_code=200)

