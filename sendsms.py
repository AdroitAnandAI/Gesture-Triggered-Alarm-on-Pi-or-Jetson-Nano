# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = '*****************************'
auth_token = '*****************************'
client = Client(account_sid, auth_token)

def informSecurity():
    message = client.messages \
                    .create(
                         body="ALERT!!! Someone needs help urgently. Please do the needful at the earliest!",
                         from_='+1*********',
                         to='+1***********'
                     )

    print(message.sid)
