
# Api.Appointment
A simple API that receives messages from Twilio and create events in your Google Calendar

# Configuration
* Create and save your OAuth client credentials (Google Cloud / APIs / Credentials) in a new credentials.json file
* Run 'py main.py' for the first time to stores the user's access and refresh tokens
* Run 'uvicorn main:app --port 10300 --reload' to execute FastAPI
* Run 'ngrok http http://localhost:10300' to expose FastAPI to internet
* Copy output Ngrok URL into Twilio Sandbox Webhook. Don't forget to add target method

## References
### Twilio
* https://www.twilio.com/docs/messaging/tutorials/how-to-receive-and-reply/python
* https://www.twilio.com/docs/usage/webhooks/messaging-webhooks#incoming-message-webhook
* https://www.twilio.com/docs/messaging/twiml
### Google Calendar API
* https://developers.google.com/calendar/api/quickstart/python?hl=es-419