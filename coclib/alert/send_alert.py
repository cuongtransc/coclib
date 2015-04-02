#!/usr/bin/python
#-*- coding: utf-8 -*-

# alert: send_alert
#
# Copyright (C) 20012-2014 coclib
# Authors: Tran Huu Cuong <tranhuucuong91@gmail.com>
# URL:     http://tranhuucuong91.wordpress.com/
# License: BSD

import smtplib
import sys
from . import config


def send_alert(subject, content, recipient='lalahahaaa@gmail.com'):
    """Send alert email"""

    # standardize encoding
    if isinstance(subject, unicode):
        subject = subject.encode('utf-8')
    if isinstance(content, unicode):
        content = content.encode('utf-8')

    sender = config.EMAIL

    headers = [
        "From: coc-alert <%s>" % (sender),
        "Subject: " + subject,
        "To: " + recipient,
        "MIME-Version: 1.0",
        "Content-Type: text/html; charset=utf-8"
    ]
    headers = "\r\n".join(headers)

    try:
        session = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT)
        session.login(config.EMAIL, config.PASSWORD)
    except Exception as e:
        sys.stderr.write("Failed to connect to mail server! %s\n" % e)
        return 1

    try:
        session.sendmail(sender, recipient, headers + "\r\n\r\n" + content)
        print('The email was sent successfully!')
        return 0
    except Exception as e:
        sys.stderr.write("Failed to send email! %s\n" % e)
        return 1
    finally:
        session.quit()


def main():
    send_alert('Alert', 'The web have a update!')


if __name__ == '__main__':
    main()

