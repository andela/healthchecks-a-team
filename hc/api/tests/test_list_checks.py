import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):
    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        ### Assert the response status code
        assert r.status_code == 200

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        ### Assert the expected length of checks
        assert len(checks) == 2
        ### Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        ### last_ping, n_pings and pause_url
        assert self.a1.timeout == td(seconds=3600)
        assert self.a1.grace == td(seconds=900)
        assert self.a1.status == "new"
        assert self.a1.last_ping == self.now
        r = self.a1.to_dict()
        assert r['ping_url'] == "http://localhost:8000/ping/" + str(self.a1.code)
        assert r['pause_url'] == "http://localhost:8000/api/v1/checks/" + str(self.a1.code) + "/pause"

        assert self.a2.timeout == td(seconds=86400)
        assert self.a2.grace == td(seconds=3600)
        assert self.a2.status == "up"
        assert self.a2.last_ping == self.now
        r = self.a2.to_dict()
        assert r['ping_url'] == "http://localhost:8000/ping/" + str(self.a2.code)
        assert r['pause_url'] == "http://localhost:8000/api/v1/checks/" + str(self.a2.code) + "/pause"



    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

            ### Test that it accepts an api_key in the request


    def get_checks(self):
        return self.client.get("/api/v1/checks/")

    def test_it_accepts_api_key_in_request(self):
        r = self.get_checks()
        data = r.json()
        self.assertTrue(data['error'], 'wrong api_key')


