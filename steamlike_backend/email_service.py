import requests
from django.conf import settings


class EmailServiceError(Exception):
    def __init__(self, error, message, status):
        self.error = error
        self.message = message
        self.status = status
        super().__init__(message)


def send_email(to, subject, text, html=None):
    api_key = settings.MAILEROO_API_KEY
    from_address = settings.MAILEROO_FROM

    payload = {
        "from": from_address,
        "to": to,
        "subject": subject,
        "plain_body": text,
    }
    if html:
        payload["html_body"] = html

    try:
        response = requests.post(
            'https://smtp.maileroo.com/send',
            headers={
                'X-API-Key': api_key,
            },
            data={
                'from': from_address,
                'to': to,
                'subject': subject,
                'plain': text,
            },
            timeout=5,
        )
    except requests.Timeout:
        raise EmailServiceError('external_service_unavailable', 'El servicio de email no está disponible.', 503)
    except requests.ConnectionError:
        raise EmailServiceError('external_service_unavailable', 'El servicio de email no está disponible.', 503)
    if not response.ok:
     
        raise EmailServiceError('external_service_error', 'Error al enviar el email.', 502)
    try:
        data = response.json()
        if not data:
            raise ValueError('Respuesta vacía')
    except Exception:
        raise EmailServiceError('external_service_error', 'Error al enviar el email.', 502)

    return data
