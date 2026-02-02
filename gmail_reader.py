import base64

def get_email_body(msg):
    payload = msg['payload']
    parts = payload.get('parts')

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        data = payload['body'].get('data')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8')

    return ""

def fetch_unread_email(service):
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=1
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        return None

    msg_id = messages[0]['id']

    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()

    headers = msg['payload']['headers']

    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

    body = get_email_body(msg)

    return {
        'id': msg_id,
        'subject': subject,
        'sender': sender,
        'body': body
    }