from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_send_email():
    email = {
        "sender": "sender@gmail.com",
        "receiver": "receiver@gmail.com",
        "subject": "Test Email",
        "body": "This is a test email"
    }
    response = client.post("/send_email/", json=email)
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully."}
