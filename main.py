import google.auth.transport.requests
import os.path
from datetime import date
from fastapi import FastAPI, Request, Response
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.twiml.messaging_response import MessagingResponse
from urllib import parse


def main():
    creds = getCredentials()

def getCredentials():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.json"):
        creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "secrets/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("secrets/token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def getMessage(bytes):
    body = bytes.decode("utf-8")
    dictionary = dict(parse.parse_qsl(body))
    message = dictionary.get("Body")
    return message

def defineDescription(summary, description): 
    if summary == "Cumpleaños":
        return f"Cumpleaños de {description}"
    return None

def defineDate(data):
    data = data.split('-')
    if len(data) < 2:
        return None
    elif len(data) == 2:
        day = defineDay(data[0])
        month = defineMonth(data[1])
        year = date.today().year
        return f"{year}-{month}-{day}"
    elif len(data) == 3:
        day = defineDay(data[0])
        month = defineMonth(data[1])
        year = data[2]
        return f"{year}-{month}-{day}"
    return None

def defineDay(day):
    return "{:02d}".format(int(day))

def defineMonth(monthName):
    months = {
        "Enero": 1, 
        "Febrero": 2, 
        "Marzo": 3, 
        "Abril": 4, 
        "Mayo": 5, 
        "Junio": 6, 
        "Julio": 7, 
        "Agosto": 8, 
        "Septiembre": 9, 
        "Octubre": 10, 
        "Noviembre": 11, 
        "Diciembre": 12}
    month = "{:02}".format(months.get(monthName, 0))
    return month

def createEvent(summary, description, date):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': f'{date}T08:00:00',
            'timeZone': 'America/Mexico_City',
        },
        'end': {
            'dateTime': f'{date}T09:00:00',
            'timeZone': 'America/Mexico_City',
        }, 
        'recurrence': [
            'RRULE:FREQ=YEARLY'
        ]
    }
    return event

def createResponse(message):
    response = MessagingResponse()
    response.message(message)
    return Response(content=str(response), media_type="application/xml")


app = FastAPI()

@app.get("/api")
def test():
    return {"status": "API is running"}

@app.post("/message")
async def message(request: Request):
    bytes = await request.body()
    message = getMessage(bytes)
    print(f"Mensaje recibido: {message}")

    data = message.split(' ')
    if len(data) < 3:
        return createResponse("Mensaje no válido")
    
    summary = data[0]
    description = defineDescription(summary, data[1])
    if description == None:
        return createResponse("Titulo no válido")
    
    date = defineDate(data[2]) 
    if date == None:
        return createResponse("Fecha no válida")
    
    event = createEvent(summary, description, date)

    try:
        creds = getCredentials()
        service = build("calendar", "v3", credentials=creds)
        result = service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

    return createResponse("Evento creado")

if __name__ == "__main__":
  main()