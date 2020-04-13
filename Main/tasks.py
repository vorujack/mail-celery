import logging

from django.conf import settings
from django.core.mail import send_mail

from user_notify.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=settings.NUMBER_OF_RETRIES_RUN_TASK)
def send_email(self, subject, message, receivers):
    """
    try to send email to user.
    try this job 10 times on failure
    :param self: celery task to retry
    :param subject: email subject
    :param message: email content
    :param receivers: email address list
    :return: nothing
    """
    num_tried = 0
    # after a problem arises tries to call logger.error the size of NUMBER_OF_LOG
    try:
        num_tried += 1
        send_mail(
            subject,
            message,
            settings.SENDER_EMAIL_ADDRESS,
            receivers
        )
        logger.info("send notification to user")
        return
    except TypeError as e:
        logger.error("failed send email: {}".format(message))
        logger.error(e)
    except:
        logger.error("failed send email : {}. try send it 10 minutes".format(message))
        self.retry(countdown=60*10) # it can write as exponential times
