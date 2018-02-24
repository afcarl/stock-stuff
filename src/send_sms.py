# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC95e6f2e5c0551c7b85904f0de8a3de56"
auth_token = "70e1a650c897867b95da29092a2eeb8e"
twilio_number = "+18324301790"


def send_text(message, to_number, from_number=twilio_number):
    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to=to_number,
        from_=from_number,
        body=message)
