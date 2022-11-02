from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import RequestContext

from shared import globals as global_constants


class SendEmail(object):

    def __init__(self,
        request=None,
        headers=None,
        sender=None,
        from_name=None,
        backend=None,
        cc_emails=None,
        bcc_emails=None,
        attachments=[]
    ):
        self.request = request
        self.headers = headers
        self.cc_emails = cc_emails
        self.bcc_emails = bcc_emails
        self.attachments = attachments
        self.from_name = from_name or settings.DEFAULT_FROM_EMAIL
        self.sender = sender or settings.DEFAULT_FROM_EMAIL

    def email_render(self, template_path, context):
        """
        wrapper to generate email body
        """

        if self.request is None:
            body = render_to_string(template_path, context)
        else:
            body = render_to_string(template_path, context, RequestContext(self.request))

        return body

    def send(self, recipient, subject, template_path, context):
        """
        send email function with template_path. will do both rendering & send in this function.
        should not change the interface.
        """

        body = self.email_render(template_path, context)
        self.send_email(recipient, subject, body)

    def send_email(self, recipient, subject, body):
        """
        send email with rendered subject and body
        Sample Attachment List:
            [{'filename': 'file.csv', 'file': '/path/to/file.csv', 'file_type': 'text/csv'}]
        """

        msg = EmailMultiAlternatives(subject,
            body,
            self.sender,
            recipient,
            bcc=self.bcc_emails,
            cc=self.cc_emails
        )
        msg.attach_alternative(body, global_constants.HTML_MIMETYPE)

        if self.attachments:
            for attachment in self.attachments:
                attachment_file = attachment['file']
                if isinstance(attachment_file, str):
                    with open(attachment_file, "rb") as attachment_file:
                        file_content = attachment_file.read()
                elif isinstance(attachment_file, bytes):
                    file_content = attachment_file
                else:
                    file_content = attachment_file.read()

                msg.attach(attachment['filename'], file_content, attachment['file_type'])

        msg.send()