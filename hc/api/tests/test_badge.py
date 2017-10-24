from django.conf import settings
from django.core.signing import base64_hmac

from hc.api.models import Check
from hc.test import BaseTestCase


class BadgeTestCase(BaseTestCase):

    def setUp(self):
        super(BadgeTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

    def test_it_rejects_bad_signature(self):
        r = self.client.get("/badge/%s/12345678/foo.svg" % self.alice.username)
        
        ### Assert the expected response status code
        self.assertEqual(r.status_code, 400)
        
    def test_it_returns_svg(self):
        sig = base64_hmac(str(self.alice.username), "foo", settings.SECRET_KEY)
        sig = sig[:8].decode("utf-8")
        url = "/badge/%s/%s/foo.svg" % (self.alice.username, sig)

        r = self.client.get(url)
        ### Assert that the svg is returned

        # self.assertEqual(r.status_code, 400)
        self.assertTrue(b'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"' in r.content)
        
        
