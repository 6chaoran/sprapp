from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
class Email:
    
    def __init__(self, SENDGRID_API_KEY):
        self.sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)

    def send_mail(self, from_email, recipient_email, template_id, data) -> str:
        """
        data: {
            "username":,
            "password":,
            "applied_date":,
            "description":,
            "closed_date":,
            "status":
        }
        """

        message = Mail(
            from_email=from_email,
            to_emails= recipient_email,
            html_content='<strong>and easy to do anywhere, even with Python</strong>')
        message.dynamic_template_data = data
        message.template_id = template_id

        try:
            response = self.sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            return "ok"
        except Exception as e:
            print(e)
            err = str(e)
        return err