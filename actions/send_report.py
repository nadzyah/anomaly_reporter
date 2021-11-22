from socket import getfqdn
import os

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from st2common.runners.base_action import Action

class SendReport(Action):

    def run(self, smtp_servername, smtp_server_port, use_ssl, use_starttls,
            sender, client_emails, report_path,
            event_handler_period, sender_username, sender_password):

        if sender_username and sender_password:
            smtp.login(sender_username, sender_password)

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = COMMASPACE.join(client_emails)
        msg["Date"] = formatdate(localtime=True)
        if event_handler_period == 1:
            msg['Subject'] = f"Log report for the last day"
        else:
            msg['Subject'] = f"Log report for last {event_handler_period} days"

        msg.attach(MIMEText("See the report in the attachment."))

        if os.path.exists(report_path) and os.access(report_path, os.R_OK):
            with open(report_path, "rb") as fil:
                part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(report_path)
            )
                part['Content-Disposition'] = 'attachment; filename="%s"' \
                    % os.path.basename(report_path)
                msg.attach(part)
        else:
            return (False, "Cannot access the report file")

        server = getfqdn(smtp_servername)

        if use_ssl:
            smtp = smtplib.SMTP_SSL(server, smtp_server_port)
        else:
            smtp = smtplib.SMTP(server, smtp_server_port)

        smtp.ehlo()
        if use_starttls:
            smtp.starttls()
        smtp.sendmail(sender, client_emails, msg.as_string())
        smtp.close()

        return (True, "The report was send to `%s`" % client_emails)
