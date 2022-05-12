from twilio.rest import Client
import smtplib
from flight_search import FlightSearch

import flight_search

TWILIO_SID = "YOUR SID"
TWILIO_AUTH_TOKEN = "YOUR TOKEN"
TWILIO_VIRTUAL_NUMBER = "YOUR TWILIO NUMBER"
TWILIO_VERIFIED_NUMBER = "YOUR VERIFIED NUMBER"

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

        def __init__(self):
            self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        
        def send_sms(self, message):
            message = self.client.messages.create(
                body=message,
                from_=TWILIO_VIRTUAL_NUMBER,
                to=TWILIO_VERIFIED_NUMBER,
            )
            # Prints if successfully sent.
            print(message.sid)
