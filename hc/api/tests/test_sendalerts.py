from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        # assert result, "handle_many should return True"
        self.assertTrue(result)

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        self.assertTrue(set(names) == set(handled_names))
        ### The above assert fails. Make it pass

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        result = Command().handle_one(check)
        self.assertTrue(result)


    ### Assert when Command's handle many that when handle_many should 
    # return True
    
    # handle many test re-written to handle the 'going down' condition
    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_checks_that_are_going_down(self, mock):
        tomorrow = timezone.now() + timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = tomorrow
            check.status = "down"
            check.save()

        result = Command().handle_many()
        self.assertTrue(result, "handle_many should return True")
