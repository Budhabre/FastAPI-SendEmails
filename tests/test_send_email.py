from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch('smtplib.SMTP')
def test_send_email(mock_smtp):
    email = {
        "sender": "sender@gmail.com",
        "receiver": "receiver@gmail.com",
        "subject": "Test Email",
        "body": "This is a test email"
    }

    response = client.post("/send_email/", json=email)

    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully."}
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()
