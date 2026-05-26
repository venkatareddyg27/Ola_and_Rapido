from pathlib import Path
import firebase_admin
from firebase_admin import credentials, messaging

BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_PATH = BASE_DIR / "firebase" / "serviceAccountKey.json"

if SERVICE_ACCOUNT_PATH.exists():
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
        firebase_admin.initialize_app(cred)
else:
    print("⚠️ Firebase key not found. Push notifications disabled.")


async def send_push_notification(token, title, body, data=None):
    if not firebase_admin._apps:
        return None

    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data={k: str(v) for k, v in (data or {}).items()}
    )

    return messaging.send(message)