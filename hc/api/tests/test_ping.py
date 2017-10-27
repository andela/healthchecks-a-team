from hc.api.models import Check, Ping
from hc.test import BaseTestCase
from django.test import Client


class PingTestCase(BaseTestCase):
    def setUp(self):
        super(PingTestCase, self).setUp()
        self.check = Check.objects.create()

    def test_it_works(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertTrue(r.status_code == 200)

        self.check.refresh_from_db()
        self.assertTrue(self.check.status == "up")

        ping = Ping.objects.latest("id")
        self.assertTrue(ping.scheme == "http")

    def test_it_handles_bad_uuid(self):
        r = self.client.get("/ping/not-uuid/")
        self.assertTrue(r.status_code == 400)

    def test_it_handles_120_char_ua(self):
        ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/44.0.2403.89 Safari/537.36")

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        self.assertTrue(r.status_code == 200)

        ping = Ping.objects.latest("id")
        self.assertTrue(ping.ua == ua)

    def test_it_truncates_long_ua(self):
        ua = "01234567890" * 30

        r = self.client.get("/ping/%s/" % self.check.code, HTTP_USER_AGENT=ua)
        self.assertTrue(r.status_code == 200)

        ping = Ping.objects.latest("id")
        self.assertTrue(len(ping.ua) == 200)
        self.assertTrue(ua.startswith(ping.ua))

    def test_it_reads_forwarded_ip(self):
        ip = "1.1.1.1"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip)
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's remote address
        self.assertTrue(r.status_code == 200)
        self.assertTrue(ping.remote_addr == "1.1.1.1")

        ip = "1.1.1.1, 2.2.2.2"
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="3.3.3.3")
        ping = Ping.objects.latest("id")
        self.assertTrue(r.status_code == 200)
        self.assertTrue(ping.remote_addr == "1.1.1.1")

    def test_it_reads_forwarded_protocol(self):
        r = self.client.get("/ping/%s/" % self.check.code,
                            HTTP_X_FORWARDED_PROTO="https")
        ping = Ping.objects.latest("id")
        ### Assert the expected response status code and ping's scheme
        self.assertTrue(r.status_code == 200)
        self.assertTrue(ping.scheme == "https")

    def test_it_never_caches(self):
        r = self.client.get("/ping/%s/" % self.check.code)
        self.assertTrue("no-cache" in r.get("Cache-Control"))

    ### Test that when a ping is made a check with a paused status 
    # changes status
    def test_it_changes_status_of_paused_check(self):
        check = Check(user=self.alice, status="up")
        check.save()

        self.assertTrue(check.status == "up")
        url = "/api/v1/checks/%s/pause" % check.code
        self.client.post(
            url, "", content_type="application/json", HTTP_X_API_KEY="abc")
        check.refresh_from_db()
        self.assertTrue(check.status == "paused")

        self.client.get("/ping/%s/" % check.code)
        check.refresh_from_db()
        self.assertTrue(check.status == "up")

    ### Test that a post to a ping works
    def test_that_post_to_a_ping_works(self):
        r = self.client.post("/ping/%s/" % self.check.code)
        self.assertTrue(r.status_code == 200)

    ### Test that the csrf_client head works
    def test_that_csrf_client_head_works(self):
        # create a csrf client
        csrf_client = Client(enforce_csrf_checks=True)

        r = csrf_client.get("/ping/%s/" % self.check.code)
        self.assertTrue(r.status_code == 200)
