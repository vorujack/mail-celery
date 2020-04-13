from unittest.mock import patch

from django.test import TestCase
from django.conf import settings
from .tasks import send_email
# Create your tests here.


class TestSupport(TestCase):
    """
    Test scenario get list of users and send email to them
    """
    SENDER_EMAIL_ADDRESS = getattr(settings, 'SENDER_EMAIL_ADDRESS')

    def mock_send_mail_success(*args, **kwargs):
        pass

    @patch('django.core.mail')
    def test_send_email_success(self, mock_send_mail):
        """
        in this scenario we must post information to send email and response
        then send mail success and email sent
        :param mock_send_mail:
        :return:
        """
        data = {
            "subject": "Problem Config Config proxy",
            "message": "Please, Help.",
            "receivers": ["noemail@test.com"]
        }
        send_email(**data)
        mock_send_mail.asset_called()
