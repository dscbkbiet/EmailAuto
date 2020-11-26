from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES) # !!important!! change creds.json from your credential json file (NAME)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    #sends mail section

    emailFile = open("email.txt","r")  # reads file for emails
    emails = emailFile.read().split("\n")
    emailFile.close()

    htmlMail = open("htmlEmail.txt","r")  # reads file for htmlEmail
    htmlEMail = htmlMail.read()
    htmlMail.close()

    count = 0 

    # !!important!! data to send mail
    sender = "" # your email
    subject = "" # subject
    
    for to in emails:
        message = create_message(sender,to,subject,htmlEMail)
        count += send_message(service,sender,message,to)
    print("%s mails sent successfully!!" % count) # prints no. of successfull sent mails

def create_message(sender,to,subject,message_text):
    message = MIMEText(message_text,"html") # for html email if you're sending plain text omit {, "html"}
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message, to):
    try:
        message = (service.users().messages().send(userId = user_id, body=message).execute())
        print("ID: %s => Message sent: %s" % (message['id'],to))
        return 1
    except Exception as e:
        print("An error ocurred: %s" % e)
        return 0

if __name__ == '__main__':
    main()


