import os
import base64
import re
import requests
from dotenv import load_dotenv
from openai import OpenAI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_emails(service, label_ids=None, max_results=10):
    result = service.users().messages().list(userId='me', labelIds=label_ids, maxResults=max_results).execute()
    return result.get('messages', [])

def get_email_content(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers", [])
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(sem assunto)')
    parts = payload.get('parts')
    if parts:
        data = parts[0]['body'].get('data')
    else:
        data = payload['body'].get('data')
    decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore') if data else ''
    return subject, decoded_data

def is_email_relevant(subject, body):
    prompt = f"""
    Você é um assistente que ajuda a organizar e-mails. Analise o seguinte conteúdo e diga se é importante ou irrelevante:

    Assunto: {subject}
    Corpo: {body}

    Responda apenas com 'IMPORTANTE' ou 'LIXO'.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().upper()
    return result == 'IMPORTANTE'

def move_to_trash(service, msg_id):
    service.users().messages().trash(userId='me', id=msg_id).execute()

def move_to_spam(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': ['SPAM']}).execute()

def remove_spam_label(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['SPAM']}).execute()

def cancel_subscription_if_found(body):
    links = re.findall(r'(https?://\S*(unsubscribe|descadastre|optout|opt-out|remover|removal)\S*)', body)
    for full_match, _ in links:
        try:
            requests.get(full_match, timeout=50)
            return True
        except:
            continue
    return False

if __name__ == '__main__':
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)
        messages = get_emails(service, max_results=10)

        for msg in messages:
            msg_id = msg['id']
            subject, body = get_email_content(service, msg_id)
            relevante = is_email_relevant(subject, body)

            if not relevante:
                cancel_subscription_if_found(body)
                if 'SPAM' in msg.get('labelIds', []):
                    move_to_trash(service, msg_id)
                else:
                    move_to_spam(service, msg_id)
                    move_to_trash(service, msg_id)
            else:
                if 'SPAM' in msg.get('labelIds', []):
                    remove_spam_label(service, msg_id)

    except HttpError:
        pass
