# Execute py twilioClient.py

import json
from twilio.rest import Client


def load_secrets():
    with open("secrets/secrets.json", 'r') as file:
        secrets = json.load(file)
    return secrets


if __name__ == "__main__":
  secrets = load_secrets()

  account_sid = secrets.get("twilio_sid")
  auth_token = secrets.get("twilio_token")
  client = Client(account_sid, auth_token)

  message = client.messages.create(
    from_ = secrets.get("twilio_from"),
    body = 'Hello world',
    to = secrets.get("twilio_to")
  )

  print(message.sid)