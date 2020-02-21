#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Notifier:
    def send(self, subject: str, content: str):
        pass


class MailNotifier(Notifier):
    _from: Header = Header("自动打卡小助手", 'utf-8')
    _to: Header = Header("小主", 'utf-8')

    def __init__(self, host: str, username: str, password: str, receiver: str):
        self._host: str = host
        self._user: str = username
        self._pass: str = password
        self._receiver: str = receiver

    def _make_content(self, subject: str, content: str) -> MIMEText:
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self._from
        message['To'] = self._to
        return message

    def send(self, subject: str, content: str):
        try:
            svr = smtplib.SMTP()
            svr.connect(self._host)
            svr.login(self._user, self._pass)
            message = self._make_content(subject, content)
            svr.sendmail(self._user, self._receiver, message.as_string())
            print("send mail successfully")
        except smtplib.SMTPException:
            print("fail to send mail")


class PrintNotifier(Notifier):
    def send(self, subject: str, content: str):
        print(f'{subject}:\n{content}')
