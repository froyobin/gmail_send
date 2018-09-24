# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient.discovery import build
from email.header import Header
from httplib2 import Http
from googleapiclient.errors import HttpError
import base64
import time
import datetime
from email.mime.text import MIMEText
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPESWRITE2 = 'https://www.googleapis.com/auth/gmail.compose'
SCOPESWRITE = 'https://www.googleapis.com/auth/gmail.send'


class TenantsInfo:
    def __init__(self, name, date, amount):
        self.name = name
        self.date = date
        self.amount = amount

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def getAmount(self):
        return self.amount


class Email:
    def __init__(self):
        store = file.Storage('creds.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPESWRITE)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text.encode('utf-8'), 'plain', 'utf-8')
        message['to'] = to
        message['from'] = sender
        message['subject'] = Header(subject, 'utf-8')
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def send_message(self, message):
        """Send an email message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId='me', body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except HttpError, error:
            print('An error occurred: %s' % error)


def main():
    tenants = list()
    tenants.append(TenantsInfo("Yan Huang",'29','600'))
    tenants.append(TenantsInfo("ZeHang chen", '21', '610'))
    tenants.append(TenantsInfo("Unknwon", '29', '600'))

    while True:
        now = datetime.datetime.now()
        print (now.day)
        for each in tenants:
            if each.getDate() == now.day:
                message = u'Hi %s,\n\n 记得及时交房租AUD %s,谢谢.\n\n\nregards,\nJoyce'%(each.getName(),each.getAmount())
                title = u'记得在%s号之前交房租AUD %s,谢谢'%(each.getDate(), each.getAmount())

                thisemail = Email()
                email = thisemail.create_message("joyce", "froyo.bin@gmail.com", title, message)
                # Send the Email
                thisemail.send_message(email)
        time.sleep(3600*6)


if __name__ == '__main__':
    main()
