import re
import threading

from django.conf import settings
from django.core.mail import EmailMessage


class MailService():

    def send_group_invite(self, creator_email, invited_email, group_label):

        if not settings.DJANGO_ENV_IS_PROD:
            return

        valid_domains = [
            '@uoguelph.ca',
        ]

        domain = re.search("@[\w.]+", invited_email).group()
        if domain in valid_domains:
            self.send_mail(
                title='Billshare.io Group Invite',
                body='You have been invited by "{}" to join group "{}"\nClick here to accept: https://api.billshare.io/mail/group/invite/'.format(creator_email, group_label),
                emails=[invited_email],
            )

    def send_mail(self, title, body, emails):
        EmailThread(title, body, emails).start()


# Sending mail can take a few seconds, threading doesn't block main execution
class EmailThread(threading.Thread):
    def __init__(self, title, body, emails):
        self.title = title
        self.body = body
        self.emails = emails
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMessage(self.title, self.body, to=self.emails)
        email.send()
