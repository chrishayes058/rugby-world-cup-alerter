import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import smtplib
from email.mime.text import MIMEText
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
# credentials.json is generated for the Gmail API via the google cloud platform
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('gmail', 'v1', credentials=creds)


while True:
    driver = webdriver.Chrome()

    driver.get("https://tickets.rugbyworldcup.com/en")
    matches = driver.find_elements(By.CLASS_NAME, "list-ticket-content")

    for match in matches:
        if "Ireland" in match.text:
            availability = match.find_element(By.CLASS_NAME, "actions-wrapper")
            if "VIEW OFFERS" in availability.text:
                try:
                    message = MIMEText("Match: " + match.text + "\nhttps://tickets.rugbyworldcup.com/en")
                    message['to'] = 'chrishayes058@gmail.com'
                    message['subject'] = 'World Cup Upate'
                    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
                    message = (service.users().messages().send(userId="me", body=create_message).execute())
                    print(F'sent message to {message} Message Id: {message["id"]}')
                except HTTPError as error:
                    print(F'An error occurred: {error}')
                    message = None
    print("Closing at time: " + str(time.time()))
    driver.close()
    time.sleep(120)






